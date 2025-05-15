import os
import json
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
import tempfile
import time
import shutil
from collections import defaultdict

from fingerprint_generator import (
    load_audio_mono,
    compute_spectrogram,
    bandpass_filter,
    find_banded_peaks,
    generate_hashes,
)

# === CONFIGURATION ===
FINGERPRINT_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Music_Test\Fingerprints"
RECORD_SECONDS = 5
FS = 44100
PEAK_THRESHOLD_DB = 10
STREAK_THRESHOLD = 5
DELTA_T_GRANULARITY = 0.5
DELTA_T_TOLERANCE = 1.0  # seconds

def record_from_mic(duration=RECORD_SECONDS, fs=FS):
    print(f"\n🎤 Listening for {duration} seconds (from Realtek Array)...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=2)
    sd.wait()
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavfile.write(temp_file.name, fs, audio)

    try:
        shutil.copy(temp_file.name, r"C:\Users\Javie\Desktop\last_snippet.wav")
        print("🗂️ Copied to Desktop as 'last_snippet.wav'")
    except PermissionError:
        print("⚠️ Couldn't copy to Desktop (maybe file is open).")

    return temp_file.name

def load_reference_fingerprints():
    reference = {}
    for file in os.listdir(FINGERPRINT_FOLDER):
        if file.endswith("_fingerprint.json"):
            with open(os.path.join(FINGERPRINT_FOLDER, file), "r", encoding="utf-8") as f:
                hashes = json.load(f)
                song_name = file.replace("_fingerprint.json", "")
                reference[song_name] = hashes
    return reference

def generate_query_hashes(wav_path):
    fs, audio = load_audio_mono(wav_path)
    freqs, times, spec = compute_spectrogram(audio, fs)
    spec, freqs = bandpass_filter(spec, freqs)
    peaks = find_banded_peaks(spec, freqs, times)
    return generate_hashes(peaks, freqs, times)

def group_offsets(offsets, tolerance):
    grouped = defaultdict(int)
    for offset in offsets:
        if offset == 0: continue
        binned = round(offset / tolerance) * tolerance
        grouped[binned] += 1
    return grouped

def compare_hashes(query_hashes, reference_hashes):
    ref_hash_map = defaultdict(list)
    for ref in reference_hashes:
        ref_hash_map[ref["hash"]].append(ref["time"])

    offset_map = []

    for q in query_hashes:
        q_time = q["time"]
        for ref_time in ref_hash_map.get(q["hash"], []):
            offset = round(ref_time - q_time, 2)
            offset_map.append(offset)

    return group_offsets(offset_map, DELTA_T_TOLERANCE)

def identify(wav_path, reference):
    query_hashes = generate_query_hashes(wav_path)
    total_query_hashes = len(query_hashes)
    print(f"🔍 Total query hashes: {total_query_hashes}")

    match_scores = {}

    for song, ref_hashes in reference.items():
        grouped_offsets = compare_hashes(query_hashes, ref_hashes)
        streaks = [v for k, v in grouped_offsets.items() if v > 1 and k != 0]
        total_score = sum(streaks)
        best_streak = max(streaks) if streaks else 0
        best_offset = max(grouped_offsets, key=grouped_offsets.get, default=0)
        match_scores[song] = {
            "total": total_score,
            "streak": best_streak,
            "offset": best_offset
        }

    # Rank by highest single streak, break ties with total score
    top_matches = sorted(match_scores.items(), key=lambda x: (x[1]['streak'], x[1]['total']), reverse=True)[:3]

    for song, data in top_matches:
        print(f"  ↳ {song}: best streak {data['streak']} at Δt={data['offset']}s | total {data['total']}")

    best_song, best_data = top_matches[0]

    if best_data["streak"] >= STREAK_THRESHOLD:
        print(f"\n✅ IDENTIFIED: {best_song} — best streak {best_data['streak']} at Δt={best_data['offset']}s")
        return best_song
    else:
        print("❌ No strong match found.")
        return None


def run_match_loop():
    reference = load_reference_fingerprints()
    while True:
        try:
            clip_path = record_from_mic()
            result = identify(clip_path, reference)
            if result:
                break
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break

if __name__ == "__main__":
    run_match_loop()
