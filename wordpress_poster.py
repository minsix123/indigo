import requests
import csv
from datetime import datetime

# ✅ 키워드 기반 카테고리 분류
CATEGORY_KEYWORDS = {
    "Crypto": ["bitcoin", "ethereum", "crypto", "blockchain", "halving"],
    "US Stocks": ["nasdaq", "apple", "tesla", "s&p", "us stock", "fed", "cpi"],
    "ETF": ["etf", "exchange-traded fund", "dividend", "arkk"],
    "Market News": ["news", "update", "forecast", "analyst", "inflation", "rate hike"],
    "AI Insights": ["ai", "gpt", "machine learning", "chatgpt", "nvidia", "openai"]
}

# ✅ 언어별 카테고리 ID 매핑
CATEGORY_IDS = {
    "en": {
        "Crypto": 2,
        "US Stocks": 3,
        "ETF": 4,
        "Market News": 5,
        "AI Insights": 6
    },
    "de": {
        "Crypto": 3,
        "US Stocks": 4,
        "ETF": 5,
        "Market News": 6,
        "AI Insights": 7
    },
    "fr": {
        "Crypto": 3,
        "US Stocks": 4,
        "ETF": 5,
        "Market News": 6,
        "AI Insights": 7
    }
}

def detect_category(content: str, language: str) -> int:
    content_lower = content.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in content_lower for keyword in keywords):
            return CATEGORY_IDS[language].get(category, 1)
    return 1  # Uncategorized

def log_post(language, title, category_id, post_url):
    log_file = "post_log.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([now, language, title, category_id, post_url])

def post_to_wordpress(title: str, content: str, language: str, url: str, username: str, app_password: str):
    category_id = detect_category(content, language)

    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category_id]
    }

    print(f"📤 [{language.upper()}] 워드프레스 블로그에 업로드 중... (카테고리 ID: {category_id})")

    response = requests.post(
        f"{url}/wp-json/wp/v2/posts",
        auth=(username, app_password),
        headers=headers,
        json=data
    )

    if response.status_code == 201:
        post_url = response.json().get("link")
        print(f"✅ [{language.upper()}] 블로그에 글이 성공적으로 업로드되었습니다!\n🔗 URL: {post_url}")
        log_post(language, title, category_id, post_url)  # ✅ 로그 저장
    else:
        print(f"❌ [{language.upper()}] 업로드 실패! 상태 코드: {response.status_code}")
        print(response.text)
