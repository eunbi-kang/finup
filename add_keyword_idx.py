import json
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_keyword_idx_from_code(stock_code):
    url = f"https://finance.finup.co.kr/Stock/{stock_code}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        keyword_input = soup.find("input", {"id": "hfStockDetailRelationThemeKeywordIdx"})

        if keyword_input and keyword_input.has_attr("value"):
            return keyword_input["value"]
        else:
            return None
    except Exception as e:
        print(f"❌ 에러 ({stock_code}): {e}")
        return None

def attach_keyword_idx(stock_list_path='data/stock_list.json', save_path='data/stock_list_with_keyword.json'):
    with open(stock_list_path, 'r', encoding='utf-8') as f:
        stock_list = json.load(f)

    updated_list = []
    for stock in tqdm(stock_list, desc="🔍 KeywordIdx 수집 중"):
        code = stock.get('code')
        name = stock.get('name')
        keyword_idx = get_keyword_idx_from_code(code)
        stock['keywordIdx'] = keyword_idx

        # ✅ keywordIdx 확인용 출력
        print(f"✔️ {name} ({code}) → KeywordIdx: {keyword_idx}")

        updated_list.append(stock)

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 저장 완료: {save_path}")

if __name__ == "__main__":
    attach_keyword_idx()
