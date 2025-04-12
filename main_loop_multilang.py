import os
import openai
import time
from dotenv import load_dotenv
from generator import generate_blog_content, generate_blog_title
from wordpress_poster import post_to_wordpress
from news_fetcher import fetch_filtered_news
from recycle_generator import load_top_posts, generate_related_article

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

LANGUAGES = {
    "en": {
        "url": os.getenv("WP_URL_EN"),
        "username": os.getenv("WP_USERNAME_EN"),
        "app_password": os.getenv("WP_APP_PASSWORD_EN"),
        "translate_to": None
    },
    "de": {
        "url": os.getenv("WP_URL_DE"),
        "username": os.getenv("WP_USERNAME_DE"),
        "app_password": os.getenv("WP_APP_PASSWORD_DE"),
        "translate_to": "German"
    },
    "fr": {
        "url": os.getenv("WP_URL_FR"),
        "username": os.getenv("WP_USERNAME_FR"),
        "app_password": os.getenv("WP_APP_PASSWORD_FR"),
        "translate_to": "French"
    }
}

def translate_content(text, target_lang):
    prompt = f"""
    Translate the following financial blog article into {target_lang}.
    Use professional tone and retain financial context.

    Article:
    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial translator."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def main():
    print("🌍 다국어 블로그 자동 루프 시작")

    # 🔁 1. Google 뉴스 기반 콘텐츠 생성
    news_items = fetch_filtered_news(language="en", limit=2)

    for summary in news_items:
        print(f"\n📰 Google 뉴스: {summary}")
        title_en = generate_blog_title(summary, language="en")
        content_en = generate_blog_content(summary, language="en")

        for lang_code, config in LANGUAGES.items():
            title = title_en
            content = content_en

            if lang_code != "en":
                title = translate_content(title_en, config["translate_to"])
                content = translate_content(content_en, config["translate_to"])

            post_to_wordpress(
                title,
                content,
                language=lang_code,
                url=config["url"],
                username=config["username"],
                app_password=config["app_password"]
            )
            time.sleep(2)

    # 🔁 2. 인기글 기반 재생성 루프
    print("\n🔁 인기글 리사이클 루프 시작")
    top_posts = load_top_posts()

    for post in top_posts:
        print(f"\n📈 [{post['views']} views] - {post['title']}")
        title_en = f"New Insights: {post['title']}"
        content_en = generate_related_article(post["title"], post["category_id"])

        for lang_code, config in LANGUAGES.items():
            title = title_en
            content = content_en

            if lang_code != "en":
                title = translate_content(title_en, config["translate_to"])
                content = translate_content(content_en, config["translate_to"])

            post_to_wordpress(
                title,
                content,
                language=lang_code,
                url=config["url"],
                username=config["username"],
                app_password=config["app_password"]
            )
            time.sleep(2)

    print("\n✅ 전체 루프 완료 – Google 뉴스 + 인기글 재생성")

if __name__ == "__main__":
    main()
