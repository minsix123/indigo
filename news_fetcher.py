# news_fetcher.py
import feedparser

# ✅ 조회수 유도 핵심 키워드 (언어 확장 가능)
HOT_KEYWORDS = [
    "bitcoin", "ethereum", "etf", "halving",
    "tesla", "apple", "nasdaq", "fed", "cpi", "inflation", "rate hike",
    "nvidia", "openai", "chatgpt", "ai", "earnings", "coinbase"
]

# ✅ Google News RSS 다국어 주소
RSS_FEEDS = {
    "en": "https://news.google.com/rss/search?q=stock+OR+crypto+OR+etf+OR+ai+OR+market&hl=en&gl=US&ceid=US:en",
    "de": "https://news.google.com/rss/search?q=aktien+OR+krypto+OR+etf+OR+markt&hl=de&gl=DE&ceid=DE:de",
    "fr": "https://news.google.com/rss/search?q=bourse+OR+crypto+OR+etf+OR+marché&hl=fr&gl=FR&ceid=FR:fr"
}

def fetch_filtered_news(language="en", limit=10):
    """Google News에서 기사 수집 후, 핫 키워드 기반으로 필터링"""
    feed_url = RSS_FEEDS.get(language, RSS_FEEDS["en"])
    feed = feedparser.parse(feed_url)

    filtered = []
    for entry in feed.entries:
        title = entry.title.lower()
        if any(keyword in title for keyword in HOT_KEYWORDS):
            filtered.append(f"{entry.title} - {entry.link}")
        if len(filtered) >= limit:
            break

    return filtered

# ✅ 테스트 실행
if __name__ == "__main__":
    print("📡 핫 뉴스 수집 결과:")
    for news in fetch_filtered_news("en"):
        print(f"• {news}")
