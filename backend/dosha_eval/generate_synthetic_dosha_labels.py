import csv
from pathlib import Path
from itertools import product

# Synthetic answer spaces (aligned with your API fields)
OPTIONS = {
    "body_frame": ["thin", "medium", "large"],
    "skin_type": ["dry", "sensitive", "oily"],
    "digestion": ["irregular", "strong", "slow"],
    "sleep_pattern": ["light", "moderate", "deep"],
    "stress_response": ["anxious", "irritable", "withdrawn"],
    "climate_preference": ["warm", "cool", "moderate_temp"],
    "energy_level": ["variable", "high", "steady"],
    "appetite": ["irregular_appetite", "strong_appetite", "steady_appetite"],
    "mental_state": ["creative", "focused", "calm"],
    "physical_activity": ["quick_movements", "purposeful", "slow_steady"],
}

# Rule rubric (proxy ground truth) similar to prior mapping
RUBRIC = {
    # key -> option -> (vata, pitta, kapha)
    "body_frame": {
        "thin": (2,0,0), "medium": (0,2,0), "large": (0,0,2)
    },
    "skin_type": {
        "dry": (2,0,0), "sensitive": (0,2,0), "oily": (0,0,2)
    },
    "digestion": {
        "irregular": (2,0,0), "strong": (0,2,0), "slow": (0,0,2)
    },
    "sleep_pattern": {
        "light": (2,0,0), "moderate": (0,2,0), "deep": (0,0,2)
    },
    "stress_response": {
        "anxious": (2,0,0), "irritable": (0,2,0), "withdrawn": (0,0,2)
    },
    "climate_preference": {
        "warm": (2,0,0), "cool": (0,2,0), "moderate_temp": (0,0,2)
    },
    "energy_level": {
        "variable": (2,0,0), "high": (0,2,0), "steady": (0,0,2)
    },
    "appetite": {
        "irregular_appetite": (2,0,0), "strong_appetite": (0,2,0), "steady_appetite": (0,0,2)
    },
    "mental_state": {
        "creative": (2,0,0), "focused": (0,2,0), "calm": (0,0,2)
    },
    "physical_activity": {
        "quick_movements": (2,0,0), "purposeful": (0,2,0), "slow_steady": (0,0,2)
    },
}

HEADERS = list(OPTIONS.keys()) + [
    "vata_true", "pitta_true", "kapha_true", "dominant_dosha_true"
]


def score_row(row):
    v = p = k = 0
    for key, value in row.items():
        if key in RUBRIC and value in RUBRIC[key]:
            dv, dp, dk = RUBRIC[key][value]
            v += dv; p += dp; k += dk
    total = v + p + k
    if total == 0:
        return 33.3, 33.3, 33.3, "Vata"
    v_pct = 100.0 * v / total
    p_pct = 100.0 * p / total
    k_pct = 100.0 * k / total
    trio = [("Vata", v_pct), ("Pitta", p_pct), ("Kapha", k_pct)]
    trio.sort(key=lambda x: x[1], reverse=True)
    return round(v_pct,1), round(p_pct,1), round(k_pct,1), trio[0][0]


def main(max_rows: int = 500):
    out_dir = Path("backend/dosha_eval")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "dosha_synthetic_labels.csv"

    # Cartesian product but cap to max_rows for speed
    all_lists = [OPTIONS[k] for k in OPTIONS]
    combos = product(*all_lists)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        count = 0
        for combo in combos:
            row = {k: v for k, v in zip(OPTIONS.keys(), combo)}
            v_true, p_true, k_true, dom = score_row(row)
            w.writerow([*(row[k] for k in OPTIONS.keys()), v_true, p_true, k_true, dom])
            count += 1
            if count >= max_rows:
                break
    print(f"Wrote {count} rows to {out_path}")


if __name__ == "__main__":
    main()
