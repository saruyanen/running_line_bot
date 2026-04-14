import requests
import json
import os

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_USER_ID = os.environ.get("LINE_USER_ID", "")

def main():
    print(f"TOKEN length: {len(LINE_CHANNEL_ACCESS_TOKEN)}")
    print(f"TOKEN first 10 chars: {LINE_CHANNEL_ACCESS_TOKEN[:10]}")
    print(f"USER_ID: {LINE_USER_ID}")
    print(f"USER_ID length: {len(LINE_USER_ID)}")

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": "テスト送信"}]
    }

    print(f"Sending to URL: {url}")
    print(f"Request data: {json.dumps(data, ensure_ascii=False)}")

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Response headers: {dict(response.headers)}")

if __name__ == "__main__":
    main()
