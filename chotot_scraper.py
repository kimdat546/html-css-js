"""
Chotot.com Scraper Module
Searches for laptop listings on Chotot.com marketplace
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from config import SEARCH_KEYWORDS, TARGET_LOCATIONS, LAPTOP_INFO

class ChototScraper:
    def __init__(self):
        self.base_url = "https://www.chotot.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []

    def search_laptops(self, keyword):
        """Search for laptops on Chotot.com with given keyword"""
        print(f"🔍 Searching Chotot.com for: {keyword}")

        try:
            # Chotot.com search URL format
            search_url = f"{self.base_url}/mua-ban-laptop"
            params = {
                'q': keyword,
                'cg': '5010',  # Laptop category
            }

            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)

            if response.status_code == 200:
                # Try to parse JSON API response (Chotot uses API)
                try:
                    # Chotot might return JSON data
                    data = response.json()
                    return self.parse_api_response(data, keyword)
                except:
                    # If not JSON, parse HTML
                    return self.parse_html_response(response.text, keyword)
            else:
                print(f"❌ Failed to fetch Chotot.com (status: {response.status_code})")
                return []

        except Exception as e:
            print(f"❌ Error searching Chotot.com: {str(e)}")
            return []

    def parse_html_response(self, html, keyword):
        """Parse HTML response from Chotot.com"""
        soup = BeautifulSoup(html, 'html.parser')
        listings = []

        # Find all listing cards (this selector may need adjustment based on actual Chotot HTML)
        items = soup.find_all(['div', 'li'], class_=lambda x: x and ('AdItem' in x or 'listing' in x or 'ad-item' in x))

        print(f"   Found {len(items)} potential listings")

        for item in items:
            try:
                listing = self.extract_listing_info(item, keyword)
                if listing:
                    listings.append(listing)
            except Exception as e:
                continue

        return listings

    def parse_api_response(self, data, keyword):
        """Parse JSON API response from Chotot.com"""
        listings = []

        # Chotot API structure (may vary)
        ads = data.get('ads', []) or data.get('data', [])

        for ad in ads:
            try:
                listing = {
                    'platform': 'Chotot.com',
                    'title': ad.get('subject', ''),
                    'price': ad.get('price', 0),
                    'location': ad.get('area_name', '') or ad.get('region_name', ''),
                    'url': f"{self.base_url}/i/{ad.get('ad_id', '')}",
                    'image': ad.get('image', ''),
                    'date': ad.get('date', ''),
                    'seller': ad.get('account_name', 'Unknown'),
                    'keyword': keyword,
                    'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                # Check if listing matches our criteria
                if self.is_potential_match(listing):
                    listings.append(listing)
                    print(f"   ⚠️ POTENTIAL MATCH: {listing['title']} - {listing['location']}")

            except Exception as e:
                continue

        return listings

    def extract_listing_info(self, item, keyword):
        """Extract information from a listing element"""
        # This will need to be adjusted based on actual Chotot HTML structure
        title_elem = item.find(['a', 'h2', 'h3', 'div'], class_=lambda x: x and ('title' in x.lower() if x else False))
        price_elem = item.find(['span', 'div'], class_=lambda x: x and ('price' in x.lower() if x else False))
        location_elem = item.find(['span', 'div'], class_=lambda x: x and ('location' in x.lower() or 'area' in x.lower() if x else False))
        link_elem = item.find('a', href=True)

        if title_elem and link_elem:
            listing = {
                'platform': 'Chotot.com',
                'title': title_elem.get_text(strip=True),
                'price': price_elem.get_text(strip=True) if price_elem else 'N/A',
                'location': location_elem.get_text(strip=True) if location_elem else 'Unknown',
                'url': self.base_url + link_elem['href'] if not link_elem['href'].startswith('http') else link_elem['href'],
                'keyword': keyword,
                'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            if self.is_potential_match(listing):
                return listing

        return None

    def is_potential_match(self, listing):
        """Check if listing is a potential match for stolen laptop"""
        title = listing['title'].lower()
        location = listing['location'].lower()

        # Check if title contains laptop model keywords
        model_match = any(keyword.lower() in title for keyword in ['t14', 'thinkpad', '21ah'])

        # Check if location matches target areas
        location_match = any(loc.lower() in location for loc in TARGET_LOCATIONS)

        # Flag as potential match if either condition is met
        return model_match or location_match

    def search_all_keywords(self):
        """Search for all configured keywords"""
        all_results = []

        print("\n" + "="*60)
        print("🔎 Starting Chotot.com Search")
        print("="*60)

        for keyword in SEARCH_KEYWORDS:
            results = self.search_laptops(keyword)
            all_results.extend(results)
            time.sleep(2)  # Be respectful with rate limiting

        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()

        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        self.results = unique_results
        print(f"\n✅ Chotot.com search complete: {len(unique_results)} unique potential matches found")

        return unique_results

    def save_results(self, filename='chotot_results.json'):
        """Save results to JSON file"""
        if self.results:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"💾 Results saved to {filename}")


if __name__ == "__main__":
    # Test the scraper
    scraper = ChototScraper()
    results = scraper.search_all_keywords()

    if results:
        print("\n" + "="*60)
        print("🚨 POTENTIAL MATCHES FOUND:")
        print("="*60)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   💰 Price: {result['price']}")
            print(f"   📍 Location: {result['location']}")
            print(f"   🔗 URL: {result['url']}")

        scraper.save_results()
    else:
        print("\n✅ No matches found on Chotot.com")
