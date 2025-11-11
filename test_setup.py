#!/usr/bin/env python3
"""
Test script to verify installation and configuration
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")

    packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('selenium', 'selenium'),
        ('python-dotenv', 'dotenv'),
        ('schedule', 'schedule'),
        ('lxml', 'lxml'),
    ]

    missing = []
    for package_name, import_name in packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - MISSING")
            missing.append(package_name)

    return len(missing) == 0, missing

def test_config():
    """Test if configuration is valid"""
    print("\nTesting configuration...")

    try:
        import config
        print(f"  ✅ Config file loaded")
        print(f"  ℹ️  Laptop model: {config.LAPTOP_INFO['model']}")
        print(f"  ℹ️  Serial: {config.LAPTOP_INFO['serial_number']}")
        print(f"  ℹ️  Search keywords: {len(config.SEARCH_KEYWORDS)} configured")
        print(f"  ℹ️  Target locations: {', '.join(config.TARGET_LOCATIONS[:3])}")
        return True
    except Exception as e:
        print(f"  ❌ Config error: {str(e)}")
        return False

def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")

    modules = [
        'chotot_scraper',
        'facebook_scraper',
        'notifier',
        'monitor'
    ]

    errors = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}.py")
        except Exception as e:
            print(f"  ❌ {module}.py - Error: {str(e)}")
            errors.append(module)

    return len(errors) == 0, errors

def main():
    print("="*60)
    print("🔧 Laptop Monitor - Installation Test")
    print("="*60)
    print()

    all_passed = True

    # Test imports
    imports_ok, missing_packages = test_imports()
    if not imports_ok:
        all_passed = False
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")

    # Test config
    config_ok = test_config()
    if not config_ok:
        all_passed = False

    # Test modules
    modules_ok, error_modules = test_modules()
    if not modules_ok:
        all_passed = False
        print(f"\n⚠️  Module errors: {', '.join(error_modules)}")

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("\nYou're ready to run the monitor!")
        print("\nQuick start:")
        print("  python monitor.py              # Run once")
        print("  python monitor.py --continuous # Keep monitoring")
        print("  ./quick_start.sh               # Interactive menu")
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the errors above before running the monitor.")
        sys.exit(1)

if __name__ == "__main__":
    main()
