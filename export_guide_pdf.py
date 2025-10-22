#!/usr/bin/env python3
"""
Export PostgreSQL_Connection_Guide.md to PDF on Windows using Microsoft Edge headless.

Usage:
  1) pip install markdown
  2) python export_guide_pdf.py

Output: PostgreSQL_Connection_Guide.pdf in the same directory as this script.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

try:
    from markdown import markdown  # type: ignore
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: markdown. Install with `pip install markdown` and re-run."
    ) from e

ROOT = Path(__file__).resolve().parent
md_path = ROOT / "PostgreSQL_Connection_Guide.md"
html_path = ROOT / "PostgreSQL_Connection_Guide.html"
pdf_path = ROOT / "PostgreSQL_Connection_Guide.pdf"

if not md_path.exists():
    raise SystemExit(f"Markdown guide not found at: {md_path}")

# Read markdown
md_text = md_path.read_text(encoding="utf-8")

# Convert to HTML
html_body = markdown(
    md_text,
    extensions=[
        "fenced_code",
        "tables",
        "toc",
        "codehilite",
        "sane_lists",
        "smarty",
    ],
)

# Basic styled HTML wrapper
html_doc = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SwasthVedha — PostgreSQL Connection Guide</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 40px; line-height: 1.6; }}
    code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
    pre {{ background: #f6f8fa; padding: 12px; border-radius: 6px; overflow-x: auto; }}
    code {{ background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }}
    h1, h2, h3 {{ color: #0f172a; }}
    hr {{ border: 0; border-top: 1px solid #e5e7eb; margin: 24px 0; }}
    table {{ border-collapse: collapse; }}
    th, td {{ border: 1px solid #e5e7eb; padding: 6px 10px; }}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_path.write_text(html_doc, encoding="utf-8")

# Locate Microsoft Edge
EDGE_CANDIDATES = [
    "msedge",  # if in PATH
    str(Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")),
    str(Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe")),
]
edge = next((p for p in EDGE_CANDIDATES if shutil.which(p) or Path(p).exists()), None)

if not edge:
    print(f"HTML written to {html_path}")
    print("Could not find Microsoft Edge. Open the HTML and use Print > Save as PDF.")
    raise SystemExit(0)

# Use Edge headless to print to PDF
html_uri = html_path.as_uri()
cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    "--no-first-run",
    f"--print-to-pdf={pdf_path}",
    html_uri,
]

print("Printing to PDF via Edge headless...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(res.stdout)
    print(res.stderr)
    print(f"HTML written to {html_path}")
    raise SystemExit("Edge headless print failed. Open the HTML and use Print > Save as PDF.")

if pdf_path.exists():
    print(f"PDF created: {pdf_path}")
else:
    print(f"Edge finished but PDF missing. HTML at: {html_path}")
