import requests
import json
import os
import random
from datetime import date
from bs4 import BeautifulSoup

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_USER_ID = os.environ.get("LINE_USER_ID", "")

# ===== ランニング豆知識（ランダムで1つ選ばれる） =====
TRIVIA_LIST = [
    "💡 豆知識：フルマラソンの距離42.195kmは、1908年ロンドン五輪で王室の都合により決まった距離が起源です。",
    "💡 豆知識：ランニング中は体重の約3倍の衝撃が膝にかかります。クッション性の高いシューズ選びが大切！",
    "💡 豆知識：朝ランは空腹時に行うと脂肪燃焼効果が高まります。ただし長距離は補給してから走りましょう。",
    "💡 豆知識：ランニング後30分以内にタンパク質を摂ると筋肉の回復が早まります。",
    "💡 豆知識：正しいフォームは「背筋を伸ばし、腕を前後に振る」。左右に振ると体力を無駄遣いします。",
    "💡 豆知識：水分補給は喉が渇く前に！目安は20〜30分ごとに150〜200mlです。",
    "💡 豆知識：カーボローディングはレース3日前から。白米・パスタなど糖質を多めに摂るのが効果的。",
    "💡 豆知識：インターバル走は週1〜2回が理想。やりすぎると逆に走力が落ちることも。",
    "💡 豆知識：シューズの寿命は約500〜800km。ソールのクッションが減ったら買い替えのサインです。",
    "💡 豆知識：ランニング後のストレッチは10〜15分かけてゆっくり行うと故障予防になります。",
    "💡 豆知識：心拍数が最大心拍数の60〜70%の「ゾーン2」トレーニングが持久力向上に最も効果的です。",
    "💡 豆知識：雨の日のランニングは路面が滑りやすいので、ペースを10〜15%落として走るのが安全です。",
    "💡 豆知識：ランニングで消費するカロリーの目安は「体重(kg)×距離(km)」。60kgの人が10km走ると約600kcal！",
    "💡 豆知識：サブ4（フルマラソン4時間切り）のペースは1kmあたり約5分41秒。まずは練習でこのペースに慣れよう。",
    "💡 豆知識：レース前夜は消化の良いものを食べ、脂っこいものは避けましょう。胃腸トラブルを防げます。",
]

# ===== Xポスト案テンプレート（ランダムで1つ選ばれる） =====
POST_TEMPLATES = [
    "🏃 今日も走ってきました！\n少しずつでも継続することが大事。\nあなたも一緒に走りませんか？\n#ランニング #マラソン #走ることが好き",
    "🌅 朝ランで一日をスタート！\n走った後の爽快感がたまらない☀️\n今日も一日頑張ろう！\n#朝ラン #ランニング #マラソン",
    "👟 ランニングは裏切らない。\n積み重ねた距離は必ず自信になる💪\n#マラソン #ランニング #自己ベスト更新",
    "🏅 大会に向けて練習中！\n目標タイムに向けて日々積み重ね🔥\n一緒に頑張るランナー仲間募集中！\n#マラソン #ランニング #大会",
    "💨 今日のランニング終了！\nどんなに短くても走った自分を褒めよう✨\n#ランニング #継続は力なり #マラソン",
]


def get_runnet_races():
    """ランネットからエントリー締切間近の大会情報を取得"""
    try:
        url = "https://runnet.jp/racematome/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        races = []
        # ニュース記事のリンクを取得
        articles = soup.select("a[href*='/racematome/']")
        seen = set()
        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if title and href and title not in seen and len(title) > 5:
                seen.add(title)
                full_url = href if href.startswith("http") else "https://runnet.jp" + href
                races.append({"title": title, "url": full_url})
            if len(races) >= 3:
                break

        return races
    except Exception as e:
        print(f"スクレイピングエラー: {e}")
        return []


def build_message(races):
    """LINEに送るメッセージを組み立てる"""
    today = date.today().strftime("%Y年%m月%d日")
    trivia = random.choice(TRIVIA_LIST)
    post = random.choice(POST_TEMPLATES)

    lines = []
    lines.append(f"🏃 おはようございます！")
    lines.append(f"📅 {today}のランニング情報をお届けします\n")

    # ①大会情報
    lines.append("=" * 20)
    lines.append("🏅 大会・エントリー情報")
    lines.append("=" * 20)
    if races:
        for i, race in enumerate(races, 1):
            lines.append(f"{i}. {race['title']}")
            lines.append(f"   🔗 {race['url']}")
    else:
        lines.append("本日は大会情報を取得できませんでした")

    lines.append("")

    # ②豆知識
    lines.append("=" * 20)
    lines.append("📚 今日のランニング豆知識")
    lines.append("=" * 20)
    lines.append(trivia)

    lines.append("")

    # ③Xポスト案
    lines.append("=" * 20)
    lines.append("✏️ 今日のXポスト案")
    lines.append("=" * 20)
    lines.append(post)

    return "\n".join(lines)


def send_line_message(text):
    """LINEにメッセージを送る"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": text}]
    }
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200


def main():
    print("ランネットから大会情報を取得中...")
    races = get_runnet_races()
    print(f"取得した大会数: {len(races)}")

    message = build_message(races)
    print("送信するメッセージ:")
    print(message)

    print("\nLINEに送信中...")
    success = send_line_message(message)
    if success:
        print("✅ 送信成功！")
    else:
        print("❌ 送信失敗")


if __name__ == "__main__":
    main()
