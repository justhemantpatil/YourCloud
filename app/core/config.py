from dotenv import load_dotenv
import os

load_dotenv()  # Make sure .env is in your working directory

API_ID   = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
DATABASE_URL = "sqlite:///./test.db"

# If API_ID or API_HASH is None, check your .env file and working directory.