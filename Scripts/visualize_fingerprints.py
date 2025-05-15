import os
import json
import matplotlib.pyplot as plt

# === CONFIGURATION ===
FINGERPRINT_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Music_Test\Fingerprints"
SAVE_IMAGES = True  # Set to False if you prefer just showing the plots

def load_hashes(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def plot_hash_map(hashes, title, save_path=None):
    times = []
    freqs = []

    for h in hashes:
        try:
            freq1, freq2, delta = h["hash"].split("|")
            t = float(h["time"])
            times.append(t)
            freqs.append(int(freq1))
        except:
            continue  # skip malformed hashes

    plt.figure(figsize=(12, 6))
    plt.scatter(times, freqs, s=10, alpha=0.7, marker='*', color='cyan')
    plt.title(f"Constellation Map: {title}")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"✅ Saved: {save_path}")
    else:
        plt.show()

def main():
    for file in os.listdir(FINGERPRINT_FOLDER):
        if file.endswith("_fingerprint.json"):
            path = os.path.join(FINGERPRINT_FOLDER, file)
            hashes = load_hashes(path)
            title = os.path.splitext(file)[0]

            if SAVE_IMAGES:
                output_img = os.path.join(FINGERPRINT_FOLDER, title + "_map.png")
                plot_hash_map(hashes, title, output_img)
            else:
                plot_hash_map(hashes, title)

if __name__ == "__main__":
    main()
