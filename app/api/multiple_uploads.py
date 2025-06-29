from fastapi import APIRouter, UploadFile, Form, HTTPException
from typing import List
from telethon import TelegramClient
from telethon.sessions import StringSession
from app.core import config
from app.models import user
from app.db.database import SessionLocal
import io

router = APIRouter()

@router.post("/upload/photos")
async def upload_multiple_photos(
    phone_number: str = Form(...),
    files: List[UploadFile] = Form(...)
):
    db = SessionLocal()
    user_record = db.query(user.UserSession).filter(user.UserSession.phone_number == phone_number).first()
    db.close()

    if not user_record:
        raise HTTPException(status_code=404, detail="User session not found")

    client = TelegramClient(StringSession(user_record.session_data), config.API_ID, config.API_HASH)
    await client.connect()

    uploaded_files = []

    try:
        for file in files:
            file_bytes = await file.read()
            file_stream = io.BytesIO(file_bytes)
            file_stream.name = file.filename
            await client.send_file("me", file_stream, file_name=file.filename , force_document=True)
            uploaded_files.append(file.filename)

        return {
            "message": "All files uploaded successfully to Telegram",
            "uploaded_files": uploaded_files
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.disconnect()
