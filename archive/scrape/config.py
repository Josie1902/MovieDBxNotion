# Import secret
import os
from dotenv import load_dotenv
from dotenv import dotenv_values

# Load secrets
load_dotenv()
config = dotenv_values(".env")
API_READ_ACCESS_TOKEN = os.getenv("API_READ_ACCESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"

# Construct the headers
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}"
}