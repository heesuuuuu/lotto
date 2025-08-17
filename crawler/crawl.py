import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 저장할 JSON 파일 경로
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "lotto_data.json"

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
            # 텍스트1,2,3
            t1_el = await elem.query_selector("div:nth-child(4) > a > ul:nth-child(1)")
            text1 = await t1_el.text_content() if t1_el else None
            t2_el = await elem.query_selector("div:nth-child(4) > a > ul:nth-child(2)")
            text2 = await t2_el.text_content() if t2_el else None
            t3_el = await elem.query_selector("div:nth-child(4) > a > ul:nth-child(3)")
            text3 = await t3_el.text_content() if t3_el else None
            # 입고율 날짜
            date_el = await elem.query_selector("div:nth-child(6) > a > ul > li:nth-child(1) > span")
            date = await date_el.text_content() if date_el else None
            # 입고율
            rate_el = await elem.query_selector("div:nth-child(6) > a > ul > li:nth-child(2) > span > em")
            rate = await rate_el.text_content() if rate_el else None
            results.append({
                "id": f"{spitto_id}_{idx}",
                "title": title.strip() if title else None,
                "text1": text1.strip() if text1 else None,
                "text2": text2.strip() if text2 else None,
                "text3": text3.strip() if text3 else None,
                "date": date.strip() if date else None,
                "rate": rate.strip() if rate else None
            })
        await browser.close()

        # JSON 저장
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"크롤링 완료: {len(results)}개의 스피또 정보 수집")
        return results

if __name__ == "__main__":
    data = asyncio.run(scrape_spitto2000())
    print("즉석식 인쇄복권 speetto2000 크롤링 완료 ✅")
    print(data[0])