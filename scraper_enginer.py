import requests
from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime
import os

# --- CONFIGURATION: Add all 30 pages here ---
# 'container': the wrapper for one news item
# 'title_tag': the tag inside that wrapper for the headline
SOURCES = [
   {
    "id": "adaderana_tamil",
    "name": "Ada Derana Tamil",
    "url": "https://tamil.adaderana.lk/categories/breakingnews",
    "container": "div.mt-4",
    "title_tag": "p.font-medium",
    "base_url": "https://tamil.adaderana.lk"
}
    # {
    #     "id": "lankatruth_politics",
    #     "name": "Lanka Truth Politics",
    #     "url": "https://lankatruth.com/si/?cat=3",
    #     "container": "article",
    #     "title_tag": "h3"
    # },
    # {
    #     "id": "dinamina_local",
    #     "name": "Dinamina Local",
    #     "url": "https://www.dinamina.lk/category/local/",
    #     "container": "div.td-block-span6",
    #     "title_tag": "h3"
    # }
    # Add your remaining 27 pages here in the same format...
]

def generate_rss(source):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"Scraping {source['name']}...")
        response = requests.get(source['url'], headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = []
        blocks = soup.select(source['container'])

        for block in blocks[:15]: # Get top 15 news items
            title_el = block.select_one(source['title_tag'])
            link_el = block.find('a')
            
            if title_el and link_el:
                link = link_el['href']
                # Handle relative URLs (e.g., /news/123 -> https://site.com/news/123)
                if not link.startswith('http'):
                    from urllib.parse import urljoin
                    link = urljoin(source['url'], link)

                items.append(PyRSS2Gen.RSSItem(
                    title = title_el.get_text().strip(),
                    link = link,
                    description = source['name'], # Or scrape a summary if needed
                    pubDate = datetime.datetime.now()
                ))

        rss = PyRSS2Gen.RSS2(
            title = source['name'],
            link = source['url'],
            description = f"Latest news from {source['name']}",
            lastBuildDate = datetime.datetime.now(),
            items = items 
        )

        # Save to a dedicated folder
        os.makedirs('feeds', exist_ok=True)
        rss.write_xml(open(f"feeds/{source['id']}.xml", "w", encoding='utf-8'))
        
    except Exception as e:
        print(f"Error scraping {source['name']}: {e}")

if __name__ == "__main__":
    for s in SOURCES:
        generate_rss(s)