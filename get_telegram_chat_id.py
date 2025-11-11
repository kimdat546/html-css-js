#!/usr/bin/env python3
"""
Simple script to get your Telegram Chat ID
Run this on your phone or computer after getting bot token from BotFather
"""

print("=" * 60)
print("📱 TELEGRAM CHAT ID FINDER")
print("=" * 60)
print()
print("Instructions:")
print("1. Get bot token from @BotFather")
print("2. Send any message to your bot")
print("3. Run this script")
print()
print("=" * 60)
print()

# Get bot token from user
bot_token = input("Paste your bot token here: ").strip()

if not bot_token:
    print("❌ No token provided!")
    exit(1)

print()
print("🔍 Fetching your chat ID...")
print()

import requests

try:
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    data = response.json()

    if not data.get("ok"):
        print("❌ Error: Invalid bot token or API error")
        print(f"Response: {data}")
        exit(1)

    results = data.get("result", [])

    if not results:
        print("⚠️  No messages found!")
        print()
        print("Please:")
        print("1. Open Telegram")
        print("2. Find your bot")
        print("3. Send it any message (like 'Hello')")
        print("4. Run this script again")
        exit(1)

    # Get the most recent chat ID
    chat_id = results[-1]["message"]["chat"]["id"]
    first_name = results[-1]["message"]["chat"].get("first_name", "Unknown")

    print("✅ SUCCESS!")
    print()
    print("=" * 60)
    print(f"Your Chat ID: {chat_id}")
    print(f"Name: {first_name}")
    print("=" * 60)
    print()
    print("📋 Add these to Coolify environment variables:")
    print()
    print(f"TELEGRAM_BOT_TOKEN={bot_token}")
    print(f"TELEGRAM_CHAT_ID={chat_id}")
    print(f"NOTIFY_TELEGRAM=true")
    print()
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("Make sure:")
    print("- You have internet connection")
    print("- The bot token is correct")
    print("- You sent a message to your bot")
