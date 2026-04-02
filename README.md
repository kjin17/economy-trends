# economy-trends

매일 평일 오전 10시에 주요 글로벌/국내 경제 지표를 자동으로 수집하고 텔레그램으로 리포트를 전송하는 자동화 스크립트입니다.

## 구성 파일

| 파일 | 설명 |
|---|---|
| `daily_economy.py` | 핵심 스크립트 — 데이터 수집, 메시지 포맷, 텔레그램 전송 |
| `economy_trends.py` | LaunchAgent 진입점 — `daily_economy.main()` 래퍼 |
| `requirements.txt` | Python 의존성 목록 |

## 수집 지표

| 카테고리 | 지표 |
|---|---|
| 💱 환율 | USD/KRW |
| 📈 미국 증시 | NASDAQ, S&P 500 |
| 📉 한국 증시 | KOSPI, KOSDAQ |
| 🏦 원자재 & 금리 | 금(Gold), WTI 유가, 미국 10년물 국채금리 |
| 🪙 암호화폐 | 비트코인 |

데이터 소스: [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance API)

## 텔레그램 리포트 예시

```
📊 데일리 경제 브리핑 (2026-04-02 10:00)

💱 환율
  USD/KRW 환율: 1,360.25원 🔺 +3.50원 (+0.26%)

📈 미국 증시
  NASDAQ: 17,845.23 🔻 -120.45 (-0.67%)
  S&P 500: 5,243.77 🔻 -18.32 (-0.35%)

📉 한국 증시
  KOSPI: 2,678.50 🔺 +12.30 (+0.46%)
  KOSDAQ: 875.40 🔺 +5.20 (+0.60%)

🏦 원자재 & 금리
  금 (Gold): $3,120.50 🔺 +12.50 (+0.40%)
  WTI 유가: $71.20 🔻 -0.80 (-1.11%)
  미국 10년물 국채금리: 4.312% 🔺 +0.015%p

🪙 암호화폐
  비트코인: $83,500 🔺 +1,200 (+1.46%)
```

## 설치 및 설정

### 1. 의존성 설치

```bash
pip3 install -r requirements.txt
```

### 2. 텔레그램 크리덴셜 설정

아래 경로에 JSON 파일을 생성합니다:

```
~/.openclaw/credentials/telegram.json
```

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "chat_id": "YOUR_CHAT_ID"
}
```

### 3. 수동 실행 (테스트)

```bash
python3 daily_economy.py
```

## 스케줄 자동화 (macOS LaunchAgent)

평일 오전 10시에 자동 실행되도록 LaunchAgent로 등록합니다.

Plist 파일 위치: `~/Library/LaunchAgents/ai.openclaw.economy.trends.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.economy.trends</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/projects/economy-trends/economy_trends.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Weekday</key><integer>2</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>3</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>4</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>5</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>6</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
    </array>
    <key>StandardOutPath</key>
    <string>/tmp/ai.openclaw.economy.trends.out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ai.openclaw.economy.trends.err.log</string>
</dict>
</plist>
```

LaunchAgent 등록:

```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.economy.trends.plist
```

## 로그 확인

```bash
# 실행 로그
tail -f /tmp/ai.openclaw.economy.trends.out.log

# 에러 로그
tail -f /tmp/ai.openclaw.economy.trends.err.log
```

## 프로젝트 구조

```
economy-trends/
├── daily_economy.py      # 핵심 스크립트
├── economy_trends.py     # LaunchAgent 진입점 (래퍼)
├── requirements.txt      # Python 의존성
└── README.md
```
