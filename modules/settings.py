import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHANNELS = {-1001825051597: ("Azizbek Zaylobiddinov", "https://t.me/abdulazizziy")}


class URLs:
    BASE_URL = os.getenv("BASE_URL") or "http://localhost:8000"

    # Users endpoints
    USERS_API_ENDPOINT = BASE_URL + "/api/users/"
    GET_USERS = USERS_API_ENDPOINT + "get/"
    ADD_USER_ENDPOINT = USERS_API_ENDPOINT + "add/"
    UPDATE_OR_ADD_USER_ENDPOINT = USERS_API_ENDPOINT + "update/"

    @staticmethod
    def get_user_endpoint(user_id):
        return f"{URLs.USERS_API_ENDPOINT}get/{user_id}"
