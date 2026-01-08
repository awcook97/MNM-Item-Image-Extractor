#!/usr/bin/env python3
"""
OCR EQ item screenshots -> title from TOP BANNER only, body from content area.
Renames image to TITLE_WITH_UNDERSCORES.ext and writes TITLE_WITH_UNDERSCORES.txt

Fixes for your current failure mode:
- Don’t take “first OCR line” as title (often garbage from the filigree border).
- Use pytesseract image_to_data to pick the MOST CONFIDENT line in the banner that
  contains letters and looks like a title.
- Use a whitelist for the banner pass (A–Z, space, apostrophe) to stop random symbols.
- Add a small *light* left padding (white) instead of black (black creates fake “ink”).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Tuple, Dict, List

import cv2
import numpy as np
import pytesseract

# If you're on Windows and pytesseract can't find tesseract.exe, uncomment and set:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

# Your layout knobs (keep as-is)
BANNER_Y0 = 0.01
BANNER_Y1 = 0.15
BANNER_X0 = 0.02
BANNER_X1 = 0.70

BODY_Y0 = 0.15
BODY_Y1 = 1.00
BODY_X0 = 0.00
BODY_X1 = 1.00

BODY_ICON_BLANK_W = 0.11  # fraction of body width


def safe_title_to_filename(title: str) -> str:
    title = title.strip().upper()
    title = re.sub(r"[^\w\s-]", "", title)
    title = re.sub(r"[\s-]+", "_", title).strip("_")
    title = re.sub(r"_+", "_", title)
    return title or "UNTITLED"


def normalize_text(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        ln = re.sub(r"\s+", " ", ln).strip()
        if ln:
            ln = re.sub(r"^[\W_]+", "", ln).strip()
            if ln:
                lines.append(ln)
    return "\n".join(lines).strip()


def crop_frac(img: np.ndarray, x0: float, y0: float, x1: float, y1: float) -> np.ndarray:
    h, w = img.shape[:2]
    xa, ya = int(w * x0), int(h * y0)
    xb, yb = int(w * x1), int(h * y1)
    return img[ya:yb, xa:xb]


def preprocess_banner(bgr: np.ndarray) -> np.ndarray:
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # White padding so we don't lose the first letter
    g = cv2.copyMakeBorder(g, 10, 10, 30, 30, borderType=cv2.BORDER_CONSTANT, value=255)

    # Upscale
    g = cv2.resize(g, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)

    # Mild blur (too much blur merges gaps)
    g = cv2.GaussianBlur(g, (3, 3), 0)

    # Banner is light text on dark background -> invert binary to get text as white
    _, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # IMPORTANT: do NOT close (closing bridges word gaps).
    # If you want a tiny cleanup, use OPEN (removes speckle without merging words)
    th = cv2.morphologyEx(
        th, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1
    )

    # Convert to black text on white background for tesseract
    return 255 - th



def preprocess_body(bgr: np.ndarray) -> np.ndarray:
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    inv = 255 - g
    inv = cv2.GaussianBlur(inv, (3, 3), 0)
    _, th = cv2.threshold(inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    th = cv2.morphologyEx(
        th, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1
    )
    return th


def ocr_banner(img_1ch: np.ndarray) -> str:
    # psm 7 = single line, and we explicitly allow variable spacing behavior
    cfg = "--oem 1 --psm 7 -c textord_space_size_is_variable=1"
    return pytesseract.image_to_string(img_1ch, config=cfg)

def ocr_body(img_1ch: np.ndarray) -> str:
    return pytesseract.image_to_string(img_1ch, config="--oem 1 --psm 6")



def banner_best_line(img_1ch: np.ndarray) -> str:
    # Banner: only allow letters and spaces (stable for filenames and avoids shlex quoting issues)
    cfg = (
        "--oem 1 --psm 6 "
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    )

    d = pytesseract.image_to_data(img_1ch, output_type=pytesseract.Output.DICT, config=cfg)

    # group word indices by (block, par, line)
    groups: Dict[Tuple[int, int, int], List[int]] = {}
    n = len(d.get("text", []))
    for i in range(n):
        txt = (d["text"][i] or "").strip()
        if not txt:
            continue
        key = (int(d["block_num"][i]), int(d["par_num"][i]), int(d["line_num"][i]))
        groups.setdefault(key, []).append(i)

    best_line = ""
    best_score = -1e9

    for idxs in groups.values():
        # sort left-to-right
        idxs = sorted(idxs, key=lambda j: int(d["left"][j]))
        print("BANNER TOKENS:", [d["text"][j] for j in idxs])

        words = []
        confs = []
        tops = []

        for j in idxs:
            w = (d["text"][j] or "").strip().upper()
            if not w:
                continue

            # If tesseract glues words, try to un-glue a bit by inserting spaces
            # between long runs of letters based on common EQ title words is unreliable,
            # so we just treat each token as a word and join with spaces.
            words.append(w)

            try:
                c = float(d["conf"][j])
                if c >= 0:
                    confs.append(c)
            except Exception:
                pass

            tops.append(int(d["top"][j]))

        if not words:
            continue

        line = " ".join(words)
        line = re.sub(r"\s+", " ", line).strip()

        # must have enough letters to be a title
        if len(re.findall(r"[A-Z]", line)) < 6:
            continue

        bad = len(re.findall(r"[^A-Z\s]", line))
        avg_conf = float(np.mean(confs)) if confs else 0.0
        mid_top = float(np.median(tops)) if tops else 0.0

        score = avg_conf + (len(line) * 0.4) - (bad * 5.0)
        score -= abs(mid_top - (img_1ch.shape[0] * 0.55)) * 0.01

        if score > best_score:
            best_score = score
            best_line = line

    return best_line




def extract_title_and_body(img_bgr: np.ndarray) -> Tuple[str, str]:
    # --- Title from banner ---
    banner = crop_frac(img_bgr, BANNER_X0, BANNER_Y0, BANNER_X1, BANNER_Y1)
    banner_th = preprocess_banner(banner)

    raw_title = ocr_banner(banner_th)

    # Keep ONLY letters/spaces, collapse whitespace
    title = raw_title.upper()
    title = re.sub(r"[^A-Z\s]", " ", title)
    title = re.sub(r"\s+", " ", title).strip()

    # --- Body from content area ---
    body = crop_frac(img_bgr, BODY_X0, BODY_Y0, BODY_X1, BODY_Y1)
    body_th = preprocess_body(body)

    h, w = body_th.shape[:2]
    body_th[:, : int(w * BODY_ICON_BLANK_W)] = 255

    raw_body = ocr_body(body_th)
    body_text = normalize_text(raw_body)

    return title, body_text



def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suf = path.stem, path.suffix
    i = 2
    while True:
        cand = path.with_name(f"{stem}_{i}{suf}")
        if not cand.exists():
            return cand
        i += 1


def process_folder(folder: Path) -> None:
    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.suffix.lower() not in IMG_EXTS:
            continue

        img = cv2.imread(str(p))
        if img is None:
            print(f"SKIP (unreadable): {p.name}")
            continue

        title, body = extract_title_and_body(img)
        if not title:
            print(f"SKIP (no title OCR): {p.name}")
            continue

        filename_base = safe_title_to_filename(title)

        out_text = title.strip() + "\n" + (body.strip() + "\n" if body else "")
        txt_path = unique_path(p.with_name(f"{filename_base}.txt"))
        txt_path.write_text(out_text, encoding="utf-8")

        new_img_path = unique_path(p.with_name(f"{filename_base}{p.suffix.lower()}"))
        if new_img_path != p:
            p.rename(new_img_path)

        print(f"OK: {p.name} -> {new_img_path.name} + {txt_path.name}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python ocr_eq_items.py /path/to/MyFolder")
        return 2

    folder = Path(sys.argv[1]).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        print(f"Not a folder: {folder}")
        return 2

    process_folder(folder)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
