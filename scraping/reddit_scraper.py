import time
import requests
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

SUBREDDITS = ["technology", "science", "sports", "books", "fitness"]
PER_SUBREDDIT = 1200  # 5 subs * 500 = 2500 samples (>=2000)

def fetch_posts(subreddit, after=None, limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    params = {"limit": limit}
    if after:
        params["after"] = after
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

rows = []

for sub in SUBREDDITS:
    print(f"\nCollecting from r/{sub}")
    after = None
    collected = 0

    while collected < PER_SUBREDDIT:
        data = fetch_posts(sub, after=after, limit=100)
        children = data["data"]["children"]
        if not children:
            break

        for c in children:
            title = c["data"].get("title", "").strip()
            if not title:
                continue
            rows.append({"text": title, "label": sub})
            collected += 1
            if collected >= PER_SUBREDDIT:
                break

        after = data["data"].get("after")
        if after is None:
            break

        print(f"  collected {collected}/{PER_SUBREDDIT}")
        time.sleep(1.0)  # polite

df = pd.DataFrame(rows)
df.to_csv("data/raw/reddit_raw.csv", index=False, encoding="utf-8")

print("\nSaved:", df.shape, "-> data/raw/reddit_raw.csv")
print(df["label"].value_counts())
