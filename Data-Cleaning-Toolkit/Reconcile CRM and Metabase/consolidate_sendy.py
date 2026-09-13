"""
Consolidate multiple Sendy campaign-export CSVs into a single Excel
workbook, one tab per source file. No standardization/dedup is applied
at this stage -- each tab is an exact copy of its source CSV's headers
and rows, so nothing is lost or reshaped before that decision is made.

Usage:
    python consolidate_sendy.py --input-dir ./csvs --output consolidated.xlsx
"""

import argparse
import glob
import os

import openpyxl
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

MAX_SHEET_NAME_LEN = 31
INVALID_SHEET_CHARS = set(r"[]:*?/\\")


def safe_sheet_name(filename: str, used_names: set) -> str:
    """Derive a valid, unique Excel sheet name from a CSV filename."""
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name[:-4] if name.endswith("-all") else name  # drop trailing "-all"
    name = "".join(c for c in name if c not in INVALID_SHEET_CHARS)
    name = name[:MAX_SHEET_NAME_LEN] or "sheet"

    original = name
    i = 2
    while name in used_names:
        suffix = f"_{i}"
        name = original[: MAX_SHEET_NAME_LEN - len(suffix)] + suffix
        i += 1
    used_names.add(name)
    return name


def autofit_columns(ws, df: pd.DataFrame, max_width: int = 60):
    for idx, col in enumerate(df.columns, start=1):
        col_letter = get_column_letter(idx)
        longest = max(
            [len(str(col))] + [len(str(v)) for v in df[col].astype(str).values]
        )
        ws.column_dimensions[col_letter].width = min(longest + 2, max_width)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, help="Folder containing the source CSVs")
    parser.add_argument("--pattern", default="*.csv", help="Glob pattern for source files (default: *.csv)")
    parser.add_argument("--output", required=True, help="Path to write the consolidated .xlsx")
    args = parser.parse_args()

    csv_paths = sorted(glob.glob(os.path.join(args.input_dir, args.pattern)))
    if not csv_paths:
        raise SystemExit(f"No CSV files found in {args.input_dir} matching {args.pattern}")

    used_names = set()
    summary = []

    with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
        for path in csv_paths:
            df = pd.read_csv(path, dtype=str)  # keep everything as text, no reformatting
            sheet_name = safe_sheet_name(path, used_names)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            summary.append((path, sheet_name, len(df)))

    # Post-process formatting: bold headers, readable column widths
    wb = openpyxl.load_workbook(args.output)
    header_font = Font(name="Arial", bold=True)
    body_font = Font(name="Arial")

    for path, sheet_name, _ in summary:
        ws = wb[sheet_name]
        df = pd.read_csv(path, dtype=str)
        for cell in ws[1]:
            cell.font = header_font
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.font = body_font
        autofit_columns(ws, df)

    wb.save(args.output)

    print(f"Wrote {len(summary)} sheets to {args.output}\n")
    print(f"{'Source file':45s} {'Sheet name':32s} Rows")
    for src, sheet, n in summary:
        print(f"{os.path.basename(src):45s} {sheet:32s} {n}")
    print(f"\nTotal rows across all sheets: {sum(n for _, _, n in summary)}")


if __name__ == "__main__":
    main()
