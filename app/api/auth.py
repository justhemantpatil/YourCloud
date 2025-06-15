from fastapi import APIRouter, HTTPException
from telethon.sessions import StringSession
from telethon import TelegramClient
from app.core import config
from app.models import user
from app.db.database import SessionLocal
from pydantic import BaseModel
import asyncio

router = APIRouter()

# Create DB tables if not exists
user.Base.metadata.create_all(bind=SessionLocal().bind)

class VerifyRequest(BaseModel):
    phone_number: str
    code: str

class LoginRequest(BaseModel):
    phone_number: str

@router.post("/auth/login/request")
async def send_code(request: LoginRequest):
    client = TelegramClient(StringSession(), config.API_ID, config.API_HASH)
    await client.connect()
    try:
        result = await client.send_code_request(request.phone_number)
        
        # Save BOTH session and phone_code_hash to DB
        session_string = client.session.save()

        db = SessionLocal()
        existing = db.query(user.UserSession).filter(user.UserSession.phone_number == request.phone_number).first()
        if existing:
            existing.session_data = session_string
            existing.phone_code_hash = result.phone_code_hash
        else:
            db.add(user.UserSession(phone_number=request.phone_number, session_data=session_string, phone_code_hash=result.phone_code_hash))
        db.commit()
        db.close()

        await client.disconnect()

        return {"message": "Code sent", "phone_number": request.phone_number}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/auth/login/verify")
async def verify_code(request: VerifyRequest):
    db = SessionLocal()
    user_session = db.query(user.UserSession).filter(user.UserSession.phone_number == request.phone_number).first()
    if not user_session:
        raise HTTPException(status_code=400, detail="No session found")

    client = TelegramClient(StringSession(user_session.session_data), config.API_ID, config.API_HASH)
    await client.connect()

    try:
        await client.sign_in(
            phone=request.phone_number,
            code=request.code,
            phone_code_hash=user_session.phone_code_hash
        )

        # Save full session after successful login
        session_string = client.session.save()
        user_session.session_data = session_string
        db.commit()
        db.close()

        await client.disconnect()

        return {"message": "Login successful"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
