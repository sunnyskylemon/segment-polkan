from __future__ import annotations
import numpy as np


def moving_average(values: list[float], window: int = 5) -> list[float]:
    if window <= 1:
        return values
    arr = np.asarray(values, dtype=float)
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode="same").tolist()


def baseline_subtract(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    baseline = np.percentile(arr, 10)
    return np.maximum(arr - baseline, 0).tolist()


def find_peaks(values: list[float], threshold_ratio: float = 0.35) -> list[dict]:
    arr = np.asarray(values, dtype=float)
    if len(arr) < 3:
        return []
    threshold = float(arr.max() * threshold_ratio)
    peaks = []
    for i in range(1, len(arr) - 1):
        if arr[i] > threshold and arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            peaks.append({"channel": i, "intensity": float(arr[i])})
    return peaks


def process_spectrum(values: list[float]) -> dict:
    smoothed = moving_average(values, window=7)
    corrected = baseline_subtract(smoothed)
    peaks = find_peaks(corrected)
    total = float(np.sum(corrected))
    max_value = float(np.max(corrected)) if corrected else 0.0
    return {
        "points": len(values),
        "total_intensity": total,
        "max_intensity": max_value,
        "peaks": peaks[:10],
        "risk_level": "high" if max_value > 80 else "medium" if max_value > 35 else "low",
    }
