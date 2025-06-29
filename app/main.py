from fastapi import FastAPI
from app.api import auth , upload , create_chat_folder , multiple_uploads
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:3000"],  # Change port if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(create_chat_folder.router)
app.include_router(multiple_uploads.router)
