from fastapi import APIRouter, HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetDialogFiltersRequest, UpdateDialogFilterRequest
from telethon.tl.types import DialogFilter
from app.core import config
from app.models import user
from app.db.database import SessionLocal
from pydantic import BaseModel


router = APIRouter()

class VerifyRequest(BaseModel):
    phone_number: str
 

@router.post("/create-yourcloud-folder")
async def create_yourcloud_folder(request: VerifyRequest):
    # Load session string from DB
    db = SessionLocal()
    user_record = db.query(user.UserSession).filter(user.UserSession.phone_number == request.phone_number).first()
    db.close()

    if not user_record:
        raise HTTPException(status_code=404, detail="User session not found")

    client = TelegramClient(StringSession(user_record.session_data), config.API_ID, config.API_HASH)
    await client.connect()

    try:
        # Fetch existing dialog filters (folders)
        filters = await client(GetDialogFiltersRequest())

        existing_folders = filters.get('filters', [])
        folder_count = len(existing_folders)

        if folder_count >= 10:
            return {
                "status": "error",
                "message": "Cannot create chat folder. Limit exceeded (10 folders). Please delete one manually."
            }

        # Create unique id (1-10 safe range)
        existing_ids = {folder.id for folder in existing_folders}
        new_id = 1
        while new_id in existing_ids:
            new_id += 1

        # Create YourCloud folder (empty for now)
        yourcloud_folder = DialogFilter(
            id=new_id,
            title="YourCloud",
            include_peers=[]
        )

        # Build new full filters list (add existing + new folder)
        updated_filters = existing_folders + [yourcloud_folder]

        await client(UpdateDialogFilterRequest(filters=updated_filters))

        return {
            "status": "success",
            "message": f"YourCloud folder created with id {new_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.disconnect()
