#!/bin/bash

echo "=================================================="
echo "  🚨 Laptop Theft Monitor - Quick Start"
echo "=================================================="
echo ""
echo "Laptop: Lenovo Thinkpad T14 GEN 3"
echo "Serial: PF3YR90J"
echo "Target: Gia Lai, Kontum, Dak Lak"
echo ""
echo "=================================================="
echo ""
echo "What would you like to do?"
echo ""
echo "1) Run a quick check (once)"
echo "2) Start continuous monitoring (every 2 hours)"
echo "3) Check Chotot.com only"
echo "4) Check Facebook only"
echo "5) Install/Update dependencies"
echo "6) View latest results"
echo "7) Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        echo "🔍 Running quick check..."
        python3 monitor.py
        ;;
    2)
        echo ""
        echo "🔄 Starting continuous monitoring..."
        echo "Press Ctrl+C to stop"
        python3 monitor.py --continuous
        ;;
    3)
        echo ""
        echo "🔍 Checking Chotot.com only..."
        python3 monitor.py --chotot-only
        ;;
    4)
        echo ""
        echo "🔍 Checking Facebook only..."
        python3 monitor.py --facebook-only
        ;;
    5)
        echo ""
        echo "📦 Installing dependencies..."
        pip3 install -r requirements.txt
        echo "✅ Done!"
        ;;
    6)
        echo ""
        echo "📊 Latest Results:"
        echo ""
        if [ -f "all_results.json" ]; then
            python3 -m json.tool all_results.json | head -50
            echo ""
            echo "💡 Open the latest HTML report for better viewing"
            ls -t report_*.html 2>/dev/null | head -1
        else
            echo "No results found yet. Run a check first."
        fi
        ;;
    7)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
