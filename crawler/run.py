import asyncio
from scraper import scrape_spitto2000
from cleaner import convert_spitto2000_clean_from_data

async def main():
    raw_data, raw_file_path = await scrape_spitto2000()
    clean_data, clean_file_path = convert_spitto2000_clean_from_data(raw_data, raw_file_path)
    print("🎉 전체 완료:", clean_file_path)

if __name__ == "__main__":
    asyncio.run(main())
