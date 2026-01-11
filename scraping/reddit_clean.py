import re
import pandas as pd

IN_PATH = "data/raw/reddit_raw.csv"
OUT_PATH = "data/processed/reddit_clean.csv"

df = pd.read_csv(IN_PATH)
#cleaning
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)     # remove URLs
    text = re.sub(r"[^a-z\s]", " ", text)             # keep only letters + spaces
    text = re.sub(r"\s+", " ", text).strip()          # remove extra spaces
    return text

df["text"] = df["text"].apply(clean_text)

# remove empty rows after cleaning
df = df[df["text"].str.len() > 0].copy()

# optional: remove duplicates (recommended)
df = df.drop_duplicates(subset=["text", "label"])

df.to_csv(OUT_PATH, index=False, encoding="utf-8")

print("Raw shape:", pd.read_csv(IN_PATH).shape)
print("Clean shape:", df.shape, "->", OUT_PATH)
print(df["label"].value_counts())
print("Example cleaned text:", df.iloc[0]["text"])
