# 🚀 Deploying to Coolify - Complete Guide

This guide will help you deploy the Laptop Theft Monitor to your Coolify server from your phone.

## 📱 Prerequisites

- ✅ Coolify server already running
- ✅ Access to Coolify web interface (on your phone browser)
- ✅ This GitHub repository
- ✅ (Optional) Telegram bot for notifications

---

## 🎯 Step-by-Step Deployment

### Step 1: Access Coolify

1. Open your Coolify server URL in your phone browser
2. Log in to your Coolify dashboard

### Step 2: Create New Application

1. Click **"+ New Resource"** or **"+ Add"**
2. Select **"Application"**
3. Choose **"Public Repository"**

### Step 3: Configure Repository

Fill in these details:

**Repository Settings:**
- **Git Repository URL**: `https://github.com/kimdat546/html-css-js.git`
- **Branch**: `claude/laptop-theft-monitor-tool-011CV1kU8ab4WayUeP9ExpKk`
- **Build Pack**: Docker (Auto-detected from Dockerfile)

**General Settings:**
- **Name**: `laptop-theft-monitor`
- **Description**: Monitors marketplaces for stolen laptop

### Step 4: Environment Variables

Click on **"Environment Variables"** and add these (very important!):

#### Required Variables:

```bash
# Laptop Information
LAPTOP_MODEL=Lenovo Thinkpad T14 GEN 3
LAPTOP_FULL_MODEL=21AH00JJVA
LAPTOP_SERIAL=PF3YR90J
LAPTOP_OS=Windows

# Search Keywords (comma-separated)
SEARCH_KEYWORDS=Thinkpad T14,T14 Gen 3,T14 GEN 3,21AH00JJVA,Lenovo T14,Thinkpad T14 Gen 3

# Target Locations (comma-separated)
TARGET_LOCATIONS=Gia Lai,Kontum,Dak Lak,Daklak,Pleiku,Buon Ma Thuot,Kon Tum

# Monitoring Settings
CHECK_INTERVAL_HOURS=2
HEADLESS_BROWSER=true

# Notifications
NOTIFY_CONSOLE=true
NOTIFY_TELEGRAM=true
```

#### Telegram Notification Setup (Recommended for phone):

```bash
# Get these from Telegram (see instructions below)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**How to get Telegram credentials:**

1. Open Telegram on your phone
2. Search for **@BotFather**
3. Send: `/newbot`
4. Follow instructions to create bot
5. Copy the **bot token** (looks like: `123456789:ABCdef...`)
6. Message your new bot with anything (e.g., "Hello")
7. Visit in browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
8. Find **"chat":{"id":123456789}** - that's your chat ID
9. Add both values to Coolify environment variables

#### Optional - Email Notifications:

```bash
NOTIFY_EMAIL=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENT=your_email@gmail.com
```

**For Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Create new app password for "Mail"
3. Copy the 16-character password
4. Use it as `EMAIL_PASSWORD`

### Step 5: Configure Volumes (Important!)

In Coolify, add these persistent volumes:

1. **Browser Profile Volume:**
   - **Source**: `laptop-monitor-browser`
   - **Destination**: `/app/browser_profile`
   - **Type**: Named Volume

2. **Data Volume:**
   - **Source**: `laptop-monitor-data`
   - **Destination**: `/app/data`
   - **Type**: Named Volume

This saves browser login session and results between restarts.

### Step 6: Advanced Settings

**Resources:**
- **Memory Limit**: 2GB (minimum, for Chrome)
- **CPU Limit**: 1 CPU core

**Security:**
- **Shared Memory Size**: 2GB (required for Chrome)

**Restart Policy:**
- Select: **"Unless Stopped"**

### Step 7: Deploy!

1. Click **"Save"** to save all settings
2. Click **"Deploy"** button
3. Wait for build to complete (5-10 minutes first time)

### Step 8: Monitor Logs

After deployment:
1. Go to **"Logs"** tab in Coolify
2. You should see:
   ```
   🚀 STARTING LAPTOP MONITOR
   ===============================================================================
   Laptop: Lenovo Thinkpad T14 GEN 3
   Serial: PF3YR90J
   ```

3. Watch for alerts in Telegram!

---

## 🔐 Facebook Login (One-Time Setup)

**IMPORTANT**: For Facebook scraping to work, you need to log in once.

Since you're on a phone and the container runs headless, here's how:

### Option 1: Skip Facebook (Recommended for Now)

Just use Chotot.com monitoring:
- Remove or comment out Facebook scraper calls
- Focus on Chotot which doesn't need login
- Set up Facebook later when you have computer access

### Option 2: Use SSH (If you have server SSH access)

1. SSH into your Coolify server
2. Find the container:
   ```bash
   docker ps | grep laptop
   ```
3. Execute into container:
   ```bash
   docker exec -it <container_id> bash
   ```
4. Temporarily disable headless:
   ```bash
   export HEADLESS_BROWSER=false
   python monitor.py --facebook-only
   ```
5. Follow login instructions

### Option 3: Setup Later

- The tool will work with Chotot.com only
- Facebook can be added later when you have computer access
- You'll still get valuable monitoring from Chotot

---

## 📊 Checking Results

### Via Telegram

If you set up Telegram, you'll get instant notifications:
- Message format: Listing title, price, location, link
- Click links to view listings
- Take screenshots for police

### Via Coolify Logs

1. Go to your app in Coolify
2. Click **"Logs"** tab
3. See all findings in console output

### Via Container Files

SSH into server:
```bash
# Find container
docker ps | grep laptop

# View results JSON
docker exec <container_id> cat /app/data/all_results.json

# View latest HTML report
docker exec <container_id> ls -t /app/report_*.html | head -1
```

---

## 🔧 Troubleshooting

### Build Fails

**Error**: Out of memory
- Increase server RAM or build on different machine
- Use pre-built Docker image instead

**Error**: Chrome installation fails
- Check Dockerfile is using Debian/Ubuntu base
- Verify internet connection on server

### Container Crashes

Check logs in Coolify:
```
Application error
```

**Solution**: Check environment variables are set correctly

### No Results

**This is good!** Means laptop hasn't been listed yet.

Check logs show:
```
✅ CHECK COMPLETE - No new matches found
⏰ Next check in 2 hour(s)
```

### Telegram Not Working

1. Verify bot token and chat ID are correct
2. Make sure you messaged the bot first
3. Check `NOTIFY_TELEGRAM=true` is set
4. View logs for error messages

---

## 📱 Managing from Phone

### Restart Container

In Coolify app page:
1. Click **"Actions"**
2. Click **"Restart"**

### View Logs

1. Go to app in Coolify
2. Click **"Logs"** tab
3. Enable auto-refresh

### Update Environment Variables

1. Click **"Environment Variables"**
2. Edit values
3. Click **"Save"**
4. Restart container

### Stop Monitoring

1. Click **"Actions"**
2. Click **"Stop"**

---

## ⚙️ Customization

### Change Check Frequency

Update in Coolify environment variables:
```bash
CHECK_INTERVAL_HOURS=1  # Check every hour
```
Then restart.

### Add More Keywords

```bash
SEARCH_KEYWORDS=Thinkpad T14,T14 Gen 3,Your Custom Keyword,Another Keyword
```

### Add More Locations

```bash
TARGET_LOCATIONS=Gia Lai,Kontum,Dak Lak,Your City,Another City
```

---

## 🎯 Recommended Setup for Phone-Only

```bash
# Required
LAPTOP_MODEL=Lenovo Thinkpad T14 GEN 3
LAPTOP_SERIAL=PF3YR90J
HEADLESS_BROWSER=true
CHECK_INTERVAL_HOURS=2

# Telegram (easiest for phone)
NOTIFY_TELEGRAM=true
TELEGRAM_BOT_TOKEN=<your_token>
TELEGRAM_CHAT_ID=<your_chat_id>

# Keywords and locations
SEARCH_KEYWORDS=Thinkpad T14,T14 Gen 3,21AH00JJVA
TARGET_LOCATIONS=Gia Lai,Kontum,Dak Lak,Pleiku
```

This setup:
- ✅ Monitors Chotot.com automatically
- ✅ Sends alerts to your phone via Telegram
- ✅ Runs 24/7 on your server
- ✅ No computer needed

---

## 📞 Need Help?

**Check logs first:**
- Coolify → Your App → Logs

**Common issues:**
- Environment variables not set → Add them in Coolify
- Memory issues → Increase container memory limit
- Telegram not working → Verify token and chat ID

**Test locally first:**
```bash
docker compose up
```

---

## 🔄 Updates

To update the code:

1. I push new code to GitHub
2. In Coolify, click **"Redeploy"**
3. Coolify pulls latest code and rebuilds
4. Environment variables persist automatically

---

## 🌟 You're All Set!

Once deployed:
- ✅ Monitoring runs every 2 hours automatically
- ✅ Telegram alerts come to your phone
- ✅ No manual intervention needed
- ✅ Runs 24/7 on your server

**Stay safe and good luck recovering your laptop!** 🙏

---

## 📋 Quick Checklist

Before deploying, make sure you have:

- [ ] Coolify server accessible
- [ ] GitHub repository URL
- [ ] Branch name: `claude/laptop-theft-monitor-tool-011CV1kU8ab4WayUeP9ExpKk`
- [ ] Laptop details (model, serial)
- [ ] Telegram bot token and chat ID
- [ ] Environment variables configured in Coolify
- [ ] Volumes configured for persistence
- [ ] Memory limit set to 2GB minimum

Once deployed:
- [ ] Check logs show successful start
- [ ] Verify first check completes
- [ ] Test Telegram notification
- [ ] Bookmark Coolify app page for easy access
