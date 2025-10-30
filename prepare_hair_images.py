#!/usr/bin/env python3
from pathlib import Path
import shutil, csv, random

RAW_DIR   = Path("data/hair_scalp/raw")
IMG_DIR   = RAW_DIR / "images"
CSV_PATH  = RAW_DIR / "bald_people.csv"
OUT_TRAIN = Path("data/hair_scalp/train")
OUT_TEST  = Path("data/hair_scalp/test")
SPLIT     = 0.8  # 80/20 split if CSV has no split column

def safe_copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)

def main():
    if not IMG_DIR.exists():
        raise FileNotFoundError(f"Missing images: {IMG_DIR}")
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing CSV: {CSV_PATH}")

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = [h.strip().lower() for h in reader.fieldnames if h and h.strip()]

        def pick(opts):
            for o in opts:
                if o in headers:
                    return o
            return None

        # Your CSV headers are ['', 'images', 'type']
        img_col   = pick(["images","image","file","filename","image_name"]) or "images"
        label_col = pick(["type","label","class","category"]) or "type"
        split_col = pick(["split","set"])  # may be missing

        rows = [{(k or '').strip().lower(): (v or '').strip() for k,v in r.items()} for r in reader]

        if not split_col:
            random.seed(42)
            random.shuffle(rows)
            cut = int(len(rows) * SPLIT)
            for i, r in enumerate(rows):
                r["split"] = "train" if i < cut else "test"
            split_col = "split"

        total = copied = 0
        for r in rows:
            total += 1
            # Normalize path from CSV
            name_raw = r.get(img_col, "").replace("\\", "/").lstrip("/")
            if name_raw.lower().startswith("images/"):
                name_raw = name_raw.split("/", 1)[1]
            filename = name_raw.split("/")[-1]

            label = r.get(label_col, "").replace(" ", "_") or "Unknown"
            subset = (r.get(split_col) or "").lower()
            if subset not in ("train", "test"):
                subset = "train" if random.random() < SPLIT else "test"

            # Look only by filename inside IMG_DIR
            src = IMG_DIR / filename
            if not src.exists():
                found = None
                for ext in (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
                    cand = filename if filename.lower().endswith(ext.lower()) else filename + ext
                    p = IMG_DIR / cand
                    if p.exists():
                        found = p
                        break
                if not found:
                    print(f"Skip missing: {r.get(img_col)}")
                    continue
                src = found

            dst_root = OUT_TRAIN if subset == "train" else OUT_TEST
            dst = dst_root / label / src.name
            safe_copy(src, dst)
            copied += 1

        print(f"Done. Rows: {total}, Copied: {copied}")
        print(f"Train: {OUT_TRAIN.resolve()}")
        print(f"Test:  {OUT_TEST.resolve()}")

if __name__ == "__main__":
    main()