import os
import json
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
import tempfile
import time
import shutil
from collections import defaultdict, Counter
from fingerprint_generator import (
    load_audio_mono,
    compute_spectrogram,
    bandpass_filter,
    find_banded_peaks,
    generate_hashes,
)

# === CONFIGURATION ===
FINGERPRINT_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Music_Test\Fingerprints"
RECORD_SECONDS = 10
FS = 44100
WINDOW_SIZE = 5  # seconds per sub-window
WINDOW_STRIDE = 1  # sliding step in seconds
PEAK_THRESHOLD_DB = 10
STREAK_THRESHOLD = 5
DELTA_T_TOLERANCE = 1.0  # seconds
SILENCE_THRESHOLD = 100  # Minimum mean energy to accept a window

# === RECORD FROM MIC ===
def record_from_mic(duration=RECORD_SECONDS, fs=FS):
    print(f"\n🎤 Recording {duration}s from mic (Realtek Array)...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=2)
    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavfile.write(temp_file.name, fs, audio)

    try:
        shutil.copy(temp_file.name, r"C:\Users\Javie\Desktop\last_snippet.wav")
        print("📂️ Copied to Desktop as 'last_snippet.wav'")
    except PermissionError:
        print("⚠️ Couldn’t copy to Desktop (file open?).")

    return temp_file.name

# === LOAD DATABASE + BUILD INVERTED INDEX ===
def load_fingerprints_inverted_index():
    inverted_index = defaultdict(list)
    song_lengths = Counter()

    for file in os.listdir(FINGERPRINT_FOLDER):
        if file.endswith("_fingerprint.json"):
            path = os.path.join(FINGERPRINT_FOLDER, file)
            with open(path, "r", encoding="utf-8") as f:
                hashes = json.load(f)
                song_name = file.replace("_fingerprint.json", "")
                for h in hashes:
                    inverted_index[h["hash"]].append((song_name, h["time"]))
                song_lengths[song_name] += len(hashes)
    return inverted_index, song_lengths

# === SLIDING WINDOW HASHING ===
def generate_query_hashes(wav_path):
    fs, audio = load_audio_mono(wav_path)
    total_len = len(audio) / fs
    query_hashes = []

    for start in np.arange(0, total_len - WINDOW_SIZE + 0.01, WINDOW_STRIDE):
        s = int(start * fs)
        e = int((start + WINDOW_SIZE) * fs)
        clip = audio[s:e]

        if np.mean(np.abs(clip)) < SILENCE_THRESHOLD:
            continue  # skip silence

        freqs, times, spec = compute_spectrogram(clip, fs)
        spec, freqs = bandpass_filter(spec, freqs)
        peaks = find_banded_peaks(spec, freqs, times)
        hashes = generate_hashes(peaks, freqs, times + start)
        query_hashes.extend(hashes)

    return query_hashes

# === MATCHING AND WEIGHTING ===
def group_offsets(query_hashes, index, idf_weights):
    offset_bins = defaultdict(lambda: defaultdict(int))
    for q in query_hashes:
        for song, ref_time in index.get(q["hash"], []):
            offset = round(ref_time - q["time"], 2)
            if offset == 0:
                continue
            binned = round(offset / DELTA_T_TOLERANCE) * DELTA_T_TOLERANCE
            weight = idf_weights.get(q["hash"], 1.0)
            offset_bins[song][binned] += weight
    return offset_bins

def rank_matches(offset_bins):
    results = []
    for song, offsets in offset_bins.items():
        top_streak = max(offsets.values())
        total_score = sum(offsets.values())
        best_offset = max(offsets, key=offsets.get)
        results.append((song, top_streak, total_score, best_offset))
    return sorted(results, key=lambda x: (x[1], x[2]), reverse=True)

# === IDF SCORE COMPUTATION ===
def compute_idf_weights(index, total_songs):
    df = Counter()
    for h in index:
        df[h] = len(set([song for song, _ in index[h]]))
    idf = {h: np.log10(total_songs / (1 + df[h])) for h in df}
    return idf

# === IDENTIFICATION PIPELINE ===
def identify(query_path, index, idf_weights):
    query_hashes = generate_query_hashes(query_path)
    print(f"🔍 Total query hashes: {len(query_hashes)}")

    offset_bins = group_offsets(query_hashes, index, idf_weights)
    ranked = rank_matches(offset_bins)[:3]

    for song, streak, score, offset in ranked:
        print(f"  → {song}: best streak {round(streak)} at Δt={offset}s | total score {round(score)}")

    if ranked and ranked[0][1] >= STREAK_THRESHOLD:
        best = ranked[0]
        print(f"\n✅ IDENTIFIED: {best[0]} — streak {round(best[1])} at Δt={best[3]}s")
        return best[0]
    else:
        print("❌ No strong match found.")
        return None

# === MAIN LOOP ===
def run_match_loop():
    index, song_lengths = load_fingerprints_inverted_index()
    idf_weights = compute_idf_weights(index, total_songs=len(song_lengths))

    while True:
        try:
            clip = record_from_mic()
            result = identify(clip, index, idf_weights)
            if result:
                break
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break

if __name__ == "__main__":
    run_match_loop()
