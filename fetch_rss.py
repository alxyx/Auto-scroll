import feedparser
from datetime import datetime
import time

# RSS feed URLs
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

# Keywords to filter articles
keywords = [
    "wide bandgap", "SiC", "GaN", "semiconductor",
    "power electronics", "ultra wide bandgap", "WBG", "UWBG", "compound semiconductor"
]

# Safe RSS parsing with retries
def safe_parse(feed_url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return feedparser.parse(feed_url)
        except Exception as e:
            print(f"Error fetching {feed_url} (attempt {attempt + 1}): {e}")
            time.sleep(delay)
    print(f"Failed to fetch {feed_url} after {retries} attempts.")
    return None

# Collect articles
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

# Sort by published date
def parse_date(article):
    try:
        return datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %Z")
    except:
        return datetime.min

articles.sort(key=parse_date, reverse=True)

# Pagination: 10 articles per page
page_size = 10
pages = [articles[i:i + page_size] for i in range(0, len(articles), page_size)]

# Generate HTML with autoscroll + navigation
with open("index.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>WBG Updates</title>")
    f.write("<style>body{font-family:Arial;margin:20px;} h1{color:#333;} hr{border:none;border-top:1px solid #ccc;margin:10px 0;} .nav{margin-top:20px;} button{padding:10px;margin:5px;}</style>")
    f.write("</head><body>")
    f.write("<h1>🌏 Wide Bandgap Semiconductor Updates - APAC Region</h1>")
    f.write(f"<p><em>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</em></p>")

    if not articles:
        f.write("<p>No updates found for the selected keywords.</p>")
        f.write("<h2>Sample WBG Update SiC Expansion in Asia</h2>")
        f.write("<p><strong>Published:</strong> Sample Date</p>")
        f.write("<p>This is a sample article to demonstrate the update feed.</p><hr>")
    else:
        for page_num, page in enumerate(pages, start=1):
            f.write(f"<div class='page' id='page-{page_num}' style='display:none;'>")
            for article in page:
                f.write(f"<h2>{article[{article['title']}</a></h2>")
                f.write(f"<p><strong>Published:</strong> {article['published']}</p>")
                f.write(f"<p>{article['summary']}</p><hr>")
            f.write("</div>")

    # Navigation buttons
    f.write("""
    <div class='nav'>
        <button onclick='prevPage()'>⬅ Prev</button>
        <button onclick='nextPage()'>Next ➡</button>
    </div>
    """)

    # JavaScript for autoscroll + manual navigation
    f.write(f"""
    <script>
    let currentPage = 1;
    const totalPages = {len(pages)};
    function showPage(page) {{
        document.querySelectorAll('.page').forEach(div => div.style.display = 'none');
        document.getElementById('page-' + page).style.display = 'block';
    }}
    function autoScroll() {{
        showPage(currentPage);
        currentPage++;
        if (currentPage > totalPages) currentPage = 1;
    }}
    function nextPage() {{
        currentPage++;
        if (currentPage > totalPages) currentPage = 1;
        showPage(currentPage);
    }}
    function prevPage() {{
        currentPage--;
        if (currentPage < 1) currentPage = totalPages;
        showPage(currentPage);
    }}
    showPage(currentPage);
    setInterval(autoScroll, 10000); // Change page every 10 seconds
    </script>
    """)
    f.write("</body></html>")

