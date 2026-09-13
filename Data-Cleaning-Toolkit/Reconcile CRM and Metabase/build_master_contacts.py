"""
Build the standardized "master_contacts" tab from the 113 raw tabs in the
consolidated hub, using the reviewed column mapping (mapping_rows_final.json).

Design decisions locked in with the user before this was written:
  - Blank-header columns: dropped entirely (not carried into master)
  - Columns from tabs flagged "needs review" during mapping: kept, but the
    resulting master row is flagged (does not silently blend in)
  - Phone numbers: NEVER auto-split. Kenyan phone listings often drop the
    shared area-code prefix on subsequent numbers in a comma list
    (e.g. "020 3742907, 3744554" -- the second number is NOT a complete,
    dialable number on its own). Splitting would silently manufacture
    broken numbers. Kept as one raw text field.
  - Emails: split on separators (comma/semicolon/newline/" or ") ONLY if
    every resulting piece is a valid email address. If any piece fails
    validation (e.g. "y.sermah@gmail,com" -- a likely typo, not a list),
    the original value is kept whole and flagged for manual review rather
    than guessed at.
  - Rows with a valid email are deduplicated on (lowercased, trimmed)
    email. Rows with no email are NEVER matched to anything -- each stays
    its own row in the master sheet, per the user's explicit decision.
  - When two rows share an email but disagree on a field (e.g. different
    Company), we do NOT silently pick one -- the merged row keeps the
    first non-blank value and records every distinct alternative in a
    "Conflicts" column so nothing is silently lost or overwritten.
  - A completely blank Name is never guessed at -- flagged for manual
    review instead.
  - Raw tabs are left untouched; this only adds a new tab alongside them.

Usage:
    python build_master_contacts.py --workbook consolidated_data_hub.xlsx --mapping mapping_rows_final.json
"""

import argparse
import json
import re
from collections import defaultdict

import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SPLIT_RE = re.compile(r"[,;\n/&]| or ", flags=re.IGNORECASE)
ANGLE_BRACKET_RE = re.compile(r"^<(.+)>$")
TRAILING_ANNOTATION_RE = re.compile(r"^([^\s(]+@[^\s(]+)\s*\(.*\)\s*$")

MASTER_FIELDS = ["Name", "Email", "Phone", "Company", "Position", "Industry",
                  "Country", "Status", "Date Added", "Notes"]


def clean_email_piece(p: str) -> str:
    """Strip formatting noise around an otherwise-valid email:
    angle brackets ("<addr>") and trailing role annotations ("addr (Head of IT)").
    Does not touch anything else -- if the piece still isn't a bare valid
    email after this, it's left as-is and will fail validation (flagged),
    not guessed at further."""
    p = p.strip().rstrip(";").strip()
    m = ANGLE_BRACKET_RE.match(p)
    if m:
        p = m.group(1).strip()
    m = TRAILING_ANNOTATION_RE.match(p)
    if m:
        p = m.group(1).strip()
    return p


ANNOTATION_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z\s\-]{1,20}$")


def split_emails_safely(raw: str):
    """Return (list_of_valid_emails, was_split_cleanly, annotation).
    If the raw value can't be confidently split into all-valid emails,
    returns ([raw], False, "") so the caller keeps it whole and flags it.

    Special case: if splitting yields exactly one valid email and the
    remaining piece(s) are short, plain alphabetic words with no "@" and
    no digits (e.g. "verified", "unverified", "bounced") -- clearly a
    status annotation, not an attempted second email -- the single email
    is accepted and the annotation is preserved separately rather than
    causing the whole cell to be flagged."""
    raw = raw.strip()
    single = clean_email_piece(raw)
    if EMAIL_RE.match(single):
        return [single.lower()], True, ""
    parts = [clean_email_piece(p) for p in SPLIT_RE.split(raw) if p.strip()]
    if len(parts) > 1 and all(EMAIL_RE.match(p) for p in parts):
        return [p.lower() for p in parts], True, ""
    valid_parts = [p for p in parts if EMAIL_RE.match(p)]
    leftover = [p for p in parts if not EMAIL_RE.match(p)]
    if len(valid_parts) == 1 and leftover and all(ANNOTATION_WORD_RE.match(p) for p in leftover):
        return [valid_parts[0].lower()], True, "; ".join(leftover)
    return [raw], False, ""


def load_workbook_and_mapping(workbook_path, mapping_path):
    wb = openpyxl.load_workbook(workbook_path, data_only=True)
    mapping = json.load(open(mapping_path))
    tab_cols = defaultdict(list)
    for m in mapping:
        if m["decision"] != "DROP":
            tab_cols[m["tab"]].append(m)
    return wb, tab_cols


def extract_rows(wb, tab_cols):
    """Yield one dict per source data row, with MASTER_FIELDS populated
    from whichever columns that tab had mapped, plus bookkeeping fields."""
    for tab, cols in tab_cols.items():
        ws = wb[tab]
        header_row = cols[0]["header_row"]
        flagged_tab = any(c["decision"] == "KEEP - flag yellow in master" for c in cols)
        for r in range(header_row + 1, ws.max_row + 1):
            row_vals = {f: "" for f in MASTER_FIELDS}
            row_flagged = flagged_tab
            has_any_value = False
            for c in cols:
                v = ws.cell(row=r, column=c["column_index"]).value
                if v is None or str(v).strip() == "":
                    continue
                v = str(v).strip()
                has_any_value = True
                target = c["proposed_target"]
                if target == "Notes":
                    label = c["original_header"] or f"col{c['column_index']}"
                    row_vals["Notes"] = (row_vals["Notes"] + f" | {label}: {v}").strip(" |")
                else:
                    join_str = " " if target == "Name" else " ; "
                    if row_vals[target]:
                        row_vals[target] = row_vals[target] + join_str + v
                    else:
                        row_vals[target] = v
            if not has_any_value:
                continue
            yield {
                "source_tab": tab,
                "source_row": r,
                "flagged": row_flagged,
                "name_missing": row_vals["Name"] == "",
                **row_vals,
            }


def explode_emails(rows):
    """Split multi-email cells into separate logical rows where safe;
    otherwise keep the row's email field as-is and flag it."""
    out = []
    for row in rows:
        raw_email = row["Email"]
        if not raw_email:
            out.append({**row, "email_ambiguous": False})
            continue
        emails, clean, annotation = split_emails_safely(raw_email)
        base_notes = row["Notes"]
        if annotation:
            base_notes = (base_notes + f" | Email status: {annotation}").strip(" |")
        if clean and len(emails) > 1:
            for e in emails:
                out.append({**row, "Email": e, "Notes": base_notes, "email_ambiguous": False})
        elif clean:
            out.append({**row, "Email": emails[0], "Notes": base_notes, "email_ambiguous": False})
        else:
            out.append({**row, "Email": raw_email, "email_ambiguous": True})
    return out


def dedupe(rows):
    """Group rows sharing a valid, normalized email. Rows with no
    email (or an ambiguous un-split one) are never merged with anything."""
    groups = defaultdict(list)
    standalone = []
    for row in rows:
        e = row["Email"].strip().lower()
        if e and EMAIL_RE.match(e) and not row["email_ambiguous"]:
            groups[e].append(row)
        else:
            standalone.append(row)

    merged = []
    for email, group in groups.items():
        if len(group) == 1:
            merged.append(group[0])
            continue
        base = {f: "" for f in MASTER_FIELDS}
        base["Email"] = email
        conflicts = defaultdict(set)
        sources = []
        flagged = False
        name_missing = True
        for g in sorted(group, key=lambda x: (x["source_tab"], x["source_row"])):
            sources.append(f"{g['source_tab']}#{g['source_row']}")
            flagged = flagged or g["flagged"]
            name_missing = name_missing and g["name_missing"]
            for f in MASTER_FIELDS:
                if f == "Email":
                    continue
                v = g[f]
                if not v:
                    continue
                if not base[f]:
                    base[f] = v
                elif base[f] != v:
                    conflicts[f].add(v)
        conflict_notes = "; ".join(f"{f}: also seen {sorted(vals)}" for f, vals in conflicts.items())
        if conflict_notes:
            base["Notes"] = (base["Notes"] + f" | CONFLICTS: {conflict_notes}").strip(" |")
        base["source_tab"] = "; ".join(sorted(set(s.split('#')[0] for s in sources)))
        base["source_row"] = "; ".join(sources)
        base["flagged"] = flagged
        base["name_missing"] = name_missing
        base["email_ambiguous"] = False
        merged.append(base)

    return merged + standalone


def write_master_sheet(wb, rows):
    if "master_contacts" in wb.sheetnames:
        del wb["master_contacts"]
    ws = wb.create_sheet("master_contacts", index=1)

    headers = MASTER_FIELDS + ["Source Tab(s)", "Source Row(s)", "Needs Review", "Review Reason"]
    header_font = Font(name="Arial", bold=True)
    body_font = Font(name="Arial")
    yellow = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    for c_idx, h in enumerate(headers, start=1):
        ws.cell(row=1, column=c_idx, value=h).font = header_font

    r_idx = 2
    for row in rows:
        reasons = []
        if row.get("name_missing"):
            reasons.append("Missing name")
        if row.get("flagged"):
            reasons.append("From a review-flagged source column")
        if row.get("email_ambiguous"):
            reasons.append("Email value could not be safely split/validated")
        if "CONFLICTS" in row.get("Notes", ""):
            reasons.append("Conflicting values across sources")

        vals = [row.get(f, "") for f in MASTER_FIELDS] + [
            row.get("source_tab", ""), str(row.get("source_row", "")),
            "YES" if reasons else "", "; ".join(reasons)
        ]
        needs_review = bool(reasons)
        for c_idx, v in enumerate(vals, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=v)
            cell.font = body_font
            if needs_review:
                cell.fill = yellow
        r_idx += 1

    widths = [22, 30, 30, 25, 20, 18, 14, 12, 14, 45, 40, 20, 10, 45]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{r_idx-1}"
    return r_idx - 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--mapping", required=True)
    args = parser.parse_args()

    wb, tab_cols = load_workbook_and_mapping(args.workbook, args.mapping)
    rows = list(extract_rows(wb, tab_cols))
    print(f"Extracted {len(rows)} raw rows from {len(tab_cols)} tabs")

    rows = explode_emails(rows)
    print(f"After safe email splitting: {len(rows)} rows")

    final_rows = dedupe(rows)
    print(f"After email-based dedup: {len(final_rows)} rows")

    n_written = write_master_sheet(wb, final_rows)
    wb.save(args.workbook)

    n_flagged = sum(1 for r in final_rows if r.get("flagged") or r.get("name_missing")
                     or r.get("email_ambiguous") or "CONFLICTS" in r.get("Notes",""))
    print(f"\nWrote master_contacts: {n_written} rows, {n_flagged} flagged for review")


if __name__ == "__main__":
    main()
