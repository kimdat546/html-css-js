# 🚨 Laptop Theft Monitor

Automated monitoring tool to track stolen laptops on Vietnamese marketplaces (Chotot.com, Facebook).

## 📋 Stolen Laptop Details

- **Model**: Lenovo Thinkpad T14 GEN 3
- **Full Model**: 21AH00JJVA
- **Serial Number**: PF3YR90J
- **Target Locations**: Gia Lai, Kontum, Dak Lak, Pleiku

---

## 🚀 Quick Deploy to Coolify

**For phone users deploying to Coolify server:**

👉 **[Read Complete Coolify Deployment Guide](COOLIFY_DEPLOYMENT.md)**

**Quick steps:**
1. Create new app in Coolify
2. Point to this GitHub repo
3. Set environment variables (see guide)
4. Set up Telegram notifications
5. Deploy and monitor!

---

## 🎯 Features

✅ **Automated marketplace monitoring**
- Chotot.com scraper
- Facebook Marketplace scraper
- Scheduled checks every 2 hours

✅ **Smart notifications**
- Telegram (recommended for phone)
- Email
- Console logs

✅ **Intelligent filtering**
- Location-based matching
- Keyword search
- Duplicate detection

✅ **Evidence collection**
- HTML reports
- JSON data export
- Screenshot-ready formats

---

## 📦 Deployment Options

### Option 1: Coolify (Recommended for Phone Users)

See **[COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)** for complete guide.

### Option 2: Docker Compose

```bash
# Clone repository
git clone https://github.com/kimdat546/html-css-js.git
cd html-css-js
git checkout claude/laptop-theft-monitor-tool-011CV1kU8ab4WayUeP9ExpKk

# Create .env file
cp .env.example .env
# Edit .env with your details

# Run with Docker Compose
docker compose up -d

# View logs
docker compose logs -f
```

### Option 3: Local Python

See **[LAPTOP_MONITOR_README.md](LAPTOP_MONITOR_README.md)** for detailed local setup.

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run monitor
python monitor.py --continuous
```

---

## ⚙️ Configuration

All configuration via environment variables (see `.env.example`):

### Required
```bash
LAPTOP_MODEL=Lenovo Thinkpad T14 GEN 3
LAPTOP_SERIAL=PF3YR90J
HEADLESS_BROWSER=true  # For server deployment
```

### Telegram Notifications (Recommended)
```bash
NOTIFY_TELEGRAM=true
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Email Notifications (Optional)
```bash
NOTIFY_EMAIL=true
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

**Complete variable list**: See `.env.example`

---

## 📊 How It Works

1. **Scheduled Monitoring**: Runs every 2 hours (configurable)
2. **Multi-Platform Search**: Checks Chotot.com and Facebook
3. **Smart Filtering**: Matches by keywords and locations
4. **Instant Alerts**: Sends notifications when matches found
5. **Evidence Collection**: Generates reports and saves data

---

## 🔐 Security & Privacy

- ✅ No passwords in code (environment variables only)
- ✅ Browser session saved locally/in volume
- ✅ Manual Facebook login (you control credentials)
- ✅ All data stays on your server
- ✅ No external services (except notifications)

---

## 📱 Usage

### View Results

**Telegram**: Instant notifications on your phone

**Logs**:
```bash
# Docker
docker compose logs -f

# Coolify
Check Logs tab in app dashboard
```

**Files**:
- `all_results.json` - All findings
- `report_YYYYMMDD_HHMMSS.html` - Visual reports

### Commands

```bash
# Run once
python monitor.py

# Run continuously (recommended)
python monitor.py --continuous

# Check only Chotot
python monitor.py --chotot-only

# Check only Facebook
python monitor.py --facebook-only
```

---

## ⚠️ If You Find a Match

**DO:**
- ✅ Take screenshots immediately
- ✅ Contact police with listing URL
- ✅ Save HTML reports as evidence
- ✅ Note seller information

**DON'T:**
- ❌ Contact seller directly
- ❌ Arrange meetings yourself
- ❌ Confront the thief

**Let police handle recovery - stay safe!**

---

## 🛠️ Troubleshooting

### No Results
✅ **This is good!** Means laptop hasn't been listed yet. Keep monitoring.

### Telegram Not Working
1. Verify bot token and chat ID
2. Message bot first to start conversation
3. Check environment variables

### Container Crashes
1. Check logs for errors
2. Verify environment variables set
3. Ensure 2GB memory minimum

**More help**: See deployment guides or check logs.

---

## 📚 Documentation

- **[COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)** - Deploy from phone to Coolify
- **[LAPTOP_MONITOR_README.md](LAPTOP_MONITOR_README.md)** - Detailed setup & usage
- **[.env.example](.env.example)** - All environment variables

---

## 🏗️ Project Structure

```
├── monitor.py              # Main monitoring script
├── chotot_scraper.py       # Chotot.com scraper
├── facebook_scraper.py     # Facebook scraper
├── notifier.py             # Notification system
├── config.py               # Configuration loader
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── docker-compose.yml      # Docker Compose config
├── .env.example            # Environment variables template
└── COOLIFY_DEPLOYMENT.md   # Deployment guide
```

---

## 🔄 Updates

Pull latest changes:
```bash
git pull origin claude/laptop-theft-monitor-tool-011CV1kU8ab4WayUeP9ExpKk
```

For Coolify: Just click "Redeploy" in dashboard.

---

## 💡 Tips

1. **Set up Telegram** - Easiest for phone notifications
2. **Start with Chotot only** - Facebook needs manual login
3. **Check every 2 hours** - Balance between coverage and resources
4. **Monitor Pleiku area** - Police indicated thief went there
5. **Save all evidence** - Screenshots and reports for police

---

## 📞 Support

**Check logs first** - Most issues show in logs

**Common Solutions**:
- Missing env variables → Check `.env` or Coolify settings
- Memory issues → Increase to 2GB minimum
- Chrome errors → Ensure Dockerfile installs Chromium correctly

---

## ⭐ Quick Start for Phone Users

1. Open Coolify on phone browser
2. Create new app → Public repository
3. Repository: `https://github.com/kimdat546/html-css-js.git`
4. Branch: `claude/laptop-theft-monitor-tool-011CV1kU8ab4WayUeP9ExpKk`
5. Add environment variables (laptop details, Telegram)
6. Deploy!
7. Get notifications on Telegram

**Detailed guide**: [COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)

---

**Stay safe and good luck recovering your laptop!** 🙏

---

## License

Personal use for stolen property recovery. Not for commercial use.
