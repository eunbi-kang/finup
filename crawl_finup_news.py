import os
import json
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

NEWS_API_URL = "https://apiradar.finup.co.kr/App"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

INPUT_PATH = "./data/stock_list_with_newsKeywordIdx.json"
OUTPUT_DIR = "./news_data"
MAX_WORKERS = 10  # 동시에 실행할 스레드 수
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_news_by_keyword_idx(news_idx):
    all_news = []
    page = 1

    while True:
        body = {
            "ApiID": "ALARM_HISTORY_KEYWORD",
            "ApiGB": "ALARM",
            "KeywordIdx": int(news_idx),
            "PageNo": page,
            "PageSize": 30,
            "TypeFilter": "10"
        }
        try:
            print(f"\n📡 [요청] KeywordIdx={news_idx}, Page={page}")
            res = requests.post(NEWS_API_URL, headers=HEADERS, json=body, timeout=10)
            print(f"🔍 상태코드: {res.status_code}")
            data = res.json()
            items = data.get("Result", [])[0] if isinstance(data.get("Result"), list) else []
            print(f"📄 뉴스 개수: {len(items)}")

            if not items:
                print(f"🛑 더 이상 뉴스 없음 (페이지 {page})")
                break

            all_news.extend(items)
            page += 1
        except Exception as e:
            print(f"❌ [KeywordIdx: {news_idx}] 요청 실패: {e}")
            break

    return all_news


def save_news_jsonl(news_list, path, keyword_idx):
    with open(path, "w", encoding="utf-8") as f:
        for item in news_list:
            if not isinstance(item, dict):
                continue

            title = item.get("Title")
            # content = item.get("Content") or item.get("Summary")
            # if not title or not content:
            #     continue

            record = {
                "keyword": item.get("Keyword", ""),  # ✅ 종목명
                "title": title,
                "summary": item.get("Summary"),
                "date": item.get("PublishDT", "")[:10],
                "url": item.get("Url"),
                "media": item.get("MediaName", ""),    # ✅ 언론사
                "keywordIdx": keyword_idx
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def crawl_single(stock):
    name = stock["name"]
    code = stock["code"]
    news_idx = stock.get("newsKeywordIdx")

    if not news_idx:
        return f"⚠️  {name} ({code}) → newsKeywordIdx 없음"

    print(f"\n🚀 {name} ({code}) 뉴스 수집 시작 → newsKeywordIdx: {news_idx}")
    file_path = os.path.join(OUTPUT_DIR, f"{code}.jsonl")
    news_items = fetch_news_by_keyword_idx(news_idx)

    if news_items:
        save_news_jsonl(news_items, file_path, news_idx)
        return f"✅ {name} ({code}) 뉴스 {len(news_items)}건 저장"
    else:
        return f"⚠️  {name} ({code}) 뉴스 없음"


def crawl_news_all():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        stock_list = json.load(f)

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(crawl_single, stock) for stock in stock_list]
        for future in tqdm(as_completed(futures), total=len(futures), desc="📰 병렬 뉴스 수집 중"):
            result = future.result()
            results.append(result)
            print(result)


if __name__ == "__main__":
    crawl_news_all()
