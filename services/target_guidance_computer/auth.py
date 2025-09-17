from sqlalchemy import select
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from services.target_guidance_computer.models import TgcAccount

def create_account_if_missing(db, room_name, country, zipcode, plain_pass):
    acct = db.execute(
        select(TgcAccount).where(
            TgcAccount.room_name==room_name,
            TgcAccount.country==country,
            TgcAccount.zipcode==zipcode
        )
    ).scalar_one_or_none()
    if acct:
        return acct.id
    acct = TgcAccount(
        room_name=room_name, country=country, zipcode=zipcode,
        passphrase=generate_password_hash(plain_pass)
    )
    db.add(acct); db.commit(); db.refresh(acct)
    return acct.id

def verify_login(db, room_name, country, zipcode, plain_pass):
    acct = db.execute(
        select(TgcAccount).where(
            TgcAccount.room_name==room_name,
            TgcAccount.country==country,
            TgcAccount.zipcode==zipcode
        )
    ).scalar_one_or_none()
    if acct and check_password_hash(acct.passphrase, plain_pass):
        acct.last_login_at = func.now()
        db.commit()
        return acct.id
    return None
