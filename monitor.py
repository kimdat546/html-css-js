#!/usr/bin/env python3
"""
Laptop Theft Monitor - Main Script
Monitors marketplaces for stolen laptop listings

Usage:
    python monitor.py              # Run once
    python monitor.py --continuous # Run continuously with scheduled checks
    python monitor.py --help       # Show help
"""

import argparse
import schedule
import time
import json
import os
from datetime import datetime

from chotot_scraper import ChototScraper
from facebook_scraper import FacebookScraper
from notifier import Notifier
from config import CHECK_INTERVAL_HOURS, LAPTOP_INFO


class LaptopMonitor:
    def __init__(self):
        self.chotot_scraper = ChototScraper()
        self.facebook_scraper = None  # Initialize only when needed
        self.notifier = Notifier()
        self.results_file = 'all_results.json'
        self.seen_urls = self.load_seen_urls()

    def load_seen_urls(self):
        """Load previously seen URLs to avoid duplicate notifications"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(result['url'] for result in data)
            except:
                return set()
        return set()

    def save_results(self, results):
        """Save all results to file"""
        all_results = []

        # Load existing results
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
            except:
                all_results = []

        # Add new results
        all_results.extend(results)

        # Save back
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

    def check_chotot(self):
        """Check Chotot.com for listings"""
        print("\n" + "="*80)
        print(f"🔍 CHECKING CHOTOT.COM - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        results = self.chotot_scraper.search_all_keywords()

        # Filter out already seen URLs
        new_results = [r for r in results if r['url'] not in self.seen_urls]

        if new_results:
            print(f"\n🚨 Found {len(new_results)} NEW listings on Chotot.com")
            self.seen_urls.update(r['url'] for r in new_results)
            self.chotot_scraper.save_results('chotot_results.json')
        else:
            print("✅ No new listings on Chotot.com")

        return new_results

    def check_facebook(self):
        """Check Facebook for listings"""
        print("\n" + "="*80)
        print(f"🔍 CHECKING FACEBOOK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        if self.facebook_scraper is None:
            self.facebook_scraper = FacebookScraper()

        results = self.facebook_scraper.search_all_keywords()

        # Filter out already seen URLs
        new_results = [r for r in results if r['url'] not in self.seen_urls]

        if new_results:
            print(f"\n🚨 Found {len(new_results)} NEW listings on Facebook")
            self.seen_urls.update(r['url'] for r in new_results)
            self.facebook_scraper.save_results('facebook_results.json')
        else:
            print("✅ No new listings on Facebook")

        return new_results

    def run_check(self):
        """Run a complete check cycle"""
        print("\n" + "="*80)
        print("🚀 STARTING LAPTOP MONITOR")
        print("="*80)
        print(f"Laptop: {LAPTOP_INFO['model']}")
        print(f"Serial: {LAPTOP_INFO['serial_number']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        all_new_results = []

        # Check Chotot.com
        try:
            chotot_results = self.check_chotot()
            all_new_results.extend(chotot_results)
        except Exception as e:
            print(f"❌ Error checking Chotot.com: {str(e)}")

        # Check Facebook
        try:
            facebook_results = self.check_facebook()
            all_new_results.extend(facebook_results)
        except Exception as e:
            print(f"❌ Error checking Facebook: {str(e)}")

        # Send notifications for new results
        if all_new_results:
            self.save_results(all_new_results)
            self.notifier.notify(all_new_results)

            # Generate HTML report
            self.generate_html_report(all_new_results)
        else:
            print("\n" + "="*80)
            print("✅ CHECK COMPLETE - No new matches found")
            print("="*80)

        # Close Facebook browser if opened
        if self.facebook_scraper:
            self.facebook_scraper.close()
            self.facebook_scraper = None

        print(f"\n⏰ Next check in {CHECK_INTERVAL_HOURS} hour(s)")

    def generate_html_report(self, results):
        """Generate an HTML report of findings"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Laptop Monitor - Results</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #d32f2f;
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .laptop-info {{
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .result {{
            background-color: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            border-left: 5px solid #d32f2f;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .result-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .result-meta {{
            color: #666;
            margin: 5px 0;
        }}
        .result-url {{
            margin-top: 15px;
        }}
        .result-url a {{
            background-color: #d32f2f;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
        }}
        .result-url a:hover {{
            background-color: #b71c1c;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 Laptop Theft Monitor - Alert Report</h1>
        <p>Potential matches found for stolen laptop</p>
    </div>

    <div class="laptop-info">
        <h2>Stolen Laptop Information</h2>
        <p><strong>Model:</strong> {LAPTOP_INFO['model']}</p>
        <p><strong>Full Model Number:</strong> {LAPTOP_INFO['full_model']}</p>
        <p><strong>Serial Number:</strong> {LAPTOP_INFO['serial_number']}</p>
        <p><strong>Operating System:</strong> {LAPTOP_INFO['os']}</p>
    </div>

    <div class="warning">
        <h3>⚠️ IMPORTANT INSTRUCTIONS:</h3>
        <ol>
            <li><strong>Review each listing carefully</strong> - Check photos, descriptions, and details</li>
            <li><strong>Do NOT contact sellers directly</strong> - This could alert the thief</li>
            <li><strong>Contact police immediately</strong> if you find a match</li>
            <li><strong>Save evidence</strong> - Take screenshots of the listing</li>
            <li><strong>Share this report</strong> with law enforcement</li>
        </ol>
    </div>

    <h2>Found {len(results)} Potential Match(es)</h2>
"""

        for i, result in enumerate(results, 1):
            html += f"""
    <div class="result">
        <div class="result-title">{i}. {result['title']}</div>
        <div class="result-meta"><strong>Platform:</strong> {result['platform']}</div>
"""
            if 'price' in result:
                html += f"<div class='result-meta'><strong>Price:</strong> {result['price']}</div>\n"
            if 'location' in result:
                html += f"<div class='result-meta'><strong>Location:</strong> {result['location']}</div>\n"

            html += f"""
        <div class="result-meta"><strong>Found at:</strong> {result['found_at']}</div>
        <div class="result-meta"><strong>Search keyword:</strong> {result['keyword']}</div>
        <div class="result-url">
            <a href="{result['url']}" target="_blank">View Listing →</a>
        </div>
    </div>
"""

        html += f"""
    <div class="timestamp">
        Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
"""

        report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n📄 HTML report generated: {report_file}")


def main():
    parser = argparse.ArgumentParser(description='Laptop Theft Monitor')
    parser.add_argument('--continuous', action='store_true',
                        help='Run continuously with scheduled checks')
    parser.add_argument('--chotot-only', action='store_true',
                        help='Check only Chotot.com')
    parser.add_argument('--facebook-only', action='store_true',
                        help='Check only Facebook')

    args = parser.parse_args()

    monitor = LaptopMonitor()

    if args.chotot_only:
        results = monitor.check_chotot()
        if results:
            monitor.save_results(results)
            monitor.notifier.notify(results)
            monitor.generate_html_report(results)
    elif args.facebook_only:
        results = monitor.check_facebook()
        if results:
            monitor.save_results(results)
            monitor.notifier.notify(results)
            monitor.generate_html_report(results)
        if monitor.facebook_scraper:
            monitor.facebook_scraper.close()
    elif args.continuous:
        print("🔄 Starting continuous monitoring mode")
        print(f"⏰ Checks will run every {CHECK_INTERVAL_HOURS} hour(s)")
        print("Press Ctrl+C to stop\n")

        # Run first check immediately
        monitor.run_check()

        # Schedule periodic checks
        schedule.every(CHECK_INTERVAL_HOURS).hours.do(monitor.run_check)

        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute if a job should run
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped by user")
            if monitor.facebook_scraper:
                monitor.facebook_scraper.close()
    else:
        # Run once
        monitor.run_check()


if __name__ == "__main__":
    main()
