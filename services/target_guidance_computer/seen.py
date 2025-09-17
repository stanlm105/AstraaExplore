from sqlalchemy import select, delete
from services.target_guidance_computer.models import TgcSeen

def mark_seen(db, account_id, catalog, number, note=None):
    row = db.get(TgcSeen, {"account_id":account_id,"catalog":catalog,"catalog_number":number})
    if row is None:
        row = TgcSeen(account_id=account_id, catalog=catalog, catalog_number=number, note=note)
        db.add(row)
    else:
        if note is not None:
            row.note = note
    db.commit()

def unsee(db, account_id, catalog, number):
    row = db.get(TgcSeen, {"account_id":account_id,"catalog":catalog,"catalog_number":number})
    if row:
        db.delete(row); db.commit()

def list_seen_for(db, account_id, catalog="M"):
    rows = db.execute(
        select(TgcSeen).where(TgcSeen.account_id==account_id, TgcSeen.catalog==catalog)
        .order_by(TgcSeen.catalog_number)
    ).scalars().all()
    return [{"catalog":r.catalog, "number":r.catalog_number, "first_seen_at":r.first_seen_at.isoformat(), "note":r.note} for r in rows]

def progress_for(db, account_id, catalog_json):
    # catalog_json is a list of dicts like {"catalog":"M","number":31,"name":"Andromeda",...}
    seen = {(x["catalog"], x["number"]) for x in list_seen_for(db, account_id, catalog="M")}
    total = sum(1 for x in catalog_json if x["catalog"]=="M")
    seen_cnt = sum(1 for x in catalog_json if (x["catalog"], x["number"]) in seen)
    remaining = [x for x in catalog_json if x["catalog"]=="M" and (x["catalog"], x["number"]) not in seen]
    pct = round(100.0 * seen_cnt / total, 1) if total else 0.0
    return {"total": total, "seen": seen_cnt, "pct": pct, "remaining_sample": remaining[:10]}
