"""
Process a batch of multi-sheet .xlsx workbooks into the consolidated hub.

For each sheet in each workbook, classify as:
  - SKIP_ALREADY_IN_HUB   : matches a sheet already added in an earlier
                             (CSV, single-sheet) pass -- identified by sheet
                             name matching the sheet that CSV was exported from
  - SKIP_EMPTY            : <=1 real (non-blank) row -- no data
  - SKIP_DUPLICATE        : byte-identical content to another sheet in this batch
  - SKIP_NEAR_DUPLICATE   : >=95% email overlap with another (richer) sheet
                             in this batch -- keeps the one with more columns
  - ADD                   : new, unique content -> written as its own tab

Sheet names are generated as "<workbook-prefix>-<sheet-slug>", sanitized and
truncated to Excel's 31-char limit, with numeric suffixes on collision.

Usage:
    python append_workbooks_batch.py --input-dir ./xlsx --workbook consolidated.xlsx
"""

import argparse
import glob
import hashlib
import os
import re

import openpyxl
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

MAX_SHEET_NAME_LEN = 31

# sheet name in each workbook that was already captured via a prior CSV export
ALREADY_IN_HUB = {
    "Beem___Customer_Success___Customer_Impact_Surveys___Customer_Lists.xlsx": ["Cheetahs"],
    "Beem_internal_email_contacts.xlsx": ["Tanzania 2"],
    "Email_drips_Emails___Enterprise_sales.xlsx": ["tours and travel companies"],
    "Healthcare_Vertical_Focus_Kenya.xlsx": ["Previous Data"],
    "Beem_-_Conferences_Trips_-_Enterprise_leads_-_2024.xlsx": ["Africa Fintech Summit 2024"],
    "Sales_Contacts.xlsx": ["Sheet1"],
    "Potential_Hopsitals_ISPs_.xlsx": ["HOSPITALS"],
    "Chemical___Construction_Company.xlsx": ["chemical & construction"],
    "Enterprise___Networking_Events_Data_2025.xlsx": ["SUBMIT TO MARKETING - DRIPS"],
    "Leads_-_Digital_Credit_Providers_-_Sharon_Mwangi.xlsx": ["List of DCPs"],
    "Beem__Marketing___ATS_outreach_2026.xlsx": ["Africa Fintech Summit 2024"],
    "Arusha_Agritech_Directory.xlsx": ["Arusha Agritech Directory"],
    "ABM_SALES_TEAM_PIPELINE.xlsx": ["List"],
    "Enterprise___Networking_Events_Data___2026.xlsx": ["Sacco Expo- Jan 26"],
}

WORKBOOK_PREFIX = {
    "Beem___Customer_Success___Customer_Impact_Surveys___Customer_Lists.xlsx": "custsuccess",
    "Beem_internal_email_contacts.xlsx": "intcontacts",
    "Email_drips_Emails___Enterprise_sales.xlsx": "drips",
    "Healthcare_Vertical_Focus_Kenya.xlsx": "hckenya",
    "Beem_-_Conferences_Trips_-_Enterprise_leads_-_2024.xlsx": "conftrips",
    "Sales_Contacts.xlsx": "sales",
    "Potential_Hopsitals_ISPs_.xlsx": "hospisps",
    "Chemical___Construction_Company.xlsx": "chemconstr",
    "Enterprise___Networking_Events_Data_2025.xlsx": "netev25",
    "Leads_-_Digital_Credit_Providers_-_Sharon_Mwangi.xlsx": "dcpsharon",
    "Beem__Marketing___ATS_outreach_2026.xlsx": "atsoutreach",
    "Arusha_Agritech_Directory.xlsx": "arusha",
    "ABM_SALES_TEAM_PIPELINE.xlsx": "abmpipe",
    "Enterprise___Networking_Events_Data___2026.xlsx": "netev26",
}


def real_extent(ws):
    max_row = 0
    max_col = 0
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None and str(cell.value).strip() != "":
                if cell.row > max_row:
                    max_row = cell.row
                if cell.column > max_col:
                    max_col = cell.column
    return max_row, max_col


def content_hash(ws, r, c):
    h = hashlib.md5()
    for row in ws.iter_rows(min_row=1, max_row=r, max_col=c, values_only=True):
        for v in row:
            h.update((str(v).strip() if v is not None else "").encode())
            h.update(b"|")
    return h.hexdigest()


def find_email_col(ws, r, c):
    for col in range(1, c + 1):
        header = ws.cell(row=1, column=col).value
        if header and "email" in str(header).lower():
            return col
    return None


def email_set(ws, r, c, email_col):
    out = set()
    for row in range(2, r + 1):
        v = ws.cell(row=row, column=email_col).value
        if v:
            out.add(str(v).strip().lower())
    return out


def slugify(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "-", name.strip())
    return name.lower()


def make_sheet_name(prefix: str, sheet: str, used: set) -> str:
    slug = f"{prefix}-{slugify(sheet)}"
    slug = slug[:MAX_SHEET_NAME_LEN]
    base, i = slug, 2
    while slug.lower() in used:
        suffix = f"-{i}"
        slug = base[: MAX_SHEET_NAME_LEN - len(suffix)] + suffix
        i += 1
    used.add(slug.lower())
    return slug


def write_raw_sheet(wb, sheet_name, ws_src, r, c):
    ws = wb.create_sheet(title=sheet_name)
    body_font = Font(name="Arial")
    widths = {}
    for row in ws_src.iter_rows(min_row=1, max_row=r, max_col=c):
        for cell in row:
            v = cell.value
            new_cell = ws.cell(row=cell.row, column=cell.column, value=v)
            new_cell.font = body_font
            widths[cell.column] = max(widths.get(cell.column, 0), len(str(v)) if v else 0)
    for col_idx, w in widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = min(w + 2, 60)


def update_index_sheet(wb, new_rows):
    if "index" not in wb.sheetnames:
        ws = wb.create_sheet(title="index", index=0)
        header_font = Font(name="Arial", bold=True)
        headers = ["Tab name", "Original filename", "Rows", "Columns", "Notes"]
        for c_idx, h in enumerate(headers, start=1):
            ws.cell(row=1, column=c_idx, value=h).font = header_font
    ws = wb["index"]
    next_row = ws.max_row + 1
    body_font = Font(name="Arial")
    for row in new_rows:
        for c_idx, value in enumerate(row, start=1):
            ws.cell(row=next_row, column=c_idx, value=value).font = body_font
        next_row += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--workbook", required=True)
    args = parser.parse_args()

    wb_out = openpyxl.load_workbook(args.workbook)
    used_names = {s.lower() for s in wb_out.sheetnames}

    files = sorted(glob.glob(os.path.join(args.input_dir, "*.xlsx")))

    # Pass 1: gather metadata for every sheet across all workbooks
    all_sheets = []  # dicts
    for f in files:
        fname = os.path.basename(f)
        wb = openpyxl.load_workbook(f, data_only=True)
        for s in wb.sheetnames:
            ws = wb[s]
            r, c = real_extent(ws)
            all_sheets.append({"file": fname, "sheet": s, "r": r, "c": c, "wb": wb})

    # Pass 2: classify
    seen_hashes = {}  # hash -> (file, sheet) first occurrence
    email_index = []  # (file, sheet, r, c, email_set) for near-dup detection
    results = []
    skipped_log = []

    for item in all_sheets:
        fname, sheet, r, c, wb = item["file"], item["sheet"], item["r"], item["c"], item["wb"]
        ws = wb[sheet]

        if fname in ALREADY_IN_HUB and sheet in ALREADY_IN_HUB[fname]:
            skipped_log.append((fname, sheet, "SKIP_ALREADY_IN_HUB"))
            continue
        if r <= 1:
            skipped_log.append((fname, sheet, "SKIP_EMPTY"))
            continue

        h = content_hash(ws, r, c)
        if h in seen_hashes:
            skipped_log.append((fname, sheet, f"SKIP_DUPLICATE of {seen_hashes[h]}"))
            continue

        # near-duplicate check via email overlap.
        # Uses overlap/union (Jaccard), not overlap/min: a small list that
        # happens to be fully contained in a much larger, unrelated list
        # (e.g. a handful of serial industry-event attendees) is NOT the
        # same source list -- Jaccard only scores high when the two sets
        # are genuinely close to the same size and mostly overlapping.
        email_col = find_email_col(ws, r, c)
        is_near_dup = False
        if email_col:
            this_emails = email_set(ws, r, c, email_col)
            MIN_SET_SIZE = 5  # below this, overlap is too easily coincidental
            if len(this_emails) >= MIN_SET_SIZE:
                for (of, os_, or_, oc_, oemails) in email_index:
                    if len(oemails) < MIN_SET_SIZE:
                        continue
                    inter = len(this_emails & oemails)
                    union = len(this_emails | oemails)
                    jaccard = inter / union if union else 0
                    if jaccard >= 0.85:
                        # keep whichever sheet actually has more data (more
                        # emails first, more columns as tiebreaker)
                        if (len(this_emails), c) <= (len(oemails), oc_):
                            skipped_log.append((fname, sheet, f"SKIP_NEAR_DUPLICATE of {of}/{os_}"))
                            is_near_dup = True
                            break
            if this_emails:
                email_index.append((fname, sheet, r, c, this_emails))

        if is_near_dup:
            continue

        seen_hashes[h] = f"{fname}/{sheet}"
        results.append(item)

    # Pass 3: write ADD sheets
    index_rows = []
    for item in results:
        fname, sheet, r, c, wb = item["file"], item["sheet"], item["r"], item["c"], item["wb"]
        prefix = WORKBOOK_PREFIX.get(fname, slugify(os.path.splitext(fname)[0])[:12])
        sheet_name = make_sheet_name(prefix, sheet, used_names)
        write_raw_sheet(wb_out, sheet_name, wb[sheet], r, c)
        index_rows.append([sheet_name, f"{fname} :: {sheet}", r, c, ""])
        print(f"ADD  {fname:60s} [{sheet:30s}] -> [{sheet_name}]  {r}x{c}")

    for fname, sheet, reason in skipped_log:
        print(f"SKIP {fname:60s} [{sheet:30s}]  {reason}")

    update_index_sheet(wb_out, index_rows)
    wb_out.save(args.workbook)

    print(f"\nAdded {len(results)} new sheets. Skipped {len(skipped_log)}.")
    print(f"Total sheets in workbook now: {len(wb_out.sheetnames)}")


if __name__ == "__main__":
    main()
