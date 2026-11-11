"""Configuration loaded from environment variables."""
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "Maroz_Maria").strip().lstrip("@")
MINIAPP_URL = os.getenv("MINIAPP_URL", "").strip()

if not CONTACT_USERNAME:
    CONTACT_USERNAME = "Maroz_Maria"
