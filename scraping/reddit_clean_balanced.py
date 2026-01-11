import re
import pandas as pd

RAW = "data/raw/reddit_raw.csv"
OUT = "data/processed/reddit_clean_balanced.csv"

TARGET_PER_CLASS = 500   # final balanced output
MIN_LEN = 12             # minimum length after cleaning

df = pd.read_csv(RAW)

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)     # urls
    text = re.sub(r"[^a-z0-9\s]", " ", text)          # keep letters + numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["text"] = df["text"].apply(clean_text)
df = df[df["text"].str.len() >= MIN_LEN].copy()

# remove duplicates within each label
df = df.drop_duplicates(subset=["label", "text"])

# balance sampling
balanced = []
for label, group in df.groupby("label"):
    group = group.sample(min(TARGET_PER_CLASS, len(group)), random_state=42)
    balanced.append(group)

out = pd.concat(balanced).sample(frac=1, random_state=42).reset_index(drop=True)
out.to_csv(OUT, index=False, encoding="utf-8")

print("Raw:", pd.read_csv(RAW).shape)
print("After clean+filter:", df.shape)
print("Final balanced:", out.shape, "->", OUT)
print(out["label"].value_counts())
print("Example:", out.iloc[0]["text"])
