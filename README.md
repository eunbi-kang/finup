
# 📊 FinUp 종목 뉴스 수집기

**AI 기반 주식 뉴스 감성분석 시스템 구축을 위한 종목/뉴스 크롤링 파이프라인**

---

## 📁 프로젝트 구조
```bash
🗂finup/
├── 📁data/
│ ├── stock_list.json                     # 전체 종목 기본 정보 (회사명, 종목코드, 시장구분)
│ ├── stock_list_with_keyword.json        # ✅ keywordIdx 포함된 종목 리스트
│ ├── stock_list_with_newsKeywordIdx.json # ✅ newsKeywordIdx 포함된 종목 리스트
│ └── 📁news_data/                         # 🗂 종목별 뉴스 데이터를 .jsonl로 저장
├── getAllStockCodes.py                   # 종목 기본 정보 수집 (KOSPI, KOSDAQ, KONEX)
├── add_keyword_idx.py                    # 종목별 테마 기반 keywordIdx 수집
├── add_news_keyword_idx.py               # 종목별 뉴스용 keywordIdx(newsKeywordIdx) 수집
├── crawl_finup_news.py                   # ✅ keywordIdx 기반 뉴스 수집 및 저장
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ✅ 설치 및 실행 방법

1. **의존 패키지 설치**
```bash
pip install -r requirements.txt
```
- 예시 패키지: requests, beautifulsoup4, pandas, tqdm

## 🚀 실행순서
```bash
# 1단계: 전체 종목 수집
python getAllStockCodes.py

# 2단계: keywordIdx 추가 (테마 기반)
python add_keyword_idx.py

# 2-1단계: newsKeywordIdx 추가 (실제 뉴스용 키워드 ID)
python add_news_keyword_idx.py

# 3단계: 뉴스 수집 (jsonl 형태로 저장)
python crawl_finup_news.py
```

---

## 📌 주요 설명

### 📄 파일명별 역할

| 파일명 | 역할 |
|--------|------|
| `getAllStockCodes.py` | KRX 공시에서 전체 종목(회사명, 코드, 시장구분) 수집 |
| `add_keyword_idx.py` | 종목별 `keywordIdx` 수집 (테마 기반 뉴스 추출용) |
| `add_news_keyword_idx.py` | 종목별 실제 뉴스용 `newsKeywordIdx` 수집 |
| `crawl_finup_news.py` | ✅ 병렬 수집 방식으로 `newsKeywordIdx` 기반 뉴스 수집 및 `.jsonl` 저장 |
| `.jsonl 포맷` | 학습 모델 학습을 위한 1줄 1뉴스 구조 |

---

## 📝 참고

- `news_data/` 폴더 안에는 각 종목별로 수집한 뉴스가 `000660.jsonl`, `005930.jsonl` 등의 파일로 저장됩니다.
- 각 `.jsonl` 파일은 다음과 같은 형식입니다:

```json
{
  "keyword": "삼성전자",               // 종목명
  "title": "삼성전자, 반도체 투자 확대",
  "summary": "삼성전자가 반도체 시설 투자 확대에 나섰다...",
  "date": "2024-03-24",
  "url": "https://www.example.com/news/123456",
  "media": "연합뉴스",                // ✅ 언론사 정보 (Media 기반)
  "keywordIdx": "123456"
}
```

- `.jsonl`은 **1줄 = 1뉴스** 형태로 구성되어 있어, 감성 분석, 벡터 임베딩, MongoDB 저장 등 다양한 처리에 활용됩니다.

---

## 👩‍💻 Contributors

| 이름   | 역할 |
|--------|------|
| **인권** | AI 모델 개발 및 종목 분석 시스템 구축을 담당. <br>뉴스 데이터를 활용한 감성 분석 모델을 설계하고, BERT 기반 문장 임베딩 및 벡터 유사도 계산을 통해 종목별 투자 리스크 예측 시스템을 개발 중. <br>Transformer 계열 모델을 활용한 고도화된 학습 파이프라인을 구성하며, 추후 유사 종목 추천 및 투자 판단 보조 시스템으로 확장할 계획. <br>PyTorch 기반 학습 및 MongoDB 벡터 저장 연동도 병행하고 있음. |
| **재윤** | AI 기반 종목 분석 API 및 백엔드 시스템 개발을 담당. <br>Spring Boot 기반으로 종목별 분석 데이터를 제공하는 API를 설계하고 있으며, 감성 분석·유사 종목 분석 결과를 프론트엔드에 전달하는 구조를 구축 중. <br>AI 예측 결과를 실시간으로 제공하기 위한 백엔드 인프라 설계와 향후 자동 추천 시스템을 위한 API 확장성 확보에도 주력하고 있음. |
| **홍덕** | 프론트엔드 및 UI/UX 설계, 데이터 시각화 구현을 담당. <br>React 기반의 웹 애플리케이션에서 카카오톡 스타일 챗봇 UI를 구현하고, 주식 뉴스 및 추천 결과를 직관적으로 표현하는 레이아웃을 설계. <br>사용자 친화적인 대화 흐름과 반응형 디자인을 통해 PC와 모바일에서 모두 원활한 사용이 가능하도록 구조화하고 있음. <br>D3.js, Chart.js 등의 라이브러리를 활용하여 뉴스 감성 분석 및 종목 관련 데이터를 시각적으로 표현하는 작업도 함께 수행 중. |
| **은비** | 데이터 수집, 크롤링 및 초기 백엔드 파이프라인 구축, 데이터 시각화 지원을 담당. <br>KRX 공시 정보 및 FinUp API를 활용해 종목 데이터를 자동으로 수집하고, `newsKeywordIdx` 기반 뉴스 데이터를 `.jsonl` 형식으로 저장하는 크롤링 파이프라인을 구축함. <br>**실제 뉴스 페이지에서 `newsKeywordIdx` 값을 정규식 기반으로 파싱하는 기능까지 구현하여 크롤링 정확도를 높임.** <br>수집된 데이터를 기반으로 뉴스 키워드, 종목 연관도, 테마별 통계 등의 백엔드 기반 시각화 데이터 구조를 설계 및 지원하고 있음. |

---

## 📅 진행 상황

- ✅ 종목 리스트 수집 완료  
- ✅ `keywordIdx` 수집 완료 (테마 기준)  
- ✅ `newsKeywordIdx` 수집 완료 (실제 뉴스 페이지 기준)  
- ✅ 뉴스 크롤링 완료 (`.jsonl` 형태로 저장 중, 병렬 수집 & 언론사 필드 포함)  
- 🔜 감성 분석 → 모델 학습 → MongoDB 연동
