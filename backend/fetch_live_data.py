"""
Fetches live daily mandi (market) price data from the data.gov.in Agmarknet API
and saves it in the same shape your existing pipeline already expects:
    Commodity, Mandi, Date, Price, Arrival

Run this on a schedule (daily) or on-demand before a prediction is made.
"""

import requests
import pandas as pd
from datetime import datetime
from config import API_KEY, RESOURCE_ID, COMMODITY_FILTER, STATE_FILTER

BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

OUTPUT_FILE = "data/live_mandi_data.csv"


def fetch_live_data(limit=100, offset=0):
    """Pull one page of records from the API."""
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": limit,
        "offset": offset,
    }

    if COMMODITY_FILTER:
        params["filters[Commodity]"] = COMMODITY_FILTER
    if STATE_FILTER:
        params["filters[State]"] = STATE_FILTER

    # This dataset goes back to 2014 and isn't sorted by default — without this,
    # you'll pull old records instead of recent ones. Sort newest first.
    params["sort[Arrival_Date]"] = "desc"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    }

    response = requests.get(BASE_URL, params=params, headers=headers, timeout=60)
    response.raise_for_status()
    payload = response.json()

    return payload.get("records", [])


def fetch_all(max_records=5000):
    """Paginate through the API until we run out of records or hit max_records."""
    all_records = []
    offset = 0
    page_size = 100

    while len(all_records) < max_records:
        records = fetch_live_data(limit=page_size, offset=offset)
        if not records:
            break
        all_records.extend(records)
        offset += page_size

    return all_records


def normalize(records):
    """Map the API's raw field names onto the columns your project already uses."""
    df = pd.DataFrame(records)

    if df.empty:
        return df

    # Confirmed via direct API test — these are the actual field names returned.
    rename_map = {
        "Market": "Mandi",
        "Arrival_Date": "Date",
        "Modal_Price": "Price",   # modal price = the representative daily price
    }
    df = df.rename(columns=rename_map)

    keep_cols = [c for c in
                 ["Commodity", "Mandi", "State", "District", "Date", "Price", "Min_Price", "Max_Price"]
                 if c in df.columns]
    df = df[keep_cols]

    for col in ["Price", "Min_Price", "Max_Price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

    df = df.dropna(subset=["Price"])

    return df


def main():
    print(f"Fetching live mandi data... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    records = fetch_all()
    print(f"Pulled {len(records)} raw records")

    df = normalize(records)
    if df.empty:
        print("No usable records returned — check your API key / resource_id / filters.")
        return

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} cleaned rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()