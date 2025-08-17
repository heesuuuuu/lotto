import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 저장할 JSON 파일 경로
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "lotto_data.json"

# 1️⃣ 재사용 가능한 크롤러 함수
async def scrape_main_spitto():
    async with async_playwright() as p:   # Playwright 실행
        browser = await p.chromium.launch(headless=False)  # 크롬 브라우저 띄우기
        page = await browser.new_page()   # 새 페이지 열기
        await page.goto("https://www.dhlottery.co.kr/common.do?method=main")  # URL 접속

        print("페이지 타이틀:", await page.title())  # 타이틀 출력 (테스트용)

        await browser.close()  # 브라우저 닫기

if __name__ == "__main__":
    data = asyncio.run(scrape_main_spitto())
    print("메인 페이지 즉석식 인쇄복권 크롤링 완료 ✅")
    print(data)