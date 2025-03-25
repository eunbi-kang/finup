# 테마 idx 를 받아오는 코드 !!!
import json
import re
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 뉴스용 KeywordIdx 추출 함수
def extract_keyword_idx(stock):
    stock_code = stock["code"]
    stock_name = stock["name"]
    url = f"https://finance.finup.co.kr/Stock/{stock_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            match = re.search(r"var\s+keywordIdx\s*=\s*'(\d+)'", res.text)
            if match:
                news_idx = match.group(1)
                return stock_code, stock_name, news_idx
    except Exception as e:
        print(f"❌ [{stock_code}] 오류: {e}")
    return stock_code, stock_name, None


# 병렬 처리하여 전체 stock_list에 newsKeywordIdx 추가
def update_stock_list_with_news_idx_parallel(input_path, output_path, max_workers=10):
    with open(input_path, "r", encoding="utf-8") as f:
        stock_list = json.load(f)

    # 병렬 요청 실행
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(extract_keyword_idx, stock): stock for stock in stock_list}
        for future in tqdm(as_completed(futures), total=len(stock_list), desc="⚡ 뉴스 KeywordIdx 병렬 수집 중"):
            code, name, news_idx = future.result()
            # 해당 stock 업데이트
            for stock in stock_list:
                if stock["code"] == code:
                    stock["newsKeywordIdx"] = news_idx
                    break
            if news_idx:
                print(f"✅ {name} ({code}) → {news_idx}")
            else:
                print(f"❌ {name} ({code}) → 없음")

    # 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stock_list, f, ensure_ascii=False, indent=4)

    print(f"\n📁 저장 완료: {output_path}")


# ✅ 실행
if __name__ == "__main__":
    update_stock_list_with_news_idx_parallel(
        "data/stock_list.json",
        "data/stock_list_with_newsKeywordIdx.json",
        max_workers=10  # 병렬 요청 개수 조절 가능
    )
