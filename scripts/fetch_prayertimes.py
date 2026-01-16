import requests
from bs4 import BeautifulSoup
from datetime import date
import os
import json

# --- CONFIG ---
BASE_URL = "https://shuroiulamo.tj/ru/namaz/ntime"
OUTPUT_DIR = "output"

# Use GitHub Action environment variables to override if needed
YEAR = os.getenv("NAMAZ_YEAR")
MONTH = os.getenv("NAMAZ_MONTH")

today = date.today()
year = int(YEAR) if YEAR else today.year
month = int(MONTH) if MONTH else today.month

def fetch_month(year, month):
    r = requests.post(BASE_URL, data={
        "fyear": year,
        "fmonth": f"{month:02}",
        "fday": "0"
    }, timeout=20)
    r.raise_for_status()

    # Wrap in fake table
    soup = BeautifulSoup(f"<table>{r.text}</table>", "html.parser")
    rows = soup.find_all("tr")

    days = []
    for tr in rows:
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) != 9:
            continue

        days.append({
            "weekday": tds[0],
            "gregorian": tds[1],
            "hijri": tds[2],
            "fajr": tds[3],
            "dhuhr": tds[4],
            "asr": tds[5],
            "sunset_makruh": tds[6],
            "maghrib": tds[7],
            "isha": tds[8],
        })
    return days

# --- MAIN ---
data = {
    "source": "shuroiulamo.tj",
    "location": "Dushanbe",
    "year": year,
    "month": month,
    "generated_at": today.isoformat(),
    "days": fetch_month(year, month)
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
json_file = f"{OUTPUT_DIR}/{year}-{month:02}.json"

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {json_file}")
