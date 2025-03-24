import json
import time
import os

# ✅ 저장할 폴더 경로
NEWS_DATA_FOLDER = "news_data"
os.makedirs(NEWS_DATA_FOLDER, exist_ok=True)  # 폴더 없으면 생성

# ✅ 종목 리스트 불러오기
with open("data/stock_list.json", "r", encoding="utf-8") as f:
    stock_list = json.load(f)

# ✅ 뉴스 데이터 크롤링 함수 (임시 예제 API, 실제 API로 변경 필요)
def fetch_news(stock_name, stock_code):
    """ 뉴스 데이터를 가져오는 함수 (테스트용) """
    file_path = f"data/post_app.json"  # ✅ 실제 API 연동 시 변경 필요

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # ✅ 뉴스 리스트 추출
        news_items = raw_data.get("Result", [None])[0]
        if not news_items:
            return []  # 뉴스 없음

        # ✅ 뉴스 데이터 정제
        cleaned_news = []
        for item in news_items:
            media_name = item.get("MediaName", "")

            cleaned_news.append({
                "종목명": stock_name,
                "종목코드": stock_code,
                "날짜": item.get("PublishDT", "unknown"),
                "제목": item.get("Title", ""),
                "url": item.get("Url", ""),
                "요약": item.get("Summary", ""),
                "언론사": media_name,
                "감성라벨": "unknown"  # 감성 분석 전처리용
            })

        return cleaned_news
    except Exception as e:
        print(f"⚠️ 오류 발생 ({stock_name}): {e}")
        return []

# ✅ 모든 종목에 대해 뉴스 크롤링 및 저장
for stock in stock_list:
    stock_name = stock["회사명"]
    stock_code = stock["종목코드"]

    print(f"🔍 {stock_name} ({stock_code}) 뉴스 가져오는 중...")

    news_data = fetch_news(stock_name, stock_code)

    if news_data:  # ✅ 뉴스가 있을 때만 저장
        file_path = os.path.join(NEWS_DATA_FOLDER, f"{stock_code}.jsonl")
        with open(file_path, "w", encoding="utf-8") as f:
            for news in news_data:
                f.write(json.dumps(news, ensure_ascii=False) + "\n")

        print(f"✅ 저장 완료: {file_path} (뉴스 {len(news_data)}개)")
    else:
        print(f"⚠️ 뉴스 데이터 없음: {stock_name} ({stock_code})")

    time.sleep(0.5)  # ✅ API 요청 간격 조절 (필요시)

print("🎉 모든 종목 뉴스 데이터 크롤링 완료!")
