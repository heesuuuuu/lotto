import os
import json
import re
from datetime import datetime

CLEAN_DIR = os.path.join("data", "clean")
os.makedirs(CLEAN_DIR, exist_ok=True)

def parse_money(text):
    """ '10억원', '1천만원' 등 → 숫자 (원 단위) """
    if not text:
        return None
    text = text.replace(",", "").replace(" ", "")
    match = re.match(r"(\d+(?:\.\d+)?)([천억만원]*)", text)
    if not match:
        return None
    num, unit = match.groups()
    num = float(num)
    if "천" in unit:
        num *= 1_0000
    if "억" in unit:
        num *= 100_000_000 # 숫자 구분 용으로 _ 를 사용, 가독성 향상 값에는 영향 없음 
    return int(num)

def parse_count(text):
    """ '4 매', '10 매' → 숫자 """
    if not text:
        return None
    return int(re.sub(r"[^\d]", "", text))

def parse_rate(text):
    """ '74%' → 숫자 74 """
    if not text:
        return None
    return int(re.sub(r"[^\d]", "", text))

def parse_date(text):
    """ '(25-08-22 기준)' → datetime.date """
    if not text:
        return None
    match = re.search(r"(\d{2}-\d{2}-\d{2})", text)
    if match:
        return datetime.strptime(match.group(1), "%y-%m-%d").date()
    return None

def convert_spitto2000_clean_from_data(raw_data, raw_file_path=None):
    """raw JSON 데이터 → clean JSON + 클렌징"""
    clean_data = []
    for item in raw_data:
        texts_clean = []
        for t in item["texts"]:
            texts_clean.append({
                "id": t["id"],
                "rank": t["rank"],
                "rank_date": parse_date(t["rank_date"]),
                "prize_money": parse_money(t["prize_money"]),
                "remaining_count": parse_count(t["remaining_count"])
            })
        clean_data.append({
            "id": item["id"],
            "title": item["title"],
            "texts": texts_clean,
            "crawl_date": datetime.strptime(item["crawl_date"], "%Y-%m-%d").date(),
            "date": parse_date(item.get("date")),
            "rate": parse_rate(item.get("rate"))
        })

    if raw_file_path:
        clean_file_path = raw_file_path.replace("/raw/", "/clean/").replace("_raw_", "_clean_")
    else:
        clean_file_path = os.path.join(CLEAN_DIR, f"speetto2000_clean.json")

    with open(clean_file_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"✅ Clean 저장 및 클렌징 완료: {clean_file_path}")
    return clean_data, clean_file_path
