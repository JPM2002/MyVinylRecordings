import os

# === Base Folder ===
RECORDINGS_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Recordings"
RAW_SUBPATH = os.path.join("Audio", "raw")

# === Counters ===
total_albums = 0
recorded_albums = 0
not_recorded_albums = []

# === Walk Through Each Album Folder ===
for album_name in os.listdir(RECORDINGS_FOLDER):
    album_path = os.path.join(RECORDINGS_FOLDER, album_name)
    if not os.path.isdir(album_path):
        continue

    total_albums += 1
    raw_folder = os.path.join(album_path, RAW_SUBPATH)

    if os.path.isdir(raw_folder):
        contents = os.listdir(raw_folder)
        if contents:
            recorded_albums += 1
        else:
            not_recorded_albums.append(album_name)
    else:
        not_recorded_albums.append(album_name)

# === Summary Report ===
print(f"\n📀 Total albums: {total_albums}")
print(f"✅ Albums with raw recordings: {recorded_albums}")
print(f"❌ Albums without raw recordings: {total_albums - recorded_albums}\n")

if not_recorded_albums:
    print("🔎 Missing 'Audio/raw' content in:")
    for album in not_recorded_albums:
        print(f"  - {album}")
else:
    print("🎉 All albums have raw audio recorded!")
