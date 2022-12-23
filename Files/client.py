from telethon.client.telegramclient import TelegramClient


def start_client(name: str, api_id: str, api_hash: str):
    client = TelegramClient(name, int(api_id), api_hash)
    return client