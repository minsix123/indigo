import os
import requests
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = {
    "en": {
        "url": os.getenv("WP_URL_EN"),
        "username": os.getenv("WP_USERNAME_EN"),
        "app_password": os.getenv("WP_APP_PASSWORD_EN"),
    },
    "de": {
        "url": os.getenv("WP_URL_DE"),
        "username": os.getenv("WP_USERNAME_DE"),
        "app_password": os.getenv("WP_APP_PASSWORD_DE"),
    },
    "fr": {
        "url": os.getenv("WP_URL_FR"),
        "username": os.getenv("WP_USERNAME_FR"),
        "app_password": os.getenv("WP_APP_PASSWORD_FR"),
    }
}

def fetch_category_ids(language, config):
    url = f"{config['url']}/wp-json/wp/v2/categories"
    auth = (config["username"], config["app_password"])

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        categories = response.json()
        print(f"\n📋 [{language.upper()}] 카테고리 ID 매핑 결과:")
        for cat in categories:
            print(f'"{cat["name"]}": {cat["id"]},')
    else:
        print(f"\n❌ [{language.upper()}] 카테고리 조회 실패: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    for lang, config in LANGUAGES.items():
        fetch_category_ids(lang, config)
