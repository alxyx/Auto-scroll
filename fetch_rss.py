import feedparser
from datetime import datetime
import time

rss_feeds = [
    "https://www.eetasia.com/feed/",
    "https://www.semiconductor-digest.com/feed/",
    "https://www.techinasia.com/feed/",
    "https://www.eetasia.com/tag/wide-bandgap/feed/",
    "https://www.powerelectronicsnews.com/feed/",
    "https://www.eetimes.com/feed/",
    "https://www.electronicsweekly.com/news/feed/",
    "https://www.semiconductoronline.com/rss/summary",
    "https://www.electronicsforu.com/feed",
]

keywords = [
    "wide bandgap", "SiC", "GaN", "semiconductor",
    "power electronics", "ultra wide bandgap", "WBG", "UWBG", "compound semiconductor"
]

def safe_parse(feed_url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return feedparser.parse(feed_url)
        except Exception as e:
            print(f"Error fetching {feed_url} (attempt {attempt + 1}): {e}")
            time.sleep(delay)
    print(f"Failed to fetch {feed_url} after {retries} attempts.")
    return None

articles = []
for feed_url in rss_feeds:
    feed = safe_parse(feed_url)
    if feed is None or not hasattr(feed, 'entries'):
        continue
    for entry in feed.entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        published = entry.get("published", "")
        if any(keyword.lower() in (title + summary).lower() for keyword in keywords):
            articles.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published
            })

def parse_date(article):
    try:
        return datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %Z")
    except:
        return datetime.min

articles.sort(key=parse_date, reverse=True)

with open("WBG_APAC.md", "w", encoding="utf-8") as f:
    f.write("# 🌏 Wide Bandgap Semiconductor Updates - APAC Region\n\n")
    f.write(f"_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_\n\n")

    if not articles:
        f.write("No updates found for the selected keywords.\n\n")
        f.write("## [Sample WBG Update SiC Expansion in Asia\n")
        f.write("**Published:** Sample Date\n\n")
        f.write("This is a sample article to demonstrate the update feed.\n\n")
        f.write("---\n\n")
    else:
        for article in articles:
            f.write(f"## [{article['title']}]({article['link']})\n")
            f.write(f"**Published:** {article['published']}\n\n")
            f.write(f"{article['summary']}\n\n")
            f.write("---\n\n")
