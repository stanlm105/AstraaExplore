import os, json
from flask import Flask, request, jsonify
from sqlalchemy import select, func
from pathlib import Path
from services.target_guidance_computer.db import SessionLocal, init_db
from services.target_guidance_computer.models import TgcAccount, TgcSeen
from services.target_guidance_computer.auth import create_account_if_missing, verify_login
from services.target_guidance_computer.seen import mark_seen, unsee, list_seen_for, progress_for

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Load catalog once at startup
project_root = Path(app.config.get("PROJECT_ROOT", Path(__file__).resolve().parent.parent.parent))
catalog_path = project_root / "data" / "messier_catalog.json"
with open(catalog_path, "r") as f:
    CATALOG = json.load(f)
    
# Init DB / create tables
init_db()

@app.get("/api/health")
def health():
    return {"ok": True, "db": True, "catalog_items": len(CATALOG)}

@app.post("/api/login")
def login():
    data = request.get_json(force=True)
    room = data.get("room_name","").strip()
    country = data.get("country","").strip()
    zipcode = data.get("zipcode","").strip()
    passphrase = data.get("passphrase","")

    if not all([room, country, zipcode, passphrase]):
        return jsonify({"error": "room_name, country, zipcode, passphrase required"}), 400

    with SessionLocal() as db:
        acct_id = verify_login(db, room, country, zipcode, passphrase)
        if acct_id is None:
            # Optionally auto-create if not found (comment out if you prefer strict)
            try:
                acct_id = create_account_if_missing(db, room, country, zipcode, passphrase)
            except ValueError as e:
                return str(e), 400
        return {"account_id": acct_id}

@app.get("/api/catalog")
def catalog():
    # Minimal catalog list
    return jsonify(CATALOG)

@app.get("/api/seen")
def get_seen():
    account_id = request.args.get("account_id", type=int)
    if not account_id:
        return {"error": "account_id required"}, 400
    with SessionLocal() as db:
        items = list_seen_for(db, account_id, catalog="M")
        return jsonify(items)

@app.post("/api/seen")
def add_seen():
    data = request.get_json(force=True)
    account_id = data.get("account_id")
    catalog = data.get("catalog","M").upper()
    number = data.get("number")
    note = data.get("note")
    if not all([account_id, catalog, number]):
        return {"error":"account_id, catalog, number required"}, 400
    with SessionLocal() as db:
        mark_seen(db, account_id, catalog, int(number), note)
        return {"ok": True}

@app.delete("/api/seen")
def del_seen():
    account_id = request.args.get("account_id", type=int)
    catalog = request.args.get("catalog","M").upper()
    number = request.args.get("number", type=int)
    if not all([account_id, catalog, number]):
        return {"error":"account_id, catalog, number required"}, 400
    with SessionLocal() as db:
        unsee(db, account_id, catalog, int(number))
        return {"ok": True}

@app.get("/api/progress")
def progress():
    account_id = request.args.get("account_id", type=int)
    if not account_id:
        return {"error":"account_id required"}, 400
    with SessionLocal() as db:
        return jsonify(progress_for(db, account_id, CATALOG))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        room = request.form.get("room_name", "").strip()
        country = request.form.get("country", "").strip()
        zipcode = request.form.get("zipcode", "").strip()
        passphrase = request.form.get("passphrase", "")
        # You could call your login logic here, or redirect to /api/login
        return f"<h3>Login submitted for room: {room}, country: {country}, zipcode: {zipcode}</h3>"
    return """
    <font face=arial><h2>Messier Target Guidance Computer Login</h2>
    <form method="post">
        <table border=0><tr>
        <td>Room Name:</td><td><input type="text" name="room_name" required></td></tr>
        <tr><td>Country (2-letter code):</td><td><input type="text" name="country" maxlength="2" required></td></tr>
        <tr><td>Zip Code:</td><td><input type="text" name="zipcode" required></td></tr>
        <tr><td>Passphrase:</td><td><input type="password" name="passphrase" required></td></tr>
        <tr><td colspan=2 align=center><button type="submit">Open 'Room'!</button></td></tr>
        </table>
    </form>
    <p>This 'login' is minimal and just helps you track your progress with a little lightweight recordkeepping on this side. No personal data is stored. One can share their room/country/zip with others to share tracking. Country/Zipcode will be used with publically available data to approximate a location that drives the recommended Messier target based on weather, darkness, date and position. If the lookup doesn't work out so well, maybe we'll switch to latitude/longitude in an update, but let's try this first!</p>
    </font>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
