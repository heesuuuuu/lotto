import os
import json
import asyncio
import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# 저장할 JSON 파일 경로
DATA_PATH = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = os.path.join(DATA_PATH, "raw")
CLEAN_DIR = os.path.join(DATA_PATH, "clean")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)


# 1️⃣ speetto2000 정보 크롤링 함수
async def scrape_spitto2000():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.dhlottery.co.kr/common.do?method=main")

        spitto_id = "speetto2000"
        elems = await page.query_selector_all(f"#{spitto_id}")
        results = []

        for idx, elem in enumerate(elems):
            # 제목
            title_el = await elem.query_selector("strong")
            title = await title_el.text_content() if title_el else None
            
            texts = []
            # 등수 별 정보 
            for i in range(1,4):
                t1_el = await elem.query_selector(f"div:nth-child(4) > a > ul:nth-child(1) > li:nth-child({i}) > span:nth-child(1)")
                rank = await t1_el.text_content() if t1_el else None
                t2_el = await elem.query_selector(f"div:nth-child(4) > a > ul:nth-child(1) > li:nth-child({i}) > span:nth-child(2)")
                rank_date = await t2_el.text_content() if t2_el else None
                t3_el = await elem.query_selector(f"div:nth-child(4) > a > ul:nth-child(2) > li:nth-child({i}) > span")
                prize_money = await t3_el.text_content() if t3_el else None
                t4_el = await elem.query_selector(f"div:nth-child(4) > a > ul:nth-child(3) > li:nth-child({i}) > span")
                remaining_count = await t4_el.text_content() if t4_el else None
                texts.append({
                    "id": f"{spitto_id}_{idx}_{i}",
                    "rank": rank.strip() if rank else None,
                    "rank_date": rank_date.strip() if rank_date else None,
                    "prize_money": prize_money.strip() if prize_money else None,
                    "remaining_count": remaining_count.strip() if remaining_count else None,
                })
            
             
            # 입고율 날짜
            date_el = await elem.query_selector("div:nth-child(6) > a > ul > li:nth-child(1) > span")
            date = await date_el.text_content() if date_el else None
            # 입고율
            rate_el = await elem.query_selector("div:nth-child(6) > a > ul > li:nth-child(2) > span > em")
            rate = await rate_el.text_content() if rate_el else None
            # 크롤링 기준일자
            crawl_date = datetime.datetime.now().strftime("%Y-%m-%d")
            results.append({
                "id": f"{spitto_id}_{idx}",
                "title": title.strip() if title else None,
                "texts": texts,
                "crawl_date": crawl_date,
                "date": date.strip() if date else None,
                "rate": rate.strip() if rate else None + "%"
            })
        await browser.close()

        # JSON 저장
        RAW_FILE_PATH = os.path.join(RAW_DIR, "speetto2000_raw.json")
        with open(RAW_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"크롤링 완료: {len(results)}개의 스피또 정보 수집")
        return results


# def convert_spitto2000_clean(raw_file: str):
#     """raw 데이터를 clean 데이터로 변환"""
#     clean_file = raw_file.replace("/raw/", "/clean/")

#     with open(raw_file, "r", encoding="utf-8") as f:
#         raw_data = json.load(f)

#     clean_data = []
#     for item in raw_data:
#         texts_clean = []
#         for t in item["texts"]:
#             spans = t["raw_texts"]
#             if len(spans) == 4:
#                 texts_clean.append({
#                     "id": t["id"],
#                     "rank": spans[0],
#                     "rank_date": spans[1],
#                     "prize_money": spans[2],
#                     "remaining_count": spans[3],
#                 })
#         clean_data.append({
#             "id": item["id"],
#             "title": item["title"],
#             "texts": texts_clean,
#             "crawl_date": item["crawl_date"]
#         })

#     with open(clean_file, "w", encoding="utf-8") as f:
#         json.dump(clean_data, f, ensure_ascii=False, indent=2)

#     print(f"✅ Clean 저장 완료: {clean_file}")
#     return clean_file


if __name__ == "__main__":
    raw_file = asyncio.run(scrape_spitto2000())
    # clean_file = convert_spitto2000_clean(raw_file)
    # print("완료:", clean_file)
