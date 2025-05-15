import os
import re
import pandas as pd
import json

# === CONFIGURATION ===
DISCOGS_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Discogs_Data"
BASE_OUTPUT_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Recordings"
PROCESSED_DICT_PATH = os.path.join(DISCOGS_FOLDER, "processed_files.json")
SUBFOLDERS = ["Front Cover", "Back Cover", "Artist", 
              os.path.join("Audio", "mp3"),
              os.path.join("Audio", "wav"),
              os.path.join("Audio", "flac"),
              os.path.join("Audio", "raw"),
              "Fingerprints"]


# For Dictionary
def load_processed_dict():
    if os.path.exists(PROCESSED_DICT_PATH):
        with open(PROCESSED_DICT_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_processed_dict(processed_dict):
    with open(PROCESSED_DICT_PATH, 'w') as f:
        json.dump(processed_dict, f, indent=4)

# Keep track of processed CSVs
processed_csvs = {}

def get_latest_csv(folder):
    csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the folder.")
    full_paths = [os.path.join(folder, f) for f in csv_files]
    return max(full_paths, key=os.path.getmtime)

def sanitize_filename(name, max_length=100):
    # Remove invalid characters
    name = re.sub(r'[\/:*?"<>|]', '_', name)
    name = name.strip()

    # Remove trailing periods and spaces (invalid in Windows)
    name = name.rstrip(". ")

    # Truncate if too long
    if len(name) > max_length:
        name = name[:max_length].rstrip(". ")

    return name


def process_csv(csv_path):
    print(f"Processing: {csv_path}")
    df = pd.read_csv(csv_path)
    seen_albums = set()
    for _, row in df.iterrows():
        artist = re.sub(r"\s*\(\d+\)", "", str(row.get("Artist")))
        title = row.get("Title")

        if pd.isna(artist) or pd.isna(title):
            continue

        raw_name = f"{artist} - {title}"
        folder_name = sanitize_filename(raw_name)

        if folder_name in seen_albums:
            continue  # Skip duplicates
        seen_albums.add(folder_name)

        album_folder = os.path.join(BASE_OUTPUT_FOLDER, folder_name)
        os.makedirs(album_folder, exist_ok=True)

        # === Create subfolders ===
        for subfolder in SUBFOLDERS:
            os.makedirs(os.path.join(album_folder, subfolder), exist_ok=True)

        # === Extract and save metadata ===
        metadata = {
            "CatalogNumber": row.get("Catalog#"),
            "Artist": artist,
            "Title": title,
            "Label": row.get("Label"),
            "Format": row.get("Format"),
            "Released": row.get("Released"),
            "DiscogsReleaseID": row.get("release_id"),
            "DateAdded": row.get("Date Added"),
            "MediaCondition": row.get("Collection Media Condition"),
            "SleeveCondition": row.get("Collection Sleeve Condition"),
            "PricePaid": row.get("Collection Price Paid"),
            "CountryBought": row.get("Collection Bought From Country"),
            "Notes": row.get("Collection Notes")
        }

        metadata_path = os.path.join(album_folder, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)


    print(f"✅ Done. Created folders for {len(seen_albums)} albums.")

# === MAIN SCRIPT ===
if not os.path.exists(DISCOGS_FOLDER):
    os.makedirs(DISCOGS_FOLDER)

if not os.path.exists(BASE_OUTPUT_FOLDER):
    os.makedirs(BASE_OUTPUT_FOLDER)

latest_csv = get_latest_csv(DISCOGS_FOLDER)

processed_csvs = load_processed_dict()

if latest_csv not in processed_csvs:
    process_csv(latest_csv)
    processed_csvs[latest_csv] = True
    save_processed_dict(processed_csvs)
else:
    print("✅ Skipped. This CSV was already processed.")
