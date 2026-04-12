import requests
import feedparser
from datetime import datetime
import os
import json

# ===== 設定 =====
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID", "YOUR_USER_ID")

# ===== LINEにメッセージを送る =====
def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return response.status_code

# ===== ランネットからマラソン大会情報を取得 =====
def get_marathon_info():
    feeds = [
        "https://runnet.jp/rss/news.rss",
    ]
    articles = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", "")
                })
        except:
            pass

    if not articles:
        return "・最新の大会情報はランネット(runnet.jp)をチェック！"

    result = ""
    for a in articles[:3]:
        result += f"・{a['title']}\n  {a['link']}\n"
    return result.strip()

# ===== ギア・豆知識リスト =====
def get_tips():
    tips = [
        "ランニングシューズの寿命は500〜800km！見た目がきれいでもソールが劣化してることがあるよ",
        "フルマラソンの30kmの壁対策はエネルギー補給が鍵！レース中はジェルやバナナを忘れずに！",
        "練習は週3〜4日が理想。毎日走るより休息日を作る方が体が強くなるよ",
        "走る前のストレッチより、走った後のストレッチの方が大事！筋肉が温まってる今がチャンス",
        "フルマラソン完走の目安ペース：キロ7分なら5時間切れる。まずはこのペースで練習しよう！",
        "初心者におすすめシューズ：アシックス GEL-KAYANO・ナイキ ペガサス41・アシックス NOVABLAST5",
        "補給食の定番：アミノバイタル、ショッツ、メダリスト。レース前に必ず練習で試しておこう！",
        "雨の日ランニングのコツ：帽子で顔をガード、綿素材は避けてポリエステルウェアを選ぼう",
        "体幹トレーニングを週1回取り入れるだけでランニングフォームが安定してタイムが上がるよ！",
        "ランニング後のビールは格別！でも水分補給を先にしてから！アルコールは脱水になりやすい",
        "東京マラソン2027のエントリーは例年8月頃スタート。今からONE TOKYOに登録しておこう！",
        "皇居ランは1周約5km。東京のランナーの聖地！週末は多くのランナーで賑わってるよ",
    ]
    day_of_year = datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]

# ===== 投稿用テンプレートを生成 =====
def generate_post_template(tip):
    templates = [
        f"【ランニング豆知識】\n{tip}\n\n#ランニング #市民ランナー #マラソン #初心者ランナー",
        f"今日のランニングメモ\n{tip}\n\n#ランニング #東京ランナー #マラソン",
        f"ランナーのみんなに届け\n{tip}\n\n#市民ランナー #ランニング #マラソン初心者",
    ]
    day = datetime.now().day
    return templates[day % len(templates)]

# ===== メイン処理 =====
def main():
    today = datetime.now().strftime("%m月%d日")
    tip = get_tips()
    post = generate_post_template(tip)
    marathon_info = get_marathon_info()

    message = (
        f"今日の投稿ネタ【{today}】\n\n"
        f"【大会・レース情報】\n{marathon_info}\n\n"
        f"【豆知識・ギア】\n{tip}\n\n"
        f"【Xに使えるポスト案】\n---\n{post}\n---"
    )

    status = send_line_message(message)
    if status == 200:
        print("LINE送信成功！")
    else:
        print(f"LINE送信失敗: {status}")

if __name__ == "__main__":
    main()
