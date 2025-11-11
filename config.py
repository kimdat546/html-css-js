"""
Laptop Monitoring Tool Configuration
Loads configuration from environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Stolen Laptop Details (from environment variables)
LAPTOP_INFO = {
    "model": os.getenv("LAPTOP_MODEL", "Lenovo Thinkpad T14 GEN 3"),
    "full_model": os.getenv("LAPTOP_FULL_MODEL", "21AH00JJVA"),
    "serial_number": os.getenv("LAPTOP_SERIAL", "PF3YR90J"),
    "os": os.getenv("LAPTOP_OS", "Windows")
}

# Search Keywords (from environment variable or default list)
# Can be comma-separated string in env: "keyword1,keyword2,keyword3"
_keywords_env = os.getenv("SEARCH_KEYWORDS", "")
if _keywords_env:
    SEARCH_KEYWORDS = [k.strip() for k in _keywords_env.split(",")]
else:
    SEARCH_KEYWORDS = [
        "Thinkpad T14",
        "T14 Gen 3",
        "T14 GEN 3",
        "21AH00JJVA",
        "Lenovo T14",
        "Thinkpad T14 Gen 3"
    ]

# Target Locations (from environment variable or default list)
# Can be comma-separated string in env: "location1,location2,location3"
_locations_env = os.getenv("TARGET_LOCATIONS", "")
if _locations_env:
    TARGET_LOCATIONS = [loc.strip() for loc in _locations_env.split(",")]
else:
    TARGET_LOCATIONS = [
        "Gia Lai",
        "Kontum",
        "Dak Lak",
        "Daklak",
        "Pleiku",
        "Buon Ma Thuot",
        "Kon Tum"
    ]

# Chotot.com Settings
CHOTOT_URL = "https://www.chotot.com"
CHOTOT_SEARCH_URL = "https://www.chotot.com/mua-ban-laptop"

# Facebook Groups (from environment variable or empty list)
# Can be comma-separated string in env
_fb_groups_env = os.getenv("FACEBOOK_GROUPS", "")
if _fb_groups_env:
    FACEBOOK_GROUPS = [g.strip() for g in _fb_groups_env.split(",")]
else:
    FACEBOOK_GROUPS = []

# Monitoring Settings
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", "2"))
MAX_RESULTS_PER_SEARCH = int(os.getenv("MAX_RESULTS_PER_SEARCH", "50"))

# Notification Settings
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "false").lower() == "true"
NOTIFY_TELEGRAM = os.getenv("NOTIFY_TELEGRAM", "false").lower() == "true"
NOTIFY_CONSOLE = os.getenv("NOTIFY_CONSOLE", "true").lower() == "true"

# Email Settings (all from environment variables)
EMAIL_SETTINGS = {
    "smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
    "sender_email": os.getenv("EMAIL_SENDER", ""),
    "sender_password": os.getenv("EMAIL_PASSWORD", ""),
    "recipient_email": os.getenv("EMAIL_RECIPIENT", os.getenv("EMAIL_SENDER", ""))
}

# Telegram Settings (all from environment variables)
TELEGRAM_SETTINGS = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID", "")
}

# Browser Settings for Facebook scraping
HEADLESS_BROWSER = os.getenv("HEADLESS_BROWSER", "false").lower() == "true"
BROWSER_PROFILE_PATH = os.getenv("BROWSER_PROFILE_PATH", "./browser_profile")

# Validate required settings
def validate_config():
    """Validate that required configuration is present"""
    errors = []

    if not LAPTOP_INFO["model"]:
        errors.append("LAPTOP_MODEL is required")

    if not LAPTOP_INFO["serial_number"]:
        errors.append("LAPTOP_SERIAL is required")

    if NOTIFY_EMAIL:
        if not EMAIL_SETTINGS["sender_email"]:
            errors.append("EMAIL_SENDER is required when NOTIFY_EMAIL is true")
        if not EMAIL_SETTINGS["sender_password"]:
            errors.append("EMAIL_PASSWORD is required when NOTIFY_EMAIL is true")

    if NOTIFY_TELEGRAM:
        if not TELEGRAM_SETTINGS["bot_token"]:
            errors.append("TELEGRAM_BOT_TOKEN is required when NOTIFY_TELEGRAM is true")
        if not TELEGRAM_SETTINGS["chat_id"]:
            errors.append("TELEGRAM_CHAT_ID is required when NOTIFY_TELEGRAM is true")

    if errors:
        print("⚠️  Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease check your .env file or environment variables.")

    return len(errors) == 0

# Auto-validate on import (optional, can be disabled)
if __name__ != "__main__":
    # Don't validate during import to avoid errors, validate in main script instead
    pass
