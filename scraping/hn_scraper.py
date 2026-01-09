import time
import requests
import pandas as pd

BASE = "https://hacker-news.firebaseio.com/v0"
ITEM = BASE + "/item/{}.json"

SOURCES = {
    "ask": BASE + "/askstories.json",
    "show": BASE + "/showstories.json",
    "new": BASE + "/newstories.json",
    "top": BASE + "/topstories.json",
}

TARGETS = {"story": 800, "ask_hn": 800, "show_hn": 800}  # total 2400+
SLEEP = 0.03

def label_from_title(title: str):
    t = title.strip().lower()
    if t.startswith("ask hn:"):
        return "ask_hn"
    if t.startswith("show hn:"):
        return "show_hn"
    return "story"

def fetch_ids(url, limit=5000):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    ids = r.json()
    return ids[:limit]  # take more than 500

def fetch_item(item_id):
    r = requests.get(ITEM.format(item_id), timeout=30)
    if r.status_code != 200:
        return None
    return r.json()

def done(counts):
    return all(counts[k] >= TARGETS[k] for k in TARGETS)

seen_ids = set()
rows = []
counts = {"story": 0, "ask_hn": 0, "show_hn": 0}

for source_name, source_url in SOURCES.items():
    ids = fetch_ids(source_url, limit=6000)
    print(f"\nSource: {source_name} -> {len(ids)} ids")

    for i, item_id in enumerate(ids):
        if done(counts):
            break
        if item_id in seen_ids:
            continue
        seen_ids.add(item_id)

        item = fetch_item(item_id)
        if not item or item.get("type") != "story":
            continue

        title = item.get("title")
        if not title:
            continue

        label = label_from_title(title)

        # Balance control
        if counts[label] >= TARGETS[label]:
            continue

        rows.append({
            "id": item_id,
            "title": title,
            "label": label,
            "source": source_name,
            "time": item.get("time", None),
            "url": item.get("url", None),
        })
        counts[label] += 1

        if (i + 1) % 500 == 0:
            print(f"  processed {i+1} | counts: {counts}")

        time.sleep(SLEEP)

    if done(counts):
        break

df = pd.DataFrame(rows)
df.to_csv("data/raw/hn_raw.csv", index=False, encoding="utf-8")

print("\nSaved:", df.shape, "-> data/raw/hn_raw.csv")
print("Final counts:", df["label"].value_counts().to_dict())
