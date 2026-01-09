import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

MOVIE_IDS = [
    "tt0111161",
    "tt0068646",
    "tt0468569",
    "tt0109830",
]

def label_from_rating(r):
    if r >= 7:
        return 1
    if r <= 4:
        return 0
    return None

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
})

rows = []

for movie_id in MOVIE_IDS:
    print(f"\nScraping movie: {movie_id}")
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    r = session.get(url, timeout=30)
    print("Status:", r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "(no title)"
    print("Page title:", title)

    # IMDb sometimes serves an alternate page; try multiple selectors
    load_more = (
        soup.select_one("div.load-more-data") or
        soup.select_one("[data-key]")  # fallback
    )

    # If still missing, save a tiny hint so we know what we got
    if not load_more or not load_more.get("data-key"):
        # Try to find any element containing "paginationKey" text
        if "paginationKey" in r.text:
            print("Found 'paginationKey' in HTML text, but not in expected element.")
        else:
            print("No pagination key found. Likely blocked/alternate layout.")
        continue

    pagination_key = load_more.get("data-key")
    print("Found pagination key.")

    while pagination_key and len(rows) < 2500:
        ajax_url = "https://www.imdb.com/review/_ajax"
        params = {"ref_": "undefined", "paginationKey": pagination_key}

        rr = session.get(ajax_url, params=params, timeout=30)
        if rr.status_code != 200:
            print("AJAX status:", rr.status_code, "Stopping this movie.")
            break

        # Some responses are JSON, some are HTML; handle both
        ct = rr.headers.get("Content-Type", "")
        if "application/json" in ct:
            data = rr.json()
            html = data.get("html", "")
            pagination_key = data.get("paginationKey")
        else:
            html = rr.text
            pagination_key = None  # no further pagination

        soup2 = BeautifulSoup(html, "html.parser")
        reviews = soup2.select("div.review-container")

        for rev in reviews:
            text_tag = rev.select_one("div.text")
            rating_tag = rev.select_one("span.rating-other-user-rating span")
            if not text_tag or not rating_tag:
                continue

            try:
                rating = int(rating_tag.get_text(strip=True))
            except:
                continue

            label = label_from_rating(rating)
            if label is None:
                continue

            text = text_tag.get_text(" ", strip=True)
            if text:
                rows.append({"review_text": text, "rating": rating, "label": label})

        print("Collected so far:", len(rows))
        time.sleep(1.2)

df = pd.DataFrame(rows)

# Always save something, even if empty (with correct columns)
if df.empty:
    df = pd.DataFrame(columns=["review_text", "rating", "label"])

df.to_csv("data/raw/imdb_raw_reviews.csv", index=False, encoding="utf-8")
print("\nSaved:", df.shape, "-> data/raw/imdb_raw_reviews.csv")

if "label" in df.columns and len(df) > 0:
    print(df["label"].value_counts())
else:
    print("No labeled rows collected yet.")
