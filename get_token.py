# get_token.py

import requests

# 오빠가 받은 인증 코드
AUTH_CODE = "8kR84Uv5KULTdYc6TmwYZB71hbg6YzSlGSBSWCdvZ6LJVcpoJGsi0QAAAAQKDSBaAAABlh-K5dDkNSpXBP-m7Q"

# 카카오 앱 설정값
REST_API_KEY = "74330233494670d0dea6d507ea2e5745"
REDIRECT_URI = "http://localhost:8080"

# 액세스 토큰 요청
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE
}

response = requests.post(url, data=data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    print("✅ Access Token:", access_token)
    print("♻️ Refresh Token:", refresh_token)
else:
    print("❌ 에러 발생:", response.json())
