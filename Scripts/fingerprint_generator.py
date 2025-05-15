import os
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import stft
from scipy.ndimage import maximum_filter
import json

# === CONFIGURATION ===
INPUT_FOLDER = r"C:\Users\Javie\Documents\GitHub\MyVinylRecordings\Data\Music_Test"
FINGERPRINT_FOLDER = os.path.join(INPUT_FOLDER, "Fingerprints")
os.makedirs(FINGERPRINT_FOLDER, exist_ok=True)

WINDOW_SIZE = 4096
OVERLAP = 2048
FREQ_BAND = (300, 3000)
PEAK_THRESHOLD_DB = 10
FAN_VALUE = 10
NUM_BANDS = 5  # Divide frequency range into 5 bands

def load_audio_mono(filepath):
    fs, data = wav.read(filepath)
    if data.ndim > 1:
        data = np.mean(data, axis=1)  # stereo to mono
    return fs, data

def compute_spectrogram(audio, fs):
    freqs, times, Zxx = stft(audio, fs=fs, nperseg=WINDOW_SIZE, noverlap=OVERLAP)
    Z = np.abs(Zxx)
    Z_db = 20 * np.log10(Z + 1e-10)
    return freqs, times, Z_db

def bandpass_filter(spectrogram, freqs):
    band_mask = (freqs >= FREQ_BAND[0]) & (freqs <= FREQ_BAND[1])
    return spectrogram[band_mask, :], freqs[band_mask]

def find_banded_peaks(spec, freqs, times):
    peaks = []
    band_edges = np.linspace(freqs[0], freqs[-1], NUM_BANDS + 1)

    for t_idx in range(spec.shape[1]):
        for b in range(NUM_BANDS):
            f_start = band_edges[b]
            f_end = band_edges[b + 1]
            band_mask = (freqs >= f_start) & (freqs < f_end)
            if not np.any(band_mask):
                continue
            band_data = spec[band_mask, t_idx]
            if len(band_data) == 0:
                continue
            peak_val = np.max(band_data)
            if peak_val > PEAK_THRESHOLD_DB:
                f_idx_local = np.argmax(band_data)
                f_idx_global = np.where(band_mask)[0][f_idx_local]
                peaks.append((t_idx, f_idx_global))
    return peaks

def generate_hashes(peaks, freqs, times, fan_value=FAN_VALUE):
    hashes = []
    time_freq_points = [(times[t], freqs[f]) for t, f in peaks]

    for i in range(len(time_freq_points)):
        t1, f1 = time_freq_points[i]
        for j in range(1, fan_value + 1):
            if i + j < len(time_freq_points):
                t2, f2 = time_freq_points[i + j]
                delta_t = t2 - t1
                if 0 < delta_t <= 10:
                    hash_string = f"{int(f1)}|{int(f2)}|{round(delta_t, 2)}"
                    hashes.append({
                        "hash": hash_string,
                        "time": round(t1, 2)
                    })
    return hashes

def fingerprint_audio_file(wav_path):
    fs, audio = load_audio_mono(wav_path)
    freqs, times, spec = compute_spectrogram(audio, fs)
    spec, freqs = bandpass_filter(spec, freqs)
    peaks = find_banded_peaks(spec, freqs, times)
    hashes = generate_hashes(peaks, freqs, times)

    filename = os.path.splitext(os.path.basename(wav_path))[0]
    out_path = os.path.join(FINGERPRINT_FOLDER, f"{filename}_fingerprint.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)

    print(f"✅ {filename}: {len(hashes)} hashes saved to {out_path}")

def main():
    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith(".wav"):
            filepath = os.path.join(INPUT_FOLDER, file)
            fingerprint_audio_file(filepath)

if __name__ == "__main__":
    main()
