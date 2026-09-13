"""
Append a batch of heterogeneous, messy CSVs into the consolidated workbook
as new tabs -- raw, exactly as exported, no header-row guessing, no
reshaping. Each source keeps its own tab; an "index" tab is written/updated
listing tab name, original filename, dimensions, and any notes (e.g.
detected near-duplicate content between sources).

Why raw (header=None)?
Several of these exports have blank leading rows or title rows before the
real header (e.g. a spreadsheet's merged title cell exported as its own
row). Assuming row 1 is the header would silently eat that row. Reading
every file as a plain, headerless grid guarantees nothing is lost or
misinterpreted before the standardization pass.

Usage:
    python append_batch.py --input-dir ./csvs --workbook consolidated.xlsx --manifest manifest.py
"""

import argparse
import importlib.util
import os

import openpyxl
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

MAX_SHEET_NAME_LEN = 31


def load_manifest(path: str):
    spec = importlib.util.spec_from_file_location("manifest", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MANIFEST, getattr(mod, "SKIPPED", [])


def autofit_columns(ws, ncols: int, widths, max_width: int = 60):
    for idx in range(1, ncols + 1):
        col_letter = get_column_letter(idx)
        ws.column_dimensions[col_letter].width = min(widths.get(idx, 10) + 2, max_width)


def write_raw_sheet(wb, sheet_name: str, csv_path: str) -> tuple:
    df = pd.read_csv(csv_path, header=None, dtype=str, keep_default_na=False)
    ws = wb.create_sheet(title=sheet_name)
    body_font = Font(name="Arial")
    widths = {}
    for r_idx, row in enumerate(df.itertuples(index=False), start=1):
        for c_idx, value in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value if value != "" else None)
            cell.font = body_font
            widths[c_idx] = max(widths.get(c_idx, 0), len(str(value)))
    autofit_columns(ws, df.shape[1], widths)
    return df.shape


def update_index_sheet(wb, rows):
    if "index" in wb.sheetnames:
        del wb["index"]
    ws = wb.create_sheet(title="index", index=0)
    header_font = Font(name="Arial", bold=True)
    body_font = Font(name="Arial")

    headers = ["Tab name", "Original filename", "Rows", "Columns", "Notes"]
    for c_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=c_idx, value=h)
        cell.font = header_font

    for r_idx, row in enumerate(rows, start=2):
        for c_idx, value in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            cell.font = body_font

    widths = [28, 60, 8, 8, 70]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--workbook", required=True, help="Existing workbook to append to")
    parser.add_argument("--manifest", required=True, help="Path to manifest.py defining MANIFEST and SKIPPED")
    args = parser.parse_args()

    manifest, skipped = load_manifest(args.manifest)
    wb = openpyxl.load_workbook(args.workbook)

    index_rows = []
    # Preserve any existing tabs already in the index, if present
    if "index" in wb.sheetnames:
        existing = wb["index"]
        for row in existing.iter_rows(min_row=2, values_only=True):
            if row[0]:
                index_rows.append(list(row))

    for filename, sheet_name, note in manifest:
        path = os.path.join(args.input_dir, filename)
        used = {s.lower() for s in wb.sheetnames}
        name = sheet_name[:MAX_SHEET_NAME_LEN]
        if name.lower() in used:
            print(f"WARNING: sheet name collision for {name!r}, skipping {filename}")
            continue
        shape = write_raw_sheet(wb, name, path)
        index_rows.append([name, filename, shape[0], shape[1], note])
        print(f"Added: {filename} -> [{name}]  ({shape[0]} rows x {shape[1]} cols)")

    for filename, note in skipped:
        print(f"Skipped: {filename} -- {note}")

    update_index_sheet(wb, index_rows)
    wb.save(args.workbook)
    print(f"\nSaved {args.workbook} with {len(wb.sheetnames)} sheets total (incl. index).")


if __name__ == "__main__":
    main()
