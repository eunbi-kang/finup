# 종목별 idx를 받아오는 코드 !!! -> 뉴스 수집에 쓸거임 !!
import requests
import re
import json
from tqdm import tqdm
import time


def extract_news_keyword_idx(stock_code):
    """
    종목 코드 기반으로 FinUp 상세 페이지에 접속하여
    뉴스용 keywordIdx를 파싱
    """
    url = f"https://www.finup.co.kr/Stock/{stock_code}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            match = re.search(r"var\s+keywordIdx\s*=\s*'(\d+)'", res.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"❌ [{stock_code}] 에러 발생: {e}")
    return None


def update_stock_list_with_news_idx(input_path, output_path):
    """
    stock_list.json을 읽어 각 종목의 뉴스 keywordIdx를 추출하고
    stock_list_with_newsKeywordIdx.json 파일로 저장
    """
    with open(input_path, "r", encoding="utf-8") as f:
        stock_list = json.load(f)

    for stock in tqdm(stock_list, desc="📡 뉴스용 KeywordIdx 수집 중"):
        code = stock.get("code")
        name = stock.get("name")
        news_idx = extract_news_keyword_idx(code)
        stock["newsKeywordIdx"] = news_idx
        if news_idx:
            print(f"✅ {name} ({code}) → {news_idx}")
        else:
            print(f"❌ {name} ({code}) → 없음")
        time.sleep(0.3)  # 서버 과부하 방지

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stock_list, f, ensure_ascii=False, indent=4)
    print(f"\n📁 저장 완료: {output_path}")


# ✅ 실행
if __name__ == "__main__":
    update_stock_list_with_news_idx(
        "data/stock_list.json",
        "data/stock_list_with_newsKeywordIdx.json"
    )
