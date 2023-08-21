# Import secret
import os
from dotenv import load_dotenv
from dotenv import dotenv_values

# Load secrets
load_dotenv()
config = dotenv_values(".env")
MY_NOTION_TOKEN = os.getenv("MY_NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {MY_NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}