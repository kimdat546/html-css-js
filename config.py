# Laptop Monitoring Tool Configuration

# Stolen Laptop Details
LAPTOP_INFO = {
    "model": "Lenovo Thinkpad T14 GEN 3",
    "full_model": "21AH00JJVA",
    "serial_number": "PF3YR90J",
    "os": "Windows"
}

# Search Keywords (these will be used to search on marketplaces)
SEARCH_KEYWORDS = [
    "Thinkpad T14",
    "T14 Gen 3",
    "T14 GEN 3",
    "21AH00JJVA",
    "Lenovo T14",
    "Thinkpad T14 Gen 3"
]

# Target Locations (areas where thief might sell the laptop)
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

# Facebook Groups (add specific group URLs here)
FACEBOOK_GROUPS = [
    # Add specific Facebook group URLs related to Gia Lai, Kontum, Dak Lak
    # Example: "https://www.facebook.com/groups/muabangialaI"
    # You can add these manually or the script will search Facebook Marketplace
]

# Monitoring Settings
CHECK_INTERVAL_HOURS = 2  # How often to check (in hours)
MAX_RESULTS_PER_SEARCH = 50  # Maximum results to check per search

# Notification Settings
NOTIFY_EMAIL = False  # Set to True if you want email notifications
NOTIFY_TELEGRAM = False  # Set to True if you want Telegram notifications
NOTIFY_CONSOLE = True  # Always show results in console

# Email Settings (if NOTIFY_EMAIL is True)
EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",  # Use app password, not regular password
    "recipient_email": "your_email@gmail.com"
}

# Telegram Settings (if NOTIFY_TELEGRAM is True)
TELEGRAM_SETTINGS = {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
}

# Browser Settings for Facebook scraping
HEADLESS_BROWSER = False  # Set to True to run browser in background (no window)
BROWSER_PROFILE_PATH = "./browser_profile"  # Where to save logged-in browser session
