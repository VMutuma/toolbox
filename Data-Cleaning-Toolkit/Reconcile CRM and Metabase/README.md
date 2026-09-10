# CRM vs Metabase Reconciliation

A small Python script for comparing deal records exported from **Zoho CRM**
against a corresponding export from **Metabase**, and surfacing any
discrepancies between the two.

## What it does

- Matches records between the two exports using their shared deal ID
- Flags deals that exist in one system but not the other
- Flags mismatches in stage, name, and value between matching records
- Writes the results out as CSV files for easy review

## Usage

```bash
python reconcile_crm_metabase.py \
  --crm path/to/crm_export.csv \
  --metabase path/to/metabase_export.csv \
  --outdir ./out
```

## Output

Running the script produces a few CSV files in the output directory
(missing records, stage mismatches, name mismatches, value mismatches)
plus a short summary printed to the console.

## Notes

This was built for a specific internal export format, so column names
and matching logic may need adjusting for other setups. Treat it as a
starting point rather than a drop-in tool.
