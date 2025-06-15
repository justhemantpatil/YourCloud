from fastapi import APIRouter, UploadFile, Form, HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession
from app.core import config
from app.models import user
from app.db.database import SessionLocal
import io

router = APIRouter()

@router.post("/upload/photo")
async def upload_photo(
    phone_number: str = Form(...),
    file_name: str = Form(...),
    file: UploadFile = Form(...)
):
    db = SessionLocal()
    user_record = db.query(user.UserSession).filter(user.UserSession.phone_number == phone_number).first()
    db.close()
    if not user_record:
        raise HTTPException(status_code=404, detail="User session not found")

    client = TelegramClient(StringSession(user_record.session_data), config.API_ID, config.API_HASH)
    await client.connect()

    try:
        file_bytes = await file.read()
        # Create file-like object from bytes
        file_stream = io.BytesIO(file_bytes)
        file_stream.name = file_name  # <-- This is important, Telethon reads this name

        await client.send_file("me", file_stream, file_name=file_name)

        return {"message": "File uploaded to Telegram"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.disconnect()
