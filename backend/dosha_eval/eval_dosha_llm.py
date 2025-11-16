import csv
from pathlib import Path
from typing import Dict, List, Tuple
import math

# Import the LLM scorer from the API router
# Make sure the 'backend' directory (parent of this file) is on sys.path
import sys
ROOT_BACKEND = Path(__file__).resolve().parents[1]  # .../backend
if str(ROOT_BACKEND) not in sys.path:
    sys.path.insert(0, str(ROOT_BACKEND))
from routers.dosha import generate_scores_with_flan_t5


def dominant_from_scores(scores: Dict[str, float]) -> str:
    trio = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return trio[0][0].capitalize()


def eval_regression(rows: List[Dict[str, str]]) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Return MAE and RMSE per dosha and macro-averaged."""
    errs = {"vata": [], "pitta": [], "kapha": []}

    for r in rows:
        answers = {
            k: r[k]
            for k in [
                "body_frame",
                "skin_type",
                "digestion",
                "sleep_pattern",
                "stress_response",
                "climate_preference",
                "energy_level",
                "appetite",
                "mental_state",
                "physical_activity",
            ]
        }
        pred = generate_scores_with_flan_t5(answers)
        for k2 in ["vata", "pitta", "kapha"]:
            try:
                true_val = float(r[f"{k2}_true"]) if r.get(f"{k2}_true") not in (None, "") else None
            except ValueError:
                true_val = None
            if true_val is not None:
                errs[k2].append((true_val - float(pred[k2])) ** 2)  # store squared error for now
                # Also store MAE term alongside using tuple? We can recompute MAE separately with abs errors

    # Re-read to also collect absolute errors for MAE
    maes = {"vata": [], "pitta": [], "kapha": []}
    for r in rows:
        answers = {
            k: r[k]
            for k in [
                "body_frame",
                "skin_type",
                "digestion",
                "sleep_pattern",
                "stress_response",
                "climate_preference",
                "energy_level",
                "appetite",
                "mental_state",
                "physical_activity",
            ]
        }
        pred = generate_scores_with_flan_t5(answers)
        for k2 in ["vata", "pitta", "kapha"]:
            try:
                true_val = float(r[f"{k2}_true"]) if r.get(f"{k2}_true") not in (None, "") else None
            except ValueError:
                true_val = None
            if true_val is not None:
                maes[k2].append(abs(true_val - float(pred[k2])))

    mae = {k: (sum(v) / len(v) if v else math.nan) for k, v in maes.items()}
    rmse = {k: (math.sqrt(sum(v) / len(v)) if v else math.nan) for k, v in errs.items()}

    # Macro averages
    mae["macro"] = sum(val for val in mae.values() if not math.isnan(val)) / 3
    rmse["macro"] = sum(val for val in rmse.values() if not math.isnan(val)) / 3
    return mae, rmse


def eval_classification(rows: List[Dict[str, str]]) -> float:
    total = 0
    correct = 0
    for r in rows:
        answers = {
            k: r[k]
            for k in [
                "body_frame",
                "skin_type",
                "digestion",
                "sleep_pattern",
                "stress_response",
                "climate_preference",
                "energy_level",
                "appetite",
                "mental_state",
                "physical_activity",
            ]
        }
        pred = generate_scores_with_flan_t5(answers)
        pred_dom = dominant_from_scores(pred)
        true_dom = r.get("dominant_dosha_true")
        if true_dom:
            total += 1
            if pred_dom.lower().strip() == true_dom.lower().strip():
                correct += 1
    return (correct / total * 100.0) if total else float("nan")


def main(csv_path: str = "backend/dosha_eval/dosha_synthetic_labels.csv"):
    path = Path(csv_path)
    if not path.exists():
        print(f"Dataset not found: {path}")
        return

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Evaluate regression metrics (if *_true columns exist)
    mae, rmse = eval_regression(rows)
    print("\n== Regression (percentage) metrics ==")
    print(f"MAE:   vata={mae['vata']:.2f}, pitta={mae['pitta']:.2f}, kapha={mae['kapha']:.2f}, macro={mae['macro']:.2f}")
    print(f"RMSE:  vata={rmse['vata']:.2f}, pitta={rmse['pitta']:.2f}, kapha={rmse['kapha']:.2f}, macro={rmse['macro']:.2f}")

    # Evaluate classification accuracy (dominant dosha)
    acc = eval_classification(rows)
    print("\n== Classification (dominant dosha) ==")
    print(f"Top-1 Accuracy: {acc:.2f}%")


if __name__ == "__main__":
    main()
