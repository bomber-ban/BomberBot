# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/storage/credentials.py

import keyring

SERVICE_NAME = "BomberBotClient"
KEY_NAME = "api_key"


def save_api_key(api_key: str):
    keyring.set_password(SERVICE_NAME, KEY_NAME, api_key)


def load_api_key() -> str | None:
    return keyring.get_password(SERVICE_NAME, KEY_NAME)


def clear_api_key():
    keyring.delete_password(SERVICE_NAME, KEY_NAME)
