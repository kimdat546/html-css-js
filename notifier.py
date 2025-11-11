"""
Notification Module
Sends alerts when potential matches are found
Supports: Console, Email, and Telegram notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
from config import (
    NOTIFY_EMAIL, NOTIFY_TELEGRAM, NOTIFY_CONSOLE,
    EMAIL_SETTINGS, TELEGRAM_SETTINGS, LAPTOP_INFO
)


class Notifier:
    def __init__(self):
        self.email_enabled = NOTIFY_EMAIL
        self.telegram_enabled = NOTIFY_TELEGRAM
        self.console_enabled = NOTIFY_CONSOLE

    def notify(self, results):
        """Send notifications for found results"""
        if not results:
            self.console_message("✅ No new listings found.")
            return

        # Send notifications via all enabled channels
        if self.console_enabled:
            self.notify_console(results)

        if self.email_enabled:
            self.notify_email(results)

        if self.telegram_enabled:
            self.notify_telegram(results)

    def console_message(self, message):
        """Print message to console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")

    def notify_console(self, results):
        """Display results in console"""
        print("\n" + "="*80)
        print("🚨 ALERT: POTENTIAL MATCHES FOUND FOR YOUR STOLEN LAPTOP 🚨")
        print("="*80)
        print(f"Laptop Model: {LAPTOP_INFO['model']}")
        print(f"Serial Number: {LAPTOP_INFO['serial_number']}")
        print(f"Total Matches: {len(results)}")
        print("="*80)

        for i, result in enumerate(results, 1):
            print(f"\n--- Match #{i} ---")
            print(f"Platform: {result['platform']}")
            print(f"Title: {result['title']}")

            if 'price' in result:
                print(f"Price: {result['price']}")

            if 'location' in result:
                print(f"Location: {result['location']}")

            print(f"URL: {result['url']}")
            print(f"Found at: {result['found_at']}")
            print(f"Search keyword: {result['keyword']}")

        print("\n" + "="*80)
        print("⚠️ ACTION REQUIRED:")
        print("1. Check each URL to verify if it's your laptop")
        print("2. If confirmed, contact the police immediately")
        print("3. Do NOT contact the seller directly")
        print("="*80 + "\n")

    def notify_email(self, results):
        """Send email notification"""
        try:
            sender = EMAIL_SETTINGS['sender_email']
            password = EMAIL_SETTINGS['sender_password']
            recipient = EMAIL_SETTINGS['recipient_email']

            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 ALERT: {len(results)} Potential Matches for Stolen Laptop"
            msg['From'] = sender
            msg['To'] = recipient

            # Create email body
            html = self.create_email_html(results)
            text = self.create_email_text(results)

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            # Send email
            server = smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port'])
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()

            self.console_message("📧 Email notification sent successfully")

        except Exception as e:
            self.console_message(f"❌ Failed to send email: {str(e)}")

    def create_email_text(self, results):
        """Create plain text email body"""
        text = f"""ALERT: Potential Matches Found for Your Stolen Laptop

Laptop Details:
- Model: {LAPTOP_INFO['model']}
- Full Model: {LAPTOP_INFO['full_model']}
- Serial Number: {LAPTOP_INFO['serial_number']}

Total Matches Found: {len(results)}

"""
        for i, result in enumerate(results, 1):
            text += f"\nMatch #{i}:\n"
            text += f"Platform: {result['platform']}\n"
            text += f"Title: {result['title']}\n"
            if 'price' in result:
                text += f"Price: {result['price']}\n"
            if 'location' in result:
                text += f"Location: {result['location']}\n"
            text += f"URL: {result['url']}\n"
            text += f"Found at: {result['found_at']}\n"
            text += "-" * 50 + "\n"

        text += "\nIMPORTANT: Contact police immediately if any listing matches your laptop."

        return text

    def create_email_html(self, results):
        """Create HTML email body"""
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background-color: #ff4444; color: white; padding: 20px; text-align: center; }}
        .laptop-info {{ background-color: #f0f0f0; padding: 15px; margin: 20px 0; }}
        .match {{ border: 2px solid #ff4444; padding: 15px; margin: 15px 0; }}
        .match-title {{ font-size: 18px; font-weight: bold; color: #333; }}
        .warning {{ background-color: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107; }}
        a {{ color: #0066cc; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 ALERT: Potential Matches Found</h1>
        <p>Your stolen laptop may have been listed online</p>
    </div>

    <div class="laptop-info">
        <h3>Stolen Laptop Details:</h3>
        <ul>
            <li><strong>Model:</strong> {LAPTOP_INFO['model']}</li>
            <li><strong>Full Model:</strong> {LAPTOP_INFO['full_model']}</li>
            <li><strong>Serial Number:</strong> {LAPTOP_INFO['serial_number']}</li>
        </ul>
    </div>

    <h2>Total Matches: {len(results)}</h2>
"""

        for i, result in enumerate(results, 1):
            html += f"""
    <div class="match">
        <div class="match-title">Match #{i}: {result['title']}</div>
        <p><strong>Platform:</strong> {result['platform']}</p>
"""
            if 'price' in result:
                html += f"<p><strong>Price:</strong> {result['price']}</p>\n"
            if 'location' in result:
                html += f"<p><strong>Location:</strong> {result['location']}</p>\n"

            html += f"""
        <p><strong>URL:</strong> <a href="{result['url']}" target="_blank">{result['url']}</a></p>
        <p><strong>Found at:</strong> {result['found_at']}</p>
        <p><strong>Search keyword:</strong> {result['keyword']}</p>
    </div>
"""

        html += """
    <div class="warning">
        <h3>⚠️ ACTION REQUIRED:</h3>
        <ol>
            <li>Check each URL to verify if it matches your laptop</li>
            <li>If confirmed, contact the police IMMEDIATELY</li>
            <li>Do NOT contact the seller directly - let the police handle it</li>
            <li>Take screenshots of the listings as evidence</li>
        </ol>
    </div>
</body>
</html>
"""
        return html

    def notify_telegram(self, results):
        """Send Telegram notification"""
        try:
            bot_token = TELEGRAM_SETTINGS['bot_token']
            chat_id = TELEGRAM_SETTINGS['chat_id']

            message = f"🚨 *ALERT: Stolen Laptop Match Found*\n\n"
            message += f"*Laptop:* {LAPTOP_INFO['model']}\n"
            message += f"*Serial:* {LAPTOP_INFO['serial_number']}\n"
            message += f"*Total Matches:* {len(results)}\n\n"

            for i, result in enumerate(results, 1):
                message += f"*Match #{i}:*\n"
                message += f"Platform: {result['platform']}\n"
                message += f"Title: {result['title']}\n"

                if 'location' in result:
                    message += f"Location: {result['location']}\n"

                message += f"[View Listing]({result['url']})\n\n"

                # Telegram has message length limits
                if len(message) > 3000:
                    self.send_telegram_message(bot_token, chat_id, message)
                    message = ""

            if message:
                self.send_telegram_message(bot_token, chat_id, message)

            self.console_message("📱 Telegram notification sent successfully")

        except Exception as e:
            self.console_message(f"❌ Failed to send Telegram: {str(e)}")

    def send_telegram_message(self, bot_token, chat_id, message):
        """Send a single Telegram message"""
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        requests.post(url, data=data)


if __name__ == "__main__":
    # Test notification
    test_results = [
        {
            'platform': 'Test Platform',
            'title': 'Lenovo Thinkpad T14 Gen 3',
            'price': '15,000,000đ',
            'location': 'Pleiku, Gia Lai',
            'url': 'https://example.com/test',
            'keyword': 'Thinkpad T14',
            'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]

    notifier = Notifier()
    notifier.notify(test_results)
