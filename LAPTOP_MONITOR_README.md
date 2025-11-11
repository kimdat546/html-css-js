# 🚨 Laptop Theft Monitor Tool

A Python-based monitoring tool to help track stolen laptops on Vietnamese marketplaces like Chotot.com and Facebook.

## 📋 Your Laptop Information

- **Model**: Lenovo Thinkpad T14 GEN 3
- **Full Model**: 21AH00JJVA
- **Serial Number**: PF3YR90J
- **Operating System**: Windows
- **Target Locations**: Gia Lai, Kontum, Dak Lak, Pleiku

## 🎯 What This Tool Does

This tool automatically:
1. ✅ Searches **Chotot.com** for laptop listings matching your model
2. ✅ Searches **Facebook Marketplace** for similar listings
3. ✅ Searches **Facebook posts** in target regions (Gia Lai, Kontum, Dak Lak)
4. ✅ Filters results by location (Pleiku area)
5. ✅ Sends notifications when potential matches are found
6. ✅ Generates HTML reports for easy review
7. ✅ Runs continuously to monitor new listings

## 📱 Installation (On Your Phone - Using Termux)

Since you only have your phone, here's how to set it up on Android using Termux:

### Step 1: Install Termux

1. Download **Termux** from F-Droid (NOT Google Play): https://f-droid.org/en/packages/com.termux/
2. Open Termux

### Step 2: Install Python and Git

```bash
# Update packages
pkg update && pkg upgrade -y

# Install Python and Git
pkg install python git -y

# Install required system packages
pkg install libxml2 libxslt -y
```

### Step 3: Download This Tool

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd <REPO_NAME>

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Configure Settings (Optional)

Edit `config.py` to customize:
- Check intervals
- Notification settings
- Search keywords

## 🚀 Usage

### Run Once (Quick Check)

```bash
python monitor.py
```

This will:
- Search Chotot.com
- Search Facebook (you'll need to log in manually once)
- Show results in console
- Generate an HTML report

### Run Continuously (Recommended)

```bash
python monitor.py --continuous
```

This will:
- Run checks every 2 hours (configurable)
- Keep monitoring until you stop it (Ctrl+C)
- Send notifications for new listings only

### Check Only Specific Platform

```bash
# Only check Chotot.com (no Facebook login needed)
python monitor.py --chotot-only

# Only check Facebook
python monitor.py --facebook-only
```

## 🔐 Facebook Login (Important!)

**IMPORTANT**: The tool will NEVER ask for your password in code.

When you run the tool for the first time:

1. A Chrome browser window will open automatically
2. You'll see the Facebook login page
3. **Log in manually** using your credentials
4. After logging in, return to the terminal and press ENTER
5. Your session will be saved and you won't need to log in again

The browser session is saved in `./browser_profile/` directory.

## 📧 Notification Setup (Optional)

### Email Notifications

1. Edit `config.py`:
```python
NOTIFY_EMAIL = True

EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",  # Get from Gmail settings
    "recipient_email": "your_email@gmail.com"
}
```

2. For Gmail, create an **App Password**:
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"
   - Use that password in config

### Telegram Notifications

1. Create a Telegram Bot:
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Copy the bot token

2. Get your Chat ID:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your `chat_id` in the response

3. Edit `config.py`:
```python
NOTIFY_TELEGRAM = True

TELEGRAM_SETTINGS = {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
}
```

## 📊 Understanding Results

When the tool finds matches, you'll see:

### Console Output
```
🚨 ALERT: POTENTIAL MATCHES FOUND FOR YOUR STOLEN LAPTOP 🚨
===============================================================================
Laptop Model: Lenovo Thinkpad T14 GEN 3
Serial Number: PF3YR90J
Total Matches: 3
===============================================================================

--- Match #1 ---
Platform: Chotot.com
Title: Lenovo Thinkpad T14 Gen 3 i7
Price: 15,000,000đ
Location: Pleiku, Gia Lai
URL: https://chotot.com/...
```

### HTML Reports

Reports are saved as `report_YYYYMMDD_HHMMSS.html`

Open them in a browser to see a nicely formatted report with:
- All laptop details
- Each matching listing
- Direct links to view listings
- Safety instructions

### Saved Data

- `all_results.json` - All findings (ever)
- `chotot_results.json` - Latest Chotot results
- `facebook_results.json` - Latest Facebook results

## ⚠️ SAFETY INSTRUCTIONS

**If you find a match:**

1. ✅ **DO**: Take screenshots immediately
2. ✅ **DO**: Contact police with the listing URL
3. ✅ **DO**: Share the HTML report with law enforcement
4. ✅ **DO**: Note the seller's profile information
5. ❌ **DON'T**: Contact the seller directly
6. ❌ **DON'T**: Arrange to meet the seller
7. ❌ **DON'T**: Confront them yourself

Let the police handle recovery - your safety is most important!

## 🔧 Troubleshooting

### "Chrome driver not found"
```bash
# The tool auto-downloads ChromeDriver, but if it fails:
pkg install chromium -y  # On Termux
```

### "Permission denied" errors
```bash
chmod +x monitor.py
```

### Facebook login not working
- Make sure you're using a real browser window (not headless)
- In `config.py`, set `HEADLESS_BROWSER = False`
- Try clearing the browser profile: `rm -rf browser_profile/`

### No results found
This is actually good! It means your laptop hasn't been listed yet. The tool will keep checking.

## 📅 Recommended Schedule

For best results:
- Run **continuously** on a computer/server if possible
- Or run **3-4 times per day** manually
- Peak listing times: morning (8-10 AM) and evening (6-9 PM)

## 🔄 Keeping It Running 24/7 (Advanced)

If you have a computer/server:

```bash
# Using screen (keeps running after terminal closes)
screen -S laptop-monitor
python monitor.py --continuous
# Press Ctrl+A then D to detach

# To reattach later
screen -r laptop-monitor
```

## 📞 Support

If you need help:
1. Check the error messages in the console
2. Make sure all dependencies are installed
3. Verify your internet connection
4. Try running with `--chotot-only` first (simpler)

## 🎯 Expected Behavior

### First Run
- Checks both platforms
- May find older listings (these are already posted)
- Review each one manually

### Subsequent Runs
- Only shows NEW listings (not previously seen)
- This prevents duplicate alerts
- All results are still saved in JSON files

## ⚡ Quick Start (Copy-Paste)

```bash
# Install everything
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 selenium python-dotenv schedule lxml webdriver-manager

# Run the monitor
python monitor.py --continuous
```

## 💡 Tips

1. **Be patient**: Searching Facebook takes time (1-3 minutes per check)
2. **Check results manually**: Not all matches will be your laptop
3. **Location filtering**: Focus on Gia Lai, Kontum, Dak Lak as configured
4. **Save evidence**: Keep all HTML reports for police
5. **Act fast**: If you find a match, contact police immediately

## 🙏 Good Luck!

I hope this tool helps you recover your laptop. Stay safe and let the police handle any confrontations.

---

**Remember**: This tool is for personal use to recover your stolen property. Use it responsibly and always work with law enforcement.
