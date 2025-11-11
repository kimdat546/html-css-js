"""
Facebook Scraper Module
Searches for laptop listings on Facebook Marketplace and Groups
Uses Selenium with persistent login session (user logs in manually once)
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

from config import SEARCH_KEYWORDS, TARGET_LOCATIONS, LAPTOP_INFO, BROWSER_PROFILE_PATH, HEADLESS_BROWSER


class FacebookScraper:
    def __init__(self):
        self.driver = None
        self.results = []
        self.profile_path = os.path.abspath(BROWSER_PROFILE_PATH)

    def setup_browser(self):
        """Setup Chrome browser with persistent profile"""
        print("🌐 Setting up browser...")

        chrome_options = Options()

        # Use persistent profile to save login session
        if not os.path.exists(self.profile_path):
            os.makedirs(self.profile_path)

        chrome_options.add_argument(f"user-data-dir={self.profile_path}")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")

        # Language settings for Vietnamese
        chrome_options.add_argument("--lang=vi")

        # Headless mode (run in background)
        if HEADLESS_BROWSER:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Additional options for stability
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Set user agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            print("✅ Browser ready")
            return True
        except Exception as e:
            print(f"❌ Failed to setup browser: {str(e)}")
            return False

    def check_login_status(self):
        """Check if user is logged into Facebook"""
        try:
            self.driver.get("https://www.facebook.com/")
            time.sleep(3)

            # Check if we're on the login page or logged in
            current_url = self.driver.current_url

            # If we see login form, user needs to log in
            if "login" in current_url.lower():
                return False

            # Try to find elements that only appear when logged in
            try:
                # Look for navigation bar or user menu
                self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Account']")
                return True
            except:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "[data-testid='royal_login_button']")
                    return False
                except:
                    # Assume logged in if no login button found
                    return True

        except Exception as e:
            print(f"❌ Error checking login status: {str(e)}")
            return False

    def wait_for_manual_login(self):
        """Wait for user to log in manually"""
        print("\n" + "="*60)
        print("🔐 FACEBOOK LOGIN REQUIRED")
        print("="*60)
        print("Please log into Facebook manually in the browser window.")
        print("After logging in successfully, return here and press ENTER...")
        print("="*60)

        input("\nPress ENTER after you've logged in: ")

        # Verify login
        if self.check_login_status():
            print("✅ Login successful! Session will be saved for future use.")
            return True
        else:
            print("❌ Login verification failed. Please try again.")
            return False

    def search_marketplace(self, keyword):
        """Search Facebook Marketplace for the keyword"""
        print(f"🔍 Searching Facebook Marketplace for: {keyword}")

        try:
            # Facebook Marketplace search URL
            search_url = f"https://www.facebook.com/marketplace/category/laptops/?query={keyword.replace(' ', '%20')}"
            self.driver.get(search_url)
            time.sleep(5)  # Wait for page to load

            # Scroll to load more results
            self.scroll_page(scrolls=3)

            # Extract listings
            listings = self.extract_marketplace_listings(keyword)
            return listings

        except Exception as e:
            print(f"❌ Error searching Marketplace: {str(e)}")
            return []

    def search_facebook_general(self, keyword):
        """Search Facebook generally for posts about the laptop"""
        print(f"🔍 Searching Facebook posts for: {keyword}")

        try:
            # Add location filters to search
            search_terms = [f"{keyword} {loc}" for loc in TARGET_LOCATIONS[:3]]

            all_results = []

            for search_term in search_terms:
                search_url = f"https://www.facebook.com/search/posts/?q={search_term.replace(' ', '%20')}"
                self.driver.get(search_url)
                time.sleep(5)

                # Scroll to load more results
                self.scroll_page(scrolls=2)

                # Extract posts
                posts = self.extract_posts(search_term)
                all_results.extend(posts)

                time.sleep(3)

            return all_results

        except Exception as e:
            print(f"❌ Error searching Facebook posts: {str(e)}")
            return []

    def scroll_page(self, scrolls=3):
        """Scroll page to load dynamic content"""
        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    def extract_marketplace_listings(self, keyword):
        """Extract listing information from Marketplace"""
        listings = []

        try:
            # Find all listing cards (selectors may need adjustment)
            items = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='x9f619']")

            print(f"   Found {len(items)} potential listings")

            for item in items[:20]:  # Limit to first 20 items
                try:
                    # Extract title
                    title_elem = item.find_element(By.TAG_NAME, "span")
                    title = title_elem.text

                    if not title:
                        continue

                    # Extract link
                    link_elem = item.find_element(By.TAG_NAME, "a")
                    url = link_elem.get_attribute('href')

                    # Extract price and location (if available)
                    spans = item.find_elements(By.TAG_NAME, "span")
                    price = "N/A"
                    location = "Unknown"

                    for span in spans:
                        text = span.text
                        if "đ" in text or "₫" in text or text.isdigit():
                            price = text
                        elif any(loc.lower() in text.lower() for loc in TARGET_LOCATIONS):
                            location = text

                    listing = {
                        'platform': 'Facebook Marketplace',
                        'title': title,
                        'price': price,
                        'location': location,
                        'url': url.split('?')[0],  # Remove tracking parameters
                        'keyword': keyword,
                        'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    if self.is_potential_match(listing):
                        listings.append(listing)
                        print(f"   ⚠️ POTENTIAL MATCH: {listing['title']}")

                except:
                    continue

        except Exception as e:
            print(f"   Error extracting listings: {str(e)}")

        return listings

    def extract_posts(self, keyword):
        """Extract posts from Facebook search"""
        posts = []

        try:
            # Find all post containers
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[role='article']")

            print(f"   Found {len(post_elements)} posts")

            for post in post_elements[:15]:  # Limit to first 15 posts
                try:
                    # Extract post text
                    text_elem = post.find_element(By.CSS_SELECTOR, "div[data-ad-comet-preview='message']")
                    text = text_elem.text

                    # Extract link
                    try:
                        link_elem = post.find_element(By.CSS_SELECTOR, "a[href*='/posts/']")
                        url = link_elem.get_attribute('href')
                    except:
                        url = self.driver.current_url

                    listing = {
                        'platform': 'Facebook Post',
                        'title': text[:100] + "..." if len(text) > 100 else text,
                        'full_text': text,
                        'url': url.split('?')[0],
                        'keyword': keyword,
                        'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    if self.is_potential_match(listing):
                        posts.append(listing)
                        print(f"   ⚠️ POTENTIAL MATCH in post")

                except:
                    continue

        except Exception as e:
            print(f"   Error extracting posts: {str(e)}")

        return posts

    def is_potential_match(self, listing):
        """Check if listing is a potential match for stolen laptop"""
        text = (listing.get('title', '') + ' ' + listing.get('location', '') + ' ' + listing.get('full_text', '')).lower()

        # Check for model keywords
        model_match = any(keyword.lower() in text for keyword in ['t14', 'thinkpad', '21ah'])

        # Check for location
        location_match = any(loc.lower() in text for loc in TARGET_LOCATIONS)

        return model_match or location_match

    def search_all_keywords(self):
        """Search for all configured keywords"""
        if not self.setup_browser():
            return []

        # Check login status
        if not self.check_login_status():
            if not self.wait_for_manual_login():
                print("❌ Cannot proceed without login")
                self.close()
                return []

        all_results = []

        print("\n" + "="*60)
        print("🔎 Starting Facebook Search")
        print("="*60)

        # Search Marketplace
        for keyword in SEARCH_KEYWORDS[:3]:  # Limit keywords to avoid too many requests
            results = self.search_marketplace(keyword)
            all_results.extend(results)
            time.sleep(3)

        # Search general Facebook
        for keyword in SEARCH_KEYWORDS[:2]:
            results = self.search_facebook_general(keyword)
            all_results.extend(results)
            time.sleep(3)

        # Remove duplicates
        unique_results = []
        seen_urls = set()

        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        self.results = unique_results
        print(f"\n✅ Facebook search complete: {len(unique_results)} unique potential matches found")

        return unique_results

    def save_results(self, filename='facebook_results.json'):
        """Save results to JSON file"""
        if self.results:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"💾 Results saved to {filename}")

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")


if __name__ == "__main__":
    # Test the scraper
    scraper = FacebookScraper()
    results = scraper.search_all_keywords()

    if results:
        print("\n" + "="*60)
        print("🚨 POTENTIAL MATCHES FOUND:")
        print("="*60)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   📍 Location: {result.get('location', 'N/A')}")
            print(f"   🔗 URL: {result['url']}")

        scraper.save_results()
    else:
        print("\n✅ No matches found on Facebook")

    scraper.close()
