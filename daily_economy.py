import json
from datetime import datetime
from pathlib import Path

import requests
import yfinance as yf

TELEGRAM_CREDENTIALS = Path.home() / ".openclaw" / "credentials" / "telegram.json"

def load_telegram_config():
    with open(TELEGRAM_CREDENTIALS) as f:
        config = json.load(f)
    return config["bot_token"], config["chat_id"]

TICKERS = {
    "USD/KRW 환율": "KRW=X",
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "금 (Gold)": "GC=F",
    "WTI 유가": "CL=F",
    "비트코인": "BTC-USD",
    "미국 10년물 국채금리": "^TNX",
}


def fetch_market_data():
    results = {}
    symbols = list(TICKERS.values())
    data = yf.download(symbols, period="5d", group_by="ticker", progress=False)

    for name, symbol in TICKERS.items():
        try:
            if len(symbols) == 1:
                ticker_data = data
            else:
                ticker_data = data[symbol]

            ticker_data = ticker_data.dropna(subset=["Close"])
            if len(ticker_data) < 1:
                results[name] = None
                continue

            latest = ticker_data.iloc[-1]
            current_price = float(latest["Close"].iloc[0]) if hasattr(latest["Close"], "iloc") else float(latest["Close"])

            if len(ticker_data) >= 2:
                prev = ticker_data.iloc[-2]
                prev_price = float(prev["Close"].iloc[0]) if hasattr(prev["Close"], "iloc") else float(prev["Close"])
                change = current_price - prev_price
                change_pct = (change / prev_price) * 100
            else:
                change = 0
                change_pct = 0

            results[name] = {
                "price": current_price,
                "change": change,
                "change_pct": change_pct,
            }
        except Exception as e:
            print(f"[{name}] 데이터 수집 실패: {e}")
            results[name] = None

    return results


def format_number(value, decimals=2):
    if abs(value) >= 1000:
        return f"{value:,.{decimals}f}"
    return f"{value:.{decimals}f}"


def build_message(results):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"📊 데일리 경제 브리핑 ({now})", ""]

    section_map = {
        "💱 환율": ["USD/KRW 환율"],
        "📈 미국 증시": ["NASDAQ", "S&P 500"],
        "📉 한국 증시": ["KOSPI", "KOSDAQ"],
        "🏦 원자재 & 금리": ["금 (Gold)", "WTI 유가", "미국 10년물 국채금리"],
        "🪙 암호화폐": ["비트코인"],
    }

    for section_title, keys in section_map.items():
        lines.append(section_title)
        for name in keys:
            data = results.get(name)
            if data is None:
                lines.append(f"  {name}: 데이터 없음")
                continue

            price = data["price"]
            change = data["change"]
            change_pct = data["change_pct"]

            if name == "미국 10년물 국채금리":
                price_str = f"{price:.3f}%"
                change_str = f"{change:+.3f}%p"
            elif name == "USD/KRW 환율":
                price_str = f"{format_number(price, 2)}원"
                change_str = f"{change:+.2f}원"
            elif name == "비트코인":
                price_str = f"${format_number(price, 0)}"
                change_str = f"${change:+,.0f}"
            elif "유가" in name or "Gold" in name:
                price_str = f"${format_number(price, 2)}"
                change_str = f"${change:+.2f}"
            else:
                price_str = format_number(price, 2)
                change_str = f"{change:+.2f}"

            arrow = "🔺" if change > 0 else "🔽" if change < 0 else "➖"
            lines.append(
                f"  {name}: {price_str} {arrow} {change_str} ({change_pct:+.2f}%)"
            )
        lines.append("")

    return "\n".join(lines)


def send_telegram(message):
    bot_token, chat_id = load_telegram_config()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    print("텔레그램 전송 완료!")


def main():
    if not TELEGRAM_CREDENTIALS.exists():
        print(f"오류: 텔레그램 설정 파일이 없습니다: {TELEGRAM_CREDENTIALS}")
        return

    print("경제 데이터 수집 중...")
    results = fetch_market_data()
    message = build_message(results)

    print("\n--- 메시지 미리보기 ---")
    print(message)
    print("--- 끝 ---\n")

    send_telegram(message)


if __name__ == "__main__":
    main()
