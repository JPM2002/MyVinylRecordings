import os

# === Base Folder ===
RECORDINGS_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Recordings"
MP3_SUBPATH = os.path.join("Audio", "mp3")

# === Track Albums ===
albums_with_mp3 = []
albums_without_mp3 = []

# === Check Each Album Folder ===
for album in os.listdir(RECORDINGS_FOLDER):
    album_path = os.path.join(RECORDINGS_FOLDER, album)
    if not os.path.isdir(album_path):
        continue

    mp3_folder = os.path.join(album_path, MP3_SUBPATH)

    if os.path.isdir(mp3_folder) and os.listdir(mp3_folder):
        albums_with_mp3.append(album)
    else:
        albums_without_mp3.append(album)

# === Summary ===
print("\n🎵 MP3 CHECK SUMMARY")
print(f"✅ Albums with MP3s: {len(albums_with_mp3)}")
print(f"❌ Albums without MP3s: {len(albums_without_mp3)}\n")

# === Detailed Lists ===
if albums_with_mp3:
    print("🎧 MP3 albums present:")
    for name in sorted(albums_with_mp3):
        print(f"  - {name}")

if albums_without_mp3:
    print("\n🚫 Albums missing MP3s:")
    for name in sorted(albums_without_mp3):
        print(f"  - {name}")
else:
    print("\n🎉 All albums have MP3s!")
