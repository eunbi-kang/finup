import json
import time
import requests
from bs4 import BeautifulSoup

def get_keyword_idx_from_code(stock_code):
    url = f"https://finance.finup.co.kr/Stock/{stock_code}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            print(f"❌ HTTP Error {response.status_code} for {stock_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        keyword_input = soup.find("input", {"id": "hfStockDetailRelationThemeKeywordIdx"})

        if keyword_input and keyword_input.has_attr("value"):
            return keyword_input["value"]
        else:
            print(f"❌ KeywordIdx not found for {stock_code}")
            return None
    except Exception as e:
        print(f"❌ Exception for {stock_code}: {e}")
        return None

def collect_all_keyword_idx(input_json_path, output_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        stock_list = json.load(f)

    results = []

    for idx, stock in enumerate(stock_list, 1):
        name = stock.get("name")
        code = stock.get("code")
        market = stock.get("market")

        print(f"[{idx}/{len(stock_list)}] ⏳ Processing {name} ({code})...")

        keyword_idx = get_keyword_idx_from_code(code)
        if keyword_idx:
            results.append({
                "KeywordIdx": keyword_idx,
                "name": name,
                "code": code,
                "market": market
            })
            print(f"✅ Collected KeywordIdx: {keyword_idx}")
        else:
            print(f"⚠️ Failed to get KeywordIdx for {name} ({code})")

        time.sleep(0.5)  # 서버에 부담 안 주도록 딜레이

    # 저장
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Done! Saved {len(results)} stocks with KeywordIdx to {output_json_path}")

# 예시 실행
collect_all_keyword_idx("stock_list.json", "stock_with_keyword_idx.json")
