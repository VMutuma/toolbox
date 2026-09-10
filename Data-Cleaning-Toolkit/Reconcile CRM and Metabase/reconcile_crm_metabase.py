"""
reconcile_crm_metabase.py

Reconciles Zoho CRM "Deals" export against a Metabase export of
signup/deal data, and reports discrepancies.

Matching key:
    CRM `Record Id` (e.g. "zcrm_2914989000027675002")
      <-> Metabase `deal_id` (e.g. 2914989000027675002)
    matched by stripping the "zcrm_" prefix from the CRM id.

Note on currency:
    Metabase's `amount` column is in USD.
    Metabase's `original_amount` column is in the deal's local
    currency (TZS, KES, EUR, etc.) — NOT directly comparable to
    CRM `Deal Value`.
    CRM `Deal Value` is stored in USD, so it should be compared
    against Metabase `amount`, not `original_amount`. (Comparing
    against original_amount by mistake will produce thousands of
    false "mismatches" — check this first if totals look wrong.)

Usage:
    python reconcile_crm_metabase.py \
        --crm Deals_2026_09_10.csv \
        --metabase all_user_sign_ups_and_deal_details.csv \
        --outdir ./out

Outputs (written to --outdir):
    missing_in_crm.csv   - deals present in Metabase but not found in the CRM export
    stage_mismatch.csv   - deals where CRM stage != Metabase stage
    value_mismatch.csv   - deals where CRM Deal Value != Metabase USD amount (beyond tolerance)
    name_mismatch.csv    - deals where deal name differs (e.g. case differences)
    summary.txt          - counts + headline findings
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

VALUE_ABS_TOLERANCE = 0.05  # USD; flag only if the difference exceeds this


def load_crm(path: str) -> pd.DataFrame:
    deals = pd.read_csv(path)
    deals["numeric_id"] = deals["Record Id"].str.replace("zcrm_", "", regex=False)
    return deals


def load_metabase(path: str) -> pd.DataFrame:
    mb = pd.read_csv(path)
    mb["deal_id_str"] = mb["deal_id"].astype("Int64").astype(str)
    return mb


def dedupe_metabase_to_deal_level(mb: pd.DataFrame) -> pd.DataFrame:
    """Metabase rows are signup-level and can repeat the same deal_id
    (multiple signups can reference one deal). Collapse to one row
    per deal_id, keeping the deal-level fields."""
    cols = ["deal_id_str", "deal_name", "stage", "amount", "original_amount"]
    return (
        mb.dropna(subset=["deal_id"])
        .drop_duplicates(subset=["deal_id_str"])[cols]
        .copy()
    )


def check_metabase_internal_consistency(mb: pd.DataFrame) -> pd.DataFrame:
    """Sanity check: does any single deal_id show conflicting stage/amount
    across its Metabase signup rows? Should normally be empty."""
    grp = mb.dropna(subset=["deal_id"]).groupby("deal_id_str").agg(
        stage_nunique=("stage", "nunique"),
        amount_nunique=("amount", "nunique"),
    )
    return grp[(grp["stage_nunique"] > 1) | (grp["amount_nunique"] > 1)]


def reconcile(crm: pd.DataFrame, mb_deals: pd.DataFrame):
    merged = mb_deals.merge(
        crm[["numeric_id", "Deal Name", "Current Stage", "Deal Value"]],
        left_on="deal_id_str",
        right_on="numeric_id",
        how="left",
        indicator=True,
    )

    missing_in_crm = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

    both = merged[merged["_merge"] == "both"].copy()
    both["mb_usd"] = both["amount"].str.replace("USD", "", regex=False).astype(float)
    both["crm_value"] = pd.to_numeric(both["Deal Value"], errors="coerce")
    both["value_diff"] = (both["crm_value"] - both["mb_usd"]).abs()

    stage_mismatch = both[
        both["stage"].str.strip().str.lower()
        != both["Current Stage"].str.strip().str.lower()
    ][["deal_id_str", "deal_name", "stage", "Current Stage"]]

    name_mismatch = both[
        both["deal_name"].str.strip() != both["Deal Name"].str.strip()
    ][["deal_id_str", "deal_name", "Deal Name"]]

    value_mismatch = both[both["value_diff"] > VALUE_ABS_TOLERANCE][
        ["deal_id_str", "deal_name", "mb_usd", "crm_value", "value_diff"]
    ].sort_values("value_diff", ascending=False)

    return {
        "matched_count": len(both),
        "missing_in_crm": missing_in_crm,
        "stage_mismatch": stage_mismatch,
        "name_mismatch": name_mismatch,
        "value_mismatch": value_mismatch,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crm", required=True, help="Path to CRM Deals export CSV")
    parser.add_argument("--metabase", required=True, help="Path to Metabase export CSV")
    parser.add_argument("--outdir", default="./out", help="Directory for output CSVs")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    crm = load_crm(args.crm)
    mb = load_metabase(args.metabase)
    mb_deals = dedupe_metabase_to_deal_level(mb)

    internal_issues = check_metabase_internal_consistency(mb)
    if len(internal_issues):
        print(
            f"WARNING: {len(internal_issues)} deal_id(s) have conflicting "
            "stage/amount across Metabase rows. Investigate before trusting "
            "the deal-level comparison.",
            file=sys.stderr,
        )
        internal_issues.to_csv(outdir / "metabase_internal_inconsistencies.csv")

    results = reconcile(crm, mb_deals)

    results["missing_in_crm"].to_csv(outdir / "missing_in_crm.csv", index=False)
    results["stage_mismatch"].to_csv(outdir / "stage_mismatch.csv", index=False)
    results["name_mismatch"].to_csv(outdir / "name_mismatch.csv", index=False)
    results["value_mismatch"].to_csv(outdir / "value_mismatch.csv", index=False)

    summary_lines = [
        f"Metabase unique deals:      {len(mb_deals)}",
        f"CRM deals:                  {len(crm)}",
        f"Matched (both systems):     {results['matched_count']}",
        f"Missing from CRM export:    {len(results['missing_in_crm'])}",
        f"Stage mismatches:           {len(results['stage_mismatch'])}",
        f"Name mismatches:            {len(results['name_mismatch'])}",
        f"Value mismatches (>${VALUE_ABS_TOLERANCE}):   {len(results['value_mismatch'])}",
    ]
    summary = "\n".join(summary_lines)
    print(summary)
    (outdir / "summary.txt").write_text(summary + "\n")


if __name__ == "__main__":
    main()
