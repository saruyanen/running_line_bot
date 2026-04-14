import requests
import feedparser
from datetime import datetime
import os
import json

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID", "YOUR_USER_ID")

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return response.status_code

def get_marathon_info():
    try:
        feed = feedparser.parse("https://runnet.jp/rss/news.rss")
        articles = []
        for entry in feed.entries[:3]:
            articles.append(entry.get("title", ""))
        if articles:
            return "\n".join([f"・{a}" for a in articles])
    except:
        pass
    return "・最新の大会情報はランネット(runnet.jp)をチェック！"

def get_tips():
    tips = [
        "シューズの寿命は500〜800km。見た目がきれいでもソールが劣化してることがあるよ",
        "30kmの壁対策はエネルギー補給が鍵。レース中はジェルやバナナを忘れずに",
        "練習は週3〜4日が理想。毎日走るより休息日を作る方が体が強くなる",
        "走った後のストレッチが大事。筋肉が温まってる今がチャンス",
        "フルマラソン完走の目安はキロ7分ペース。まずはこれで練習しよう",
        "初心者におすすめ：アシックス GEL-KAYANO、ナイキ ペガサス41",
        "補給食の定番：アミノバイタル、ショッツ、メダリスト",
        "雨の日は帽子で顔をガード、綿素材は避けてポリエステルウェアを選ぼう",
        "体幹トレーニングを週1回取り入れるとフォームが安定してタイムが上がる",
        "ランニング後のビールは格別。でも水分補給を先にしてから",
        "東京マラソン2027のエントリーは例年8月頃スタート",
        "皇居ランは1周約5km。東京ランナーの聖地だよ",
    ]
    day_of_year = datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]

def generate_post(tip):
    templates = [
        "【ランニング豆知識】\n" + tip + "\n\n#ランニング #市民ランナー #マラソン",
        "今日のランニングメモ\n" + tip + "\n\n#ランニング #東京ランナー #マラソン",
        "ランナーのみんなに届け\n" + tip + "\n\n#市民ランナー #ランニング #マラソン",
    ]
    return templates[datetime.now().day % len(templates)]

def main():
    today = datetime.now().strftime("%m月%d日")
    tip = get_tips()
    post = generate_post(tip)
    marathon_info = get_marathon_info()

    message = "今日の投稿ネタ【" + today + "】\n\n"
    message += "【大会情報】\n" + marathon_info + "\n\n"
    message += "【豆知識】\n" + tip + "\n\n"
    message += "【ポスト案】\n" + post

    status = send_line_message(message)
    if status == 200:
        print("LINE送信成功")
    else:
        print("LINE送信失敗: " + str(status))

if __name__ == "__main__":
    main()
