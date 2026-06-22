import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
from datetime import datetime

# Suppress specific FutureWarnings from seaborn/matplotlib if they don't impede functionality
warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")
warnings.filterwarnings("ignore", category=UserWarning, module="xlsxwriter") # Suppress sheetname warnings

# Set a style for plots for better aesthetics
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)

# Function to save plots with clean filenames
def save_plot(fig, title):
    filename = re.sub(r'[\\/*?:"<>|]', '', title)
    filename = filename.replace(' ', '_').lower() + '.png'
    try:
        fig.savefig(filename, bbox_inches='tight', dpi=300)
        print(f"Plot saved: {filename}")
    except Exception as e:
        print(f"Error saving plot {filename}: {e}")
    plt.close(fig)

# --- Data Loading and Initial Preparation (crm_data.csv) ---
print("--- Data Loading and Initial Preparation (crm_data.csv) ---")
try:
    # Assuming 'crm_data.csv' is in the same directory as this script
    df = pd.read_csv('crm_data.csv', sep=';', quotechar='"')
    df.drop(columns=['id.1', 'user_id.1'], inplace=True, errors='ignore')

    def extract_usd_amount(amount_str):
        if isinstance(amount_str, str):
            match = re.search(r'USD\s*([\d.]+)', amount_str)
            if match:
                return float(match.group(1))
        return np.nan

    df['amount_usd'] = df['amount'].apply(extract_usd_amount)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce')

    # Calculate deal_duration more accurately by checking for valid date range
    df['deal_duration'] = (df['updated_at'] - df['created_at']).dt.days

    # Ensure updated_at is not before created_at, or if it is, set duration to NaN for calculation safety.
    df.loc[df['deal_duration'] < 0, 'deal_duration'] = np.nan


    df['utm_source_cleaned'] = df['utm_source'].fillna('Organic Traffic').replace('(not set)', 'Unknown').str.lower()
    df['utm_medium'] = df['utm_medium'].fillna('Unknown').replace('(not set)', 'Unknown').str.lower()
    df['utm_campaign'] = df['utm_campaign'].fillna('Unknown').replace('(not set)', 'Unknown').str.lower()
    df['stage'] = df['stage'].replace('(not set)', 'Unknown').str.title() # Capitalize first letter

    df['created_quarter'] = df['created_at'].dt.to_period('Q')
    df['created_quarter_str'] = df['created_quarter'].astype(str)
    df['created_year'] = df['created_at'].dt.year

    # Define a threshold for high-value deals (e.g., top 5% of deals by value)
    high_value_threshold = df['amount_usd'].quantile(0.95) if not df['amount_usd'].dropna().empty else 0
    df['is_high_value'] = df['amount_usd'] >= high_value_threshold
    print(f"High-value deal threshold set at: ${high_value_threshold:,.2f} (Top 5% by amount_usd)")

    print("DataFrame initialized and essential columns prepared.")
    print(f"Total deals in dataset: {len(df)}")
except Exception as e:
    print(f"Error initializing DataFrame: {e}. Please ensure 'crm_data.csv' is accessible and correctly formatted.")
    # Exit or handle gracefully if file is missing - for this context, we will exit if the core CRM data isn't loaded
    exit()

# Filter for closed won deals
df_closed_won = df[df['stage'] == 'Closed Won'].copy()

# --- Process 2025 Ad Spend Data (Using ALL 27 weeks of provided data) ---
print("\n--- Processing 2025 Ad Spend Data (Using ALL 27 weeks of provided data) ---")

# User provided ad spend data as a string
ad_spend_string = "$192.94$218.04$249.00$256.70$230.98$262.93$338.08$242.72$227.71$218.13$203.04$209.52$198.30$210.40$205.28$94.10$118.06$103.97$184.79$206.69$210.28$202.73$217.84$305.32$315.39$309.53$302.12"

# Use regex to find all dollar amounts and convert them to floats
weekly_ad_spend_values_actual = [float(s.replace('$', '')) for s in re.findall(r'\$\d+\.?\d*', ad_spend_string)]

# Calculate total ad spend for the provided weeks
total_ad_spend_2025_ytd = sum(weekly_ad_spend_values_actual)
num_actual_weeks_provided = len(weekly_ad_spend_values_actual)
target_week_for_ytd = 27 # As specified by user (up to week 27)

if num_actual_weeks_provided != target_week_for_ytd:
    print(f"Warning: Expected {target_week_for_ytd} weeks of data, but received {num_actual_weeks_provided}. Using provided {num_actual_weeks_provided} weeks for YTD calculation.")
    target_week_for_ytd = num_actual_weeks_provided

print(f"Total Actual Ad Spend for {num_actual_weeks_provided} weeks: ${total_ad_spend_2025_ytd:,.2f}")

# --- Calculate 2025 YTD Combined ROI (Closed Won Deals) ---
print("\n--- Calculating 2025 YTD Combined ROI (Closed Won Deals) ---")

def calculate_roi(revenue, cost):
    if cost > 0:
        return ((revenue - cost) / cost) * 100
    return np.inf if revenue > 0 else 0 # Infinite ROI if cost is zero and there's revenue, else 0 if no revenue and no cost

# Define the current date for YTD calculation (July 10, 2025)
current_date_2025_ytd = datetime(2025, 7, 10)

# Filter closed won deals for 2025 YTD
df_closed_won_2025_ytd = df_closed_won[
    (df_closed_won['created_year'] == 2025) &
    (df_closed_won['created_at'] <= current_date_2025_ytd)
].copy()

total_revenue_closed_won_2025_ytd = df_closed_won_2025_ytd['amount_usd'].sum()

# Combined ROI for 2025 YTD
combined_roi_2025_ytd = calculate_roi(total_revenue_closed_won_2025_ytd, total_ad_spend_2025_ytd)

print(f"Total Closed Won Revenue YTD 2025 (up to {current_date_2025_ytd.strftime('%B %d, %Y')}): ${total_revenue_closed_won_2025_ytd:,.2f}")
print(f"Combined ROI for 2025 YTD (Closed Won Deals): {combined_roi_2025_ytd:,.2f}%")


# --- Calculate Quarterly ROI for 2025 (Closed Won Deals) ---
print("\n--- Calculating Quarterly ROI for 2025 (Closed Won Deals) ---")

# Distribute ad spend into quarters based on 27 weeks of data
# Assumption: Q1 (Weeks 1-13), Q2 (Weeks 14-26), Q3 (Week 27)
quarterly_ad_spend_2025 = {
    '2025Q1': sum(weekly_ad_spend_values_actual[0:13]), # Weeks 1-13
    '2025Q2': sum(weekly_ad_spend_values_actual[13:26]), # Weeks 14-26
    '2025Q3': sum(weekly_ad_spend_values_actual[26:num_actual_weeks_provided]) # Week 27 (if data up to week 27)
}
print(f"Estimated Quarterly Ad Spend 2025: {quarterly_ad_spend_2025}")

# Filter closed won deals for 2025 and create quarter string for grouping
df_closed_won_2025 = df_closed_won[df_closed_won['created_year'] == 2025].copy()
df_closed_won_2025['created_quarter_str'] = df_closed_won_2025['created_at'].dt.to_period('Q').astype(str)

# Group by quarter to get revenue
quarterly_revenue_2025 = df_closed_won_2025.groupby('created_quarter_str')['amount_usd'].sum().to_dict()
print(f"Quarterly Closed Won Revenue 2025: {quarterly_revenue_2025}")

quarterly_roi_data = []
for quarter, ad_spend in quarterly_ad_spend_2025.items():
    # Ensure revenue exists for the quarter, otherwise default to 0
    revenue = quarterly_revenue_2025.get(quarter, 0)
    roi = calculate_roi(revenue, ad_spend)
    quarterly_roi_data.append({
        'Quarter': quarter,
        'Ad Spend (USD)': ad_spend,
        'Revenue (USD)': revenue,
        'ROI (%)': roi
    })

quarterly_roi_df = pd.DataFrame(quarterly_roi_data)
print("\n2025 Quarterly ROI Data (Closed Won Deals):")
print(quarterly_roi_df.to_string(index=False))

# --- Prepare Data for "2025 High-Level Overview" Tab ---
print("\n--- Preparing '2025 High-Level Overview' Data ---")

total_deals_closed_won_2025_ytd = len(df_closed_won_2025_ytd)
# total_revenue_closed_won_2025_ytd is already calculated above
avg_deal_size_2025_ytd = df_closed_won_2025_ytd['amount_usd'].mean() if total_deals_closed_won_2025_ytd > 0 else 0

overview_2025_data = {
    "Metric": [
        "Period Covered",
        "Total Ad Spend (USD) YTD 2025",
        "Total Closed Won Revenue (USD) YTD 2025", # Combined revenue
        "Combined ROI (%) YTD 2025", # Combined ROI
        "Total Deals Closed Won YTD 2025",
        "Average Closed Won Deal Size (USD) YTD 2025"
    ],
    "Value": [
        f"January 1, 2025 - {current_date_2025_ytd.strftime('%B %d, %Y')} (Week 1 - Week {target_week_for_ytd})",
        total_ad_spend_2025_ytd,
        total_revenue_closed_won_2025_ytd,
        combined_roi_2025_ytd,
        total_deals_closed_won_2025_ytd,
        avg_deal_size_2025_ytd
    ]
}
overview_2025_df = pd.DataFrame(overview_2025_data)


# --- Visualizations for Presentation (PNGs) ---
print("\n--- Generating Visualizations for Presentation (PNGs) ---")

# Funnel Chart (simulated as bar plot for stages)
fig_funnel = plt.figure(figsize=(10, 7))
sns.barplot(x='total_deals', y='stage', data=stage_funnel, palette='coolwarm')
plt.title('Deal Volume by Stage (Overall Funnel)')
plt.xlabel('Total Deals')
plt.ylabel('Deal Stage')
plt.tight_layout()
save_plot(fig_funnel, 'Deal Volume by Stage Overall Funnel')

# Closed Won Deal Sizes Histogram
if not closed_won_deal_sizes.empty:
    fig_hist = plt.figure(figsize=(10, 6))
    sns.histplot(closed_won_deal_sizes, bins=30, kde=True)
    plt.title('Distribution of Closed Won Deal Sizes (USD)')
    plt.xlabel('Deal Amount (USD)')
    plt.ylabel('Number of Deals')
    plt.ticklabel_format(style='plain', axis='x')
    plt.tight_layout()
    save_plot(fig_hist, 'Distribution of Closed Won Deal Sizes')
else:
    print("Skipping 'Distribution of Closed Won Deal Sizes' plot as data is empty.")

# Deal Duration Box Plot (Closed Won)
# Only plot if there's variation and not all 0s
if not overall_deal_duration_dist.empty and overall_deal_duration_dist.max() > 0:
    fig_boxplot = plt.figure(figsize=(10, 6))
    sns.boxplot(y=overall_deal_duration_dist)
    plt.title('Distribution of Deal Duration for Closed Won Deals (Days)')
    plt.ylabel('Deal Duration (Days)')
    plt.tight_layout()
    save_plot(fig_boxplot, 'Distribution of Deal Duration Closed Won')
else:
    print("Skipping 'Distribution of Deal Duration Closed Won' plot as data is empty or all zero.")

# Treemap for UTM Source & Medium (Revenue)
# Requires squarify library: pip install squarify
try:
    import squarify
    if not utm_source_medium_combined.empty:
        fig_treemap = plt.figure(figsize=(16, 10))
        # Plot only if total_amount_usd is not 0 for labels
        sizes = utm_source_medium_combined['total_amount_usd']
        labels = utm_source_medium_combined.apply(
            lambda x: f"{x['utm_source_cleaned']}\n({x['utm_medium']})\n${x['total_amount_usd']:,.0f}", axis=1
        )
        # Filter out labels for zero sizes to avoid errors or ugly plots
        filtered_labels = [label for i, label in enumerate(labels) if sizes.iloc[i] > 0]
        filtered_sizes = sizes[sizes > 0]

        if not filtered_sizes.empty:
            squarify.plot(sizes=filtered_sizes, label=filtered_labels,
                            alpha=0.8, pad=True, text_kwargs={'fontsize': 8, 'wrap': True})
            plt.title('Revenue Contribution by UTM Source & Medium (Top Sources)')
            plt.axis('off')
            plt.tight_layout()
            save_plot(fig_treemap, 'Revenue Contribution by UTM Source and Medium Treemap')
        else:
            print("Skipping Treemap: No positive revenue values after filtering for top sources.")
    else:
        print("Skipping Treemap: utm_source_medium_combined is empty.")

except ImportError:
    print("Skipping Treemap: 'squarify' library not found. Install it with 'pip install squarify'.")
except Exception as e:
    print(f"Error generating Treemap: {e}")

# NEW: 2025 Quarterly ROI Visualization
if not quarterly_roi_df.empty:
    fig_quarterly_roi = plt.figure(figsize=(10, 6))
    sns.barplot(x='Quarter', y='ROI (%)', data=quarterly_roi_df, palette='viridis')
    plt.title('2025 Quarterly ROI (Closed Won Deals)')
    plt.xlabel('Quarter')
    plt.ylabel('ROI (%)')
    plt.ylim(bottom=0) # Ensure y-axis starts at 0 or below if negative ROI

    # Add ROI values on top of bars
    for index, row in quarterly_roi_df.iterrows():
        # Adjust vertical alignment for negative ROI
        va = 'top' if row['ROI (%)'] < 0 else 'bottom'
        plt.text(index, row['ROI (%)'], f"{row['ROI (%)']:.2f}%", color='black', ha="center", va=va)

    plt.tight_layout()
    save_plot(fig_quarterly_roi, '2025 Quarterly ROI Closed Won Deals')
else:
    print("Skipping '2025 Quarterly ROI' plot as data is empty.")

print("PNG visualizations generated and saved.")


# --- Exporting all summaries AND embedding charts to Excel ---
output_excel_file = 'crm_elite_analysis.xlsx'

with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
    workbook = writer.book

    # --- 1. Summary Dashboard ---
    summary_data = {
        "Metric": ["Total Deals in CRM", "Total Revenue in CRM ($)", "Average Deal Size in CRM ($)",
                   "Total Deals Closed Won", "Total Revenue Closed Won ($)", "Average Closed Won Deal Size ($)",
                   "High-Value Deal Threshold ($)"],
        "Value": [len(df), df['amount_usd'].sum(), df['amount_usd'].mean(),
                  len(df_closed_won), df_closed_won['amount_usd'].sum(), df_closed_won['amount_usd'].mean(),
                  high_value_threshold]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary Dashboard', index=False)
    summary_ws = writer.sheets['Summary Dashboard']
    summary_ws.set_column('A:A', 30) # Widen column for readability
    summary_ws.set_column('B:B', 20)

    # --- NEW: 2025 High-Level Overview Tab ---
    if not overview_2025_df.empty:
        overview_2025_df.to_excel(writer, sheet_name='2025 High-Level Overview', index=False)
        overview_2025_ws = writer.sheets['2025 High-Level Overview']
        overview_2025_ws.set_column('A:A', 45) # Metric column
        overview_2025_ws.set_column('B:B', 25) # Value column

        # Add notes for clarity on data sources
        overview_2025_ws.write_comment('A1', f'This overview presents Year-To-Date (YTD) data for 2025, up to July 10, 2025 (Week 1 - Week {num_actual_weeks_provided}).')
        overview_2025_ws.write_comment('A2', f'Total Ad Spend for 2025 YTD is based on actual provided data for {num_actual_weeks_provided} weeks.')

        # Add Quarterly ROI data below the YTD overview
        start_row_quarterly_data = overview_2025_df.shape[0] + 2
        overview_2025_ws.write_string(start_row_quarterly_data, 0, "2025 Quarterly ROI Breakdown:")
        if not quarterly_roi_df.empty:
            quarterly_roi_df.to_excel(writer, sheet_name='2025 High-Level Overview', startrow=start_row_quarterly_data + 1, index=False)
            # Embed the quarterly ROI chart
            if fig_quarterly_roi: # Check if the figure was created
                chart_quarterly_roi = workbook.add_chart({'type': 'column'})
                num_q_rows = len(quarterly_roi_df)
                chart_quarterly_roi.add_series({
                    'name':       "='2025 High-Level Overview'!$D$" + str(start_row_quarterly_data + 2), # 'ROI (%)' header
                    'categories': "='2025 High-Level Overview'!$A$" + str(start_row_quarterly_data + 3) + ":$A$" + str(start_row_quarterly_data + 2 + num_q_rows), # Quarter categories
                    'values':     "='2025 High-Level Overview'!$D$" + str(start_row_quarterly_data + 3) + ":$D$" + str(start_row_quarterly_data + 2 + num_q_rows), # ROI values
                    'data_labels': {'value': True, 'num_format': '0.00"%'}, # Format as percentage
                })
                chart_quarterly_roi.set_title({'name': '2025 Quarterly ROI (Closed Won Deals)'})
                chart_quarterly_roi.set_x_axis({'name': 'Quarter'})
                chart_quarterly_roi.set_y_axis({'name': 'ROI (%)'})
                chart_quarterly_roi.set_size({'width': 720, 'height': 432})
                overview_2025_ws.insert_chart(f'F{start_row_quarterly_data + 1}', chart_quarterly_roi)
            else:
                print("Quarterly ROI chart was not generated, skipping embedding in Excel.")
        else:
            overview_2025_ws.write_string(start_row_quarterly_data + 1, 0, "No quarterly ROI data available for 2025.")
    else:
        print("Skipping '2025 High-Level Overview' sheet as data is empty.")


    # --- 2. Quarterly Trends ---
    quarterly_performance.to_excel(writer, sheet_name='Quarterly Trends', index=False)
    quarterly_stage_pivot.to_excel(writer, sheet_name='Quarterly Trends', startrow=quarterly_performance.shape[0] + 2, index=False)
    qt_ws = writer.sheets['Quarterly Trends']

    # Chart: Total Deals Over Quarters (Line)
    if not quarterly_performance.empty:
        chart_qt_deals = workbook.add_chart({'type': 'line'})
        num_rows = len(quarterly_performance)
        chart_qt_deals.add_series({
            'name':       "='Quarterly Trends'!$B$1", # total_deals
            'categories': "='Quarterly Trends'!$D$2:$D$" + str(num_rows + 1), # created_quarter_str
            'values':     "='Quarterly Trends'!$B$2:$B$" + str(num_rows + 1),
            'marker': {'type': 'automatic'},
        })
        chart_qt_deals.set_title({'name': 'Total Deals Over Quarters'})
        chart_qt_deals.set_x_axis({'name': 'Quarter'})
        chart_qt_deals.set_y_axis({'name': 'Number of Deals'})
        chart_qt_deals.set_size({'width': 720, 'height': 432})
        qt_ws.insert_chart('F2', chart_qt_deals)

        # Chart: Total Revenue Over Quarters (Line)
        chart_qt_revenue = workbook.add_chart({'type': 'line'})
        chart_qt_revenue.add_series({
            'name':       "='Quarterly Trends'!$C$1", # total_amount_usd
            'categories': "='Quarterly Trends'!$D$2:$D$" + str(num_rows + 1),
            'values':     "='Quarterly Trends'!$C$2:$C$" + str(num_rows + 1),
            'marker': {'type': 'automatic'},
            'data_labels': {'value': True, 'num_format': '$#,##0'},
        })
        chart_qt_revenue.set_title({'name': 'Total Revenue Over Quarters (USD)'})
        chart_qt_revenue.set_x_axis({'name': 'Quarter'})
        chart_qt_revenue.set_y_axis({'name': 'Total Revenue (USD)'})
        chart_qt_revenue.set_size({'width': 720, 'height': 432})
        qt_ws.insert_chart('F25', chart_qt_revenue) # Position below the first chart

        # Chart: Deal Count by Stage Over Quarters (Stacked Column)
        if not quarterly_stage_pivot.empty:
            chart_qt_stage_stacked = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
            num_stage_rows = len(quarterly_stage_pivot)
            col_offset = 1 # Column A is 'created_quarter_str'
            for i, stage_name in enumerate(quarterly_stage_pivot.columns[1:]): # Iterate over stage columns
                chart_qt_stage_stacked.add_series({
                    'name':       f"='Quarterly Trends'!${chr(65 + col_offset + i)}${quarterly_performance.shape[0] + 3}", # Column header for stage
                    'categories': f"='Quarterly Trends'!$A${quarterly_performance.shape[0] + 4}:$A${quarterly_performance.shape[0] + 3 + num_stage_rows}", # created_quarter_str
                    'values':     f"='Quarterly Trends'!${chr(65 + col_offset + i)}${quarterly_performance.shape[0] + 4}:${chr(65 + col_offset + i)}${quarterly_performance.shape[0] + 3 + num_stage_rows}", # Deal Counts
                })
            chart_qt_stage_stacked.set_title({'name': 'Deal Count by Stage Over Quarters'})
            chart_qt_stage_stacked.set_x_axis({'name': 'Quarter'})
            chart_qt_stage_stacked.set_y_axis({'name': 'Number of Deals'})
            chart_qt_stage_stacked.set_size({'width': 1000, 'height': 600})
            qt_ws.insert_chart('F48', chart_qt_stage_stacked)
        else:
            print("Skipping 'Deal Count by Stage Over Quarters' chart due to empty data.")
    else:
        print("Skipping 'Quarterly Trends' charts due to empty data.")

    # --- 3. Funnel Breakdown ---
    funnel_summary_df.to_excel(writer, sheet_name='Funnel Breakdown', index=False)
    stage_funnel.to_excel(writer, sheet_name='Funnel Breakdown', startrow=funnel_summary_df.shape[0] + 2, index=False)
    fb_ws = writer.sheets['Funnel Breakdown']
    fb_ws.set_column('A:A', 40)
    fb_ws.set_column('B:B', 20)

    # Chart: Deals and Revenue by Stage (Column)
    if not stage_funnel.empty:
        chart_funnel_stage = workbook.add_chart({'type': 'column'})
        num_rows = len(stage_funnel)
        chart_funnel_stage.add_series({
            'name':       "='Funnel Breakdown'!$B$" + str(funnel_summary_df.shape[0] + 3), # total_deals header
            'categories': "='Funnel Breakdown'!$A$" + str(funnel_summary_df.shape[0] + 4) + ":$A$" + str(funnel_summary_df.shape[0] + 3 + num_rows), # stages
            'values':     "='Funnel Breakdown'!$B$" + str(funnel_summary_df.shape[0] + 4) + ":$B$" + str(funnel_summary_df.shape[0] + 3 + num_rows), # total_deals
            'data_labels': {'value': True},
        })
        chart_funnel_stage.add_series({
            'name':       "='Funnel Breakdown'!$C$" + str(funnel_summary_df.shape[0] + 3), # total_amount_usd header
            'categories': "='Funnel Breakdown'!$A$" + str(funnel_summary_df.shape[0] + 4) + ":$A$" + str(funnel_summary_df.shape[0] + 3 + num_rows),
            'values':     "='Funnel Breakdown'!$C$" + str(funnel_summary_df.shape[0] + 4) + ":$C$" + str(funnel_summary_df.shape[0] + 3 + num_rows),
            'y2_axis': 1, # Use secondary axis for amount
            'data_labels': {'value': True, 'num_format': '$#,##0'},
        })
        chart_funnel_stage.set_title({'name': 'Deals and Revenue by Stage'})
        chart_funnel_stage.set_x_axis({'name': 'Deal Stage'})
        chart_funnel_stage.set_y_axis({'name': 'Total Deals'})
        chart_funnel_stage.set_y2_axis({'name': 'Total Revenue (USD)'})
        chart_funnel_stage.set_size({'width': 720, 'height': 432})
        fb_ws.insert_chart('E2', chart_funnel_stage)
    else:
        print("Skipping 'Deals and Revenue by Stage' chart due to empty data.")

    # --- 4. Closed Won Insights ---
    closed_won_quarterly_summary.to_excel(writer, sheet_name='Closed Won Insights', index=False)
    closed_won_by_user_quarter.to_excel(writer, sheet_name='Closed Won Insights', startrow=closed_won_quarterly_summary.shape[0] + 2, index=False)
    cwi_ws = writer.sheets['Closed Won Insights']

    # Chart: Closed Won Revenue Over Quarters (Line)
    if not closed_won_quarterly_summary.empty:
        chart_cwi_revenue = workbook.add_chart({'type': 'line'})
        num_rows = len(closed_won_quarterly_summary)
        chart_cwi_revenue.add_series({
            'name':       "='Closed Won Insights'!$C$1", # total_closed_amount_usd
            'categories': "='Closed Won Insights'!$D$2:$D$" + str(num_rows + 1), # created_quarter_str
            'values':     "='Closed Won Insights'!$C$2:$C$" + str(num_rows + 1),
            'marker': {'type': 'automatic'},
            'data_labels': {'value': True, 'num_format': '$#,##0'},
        })
        chart_cwi_revenue.set_title({'name': 'Closed Won Revenue Over Quarters (USD)'})
        chart_cwi_revenue.set_x_axis({'name': 'Quarter'})
        chart_cwi_revenue.set_y_axis({'name': 'Total Revenue (USD)'})
        chart_cwi_revenue.set_size({'width': 720, 'height': 432})
        cwi_ws.insert_chart('F2', chart_cwi_revenue)
    else:
        print("Skipping 'Closed Won Revenue Over Quarters' chart due to empty data.")

    # --- 5. User Performance ---
    user_performance.to_excel(writer, sheet_name='User Performance', index=False)
    up_ws = writer.sheets['User Performance']
    up_ws.set_column('A:A', 15) # user_id
    up_ws.set_column('B:E', 20) # Metrics

    # Chart: Top 10 Users by Total Revenue Won (Bar)
    if not user_performance.empty:
        top_10_users = user_performance.sort_values(by='total_revenue_won', ascending=False).head(10) # Ensure sorting for chart
        num_rows_top_10 = len(top_10_users)
        if num_rows_top_10 > 0:
            # Data for chart needs to be written to sheet first if not already there
            top_10_users.to_excel(writer, sheet_name='User Performance', startrow=user_performance.shape[0] + 2, index=False)
            chart_data_start_row = user_performance.shape[0] + 3
            chart_up_revenue = workbook.add_chart({'type': 'bar'})
            chart_up_revenue.add_series({
                'name':       "='User Performance'!$D$" + str(chart_data_start_row - 1), # total_revenue_won header
                'categories': "='User Performance'!$A$" + str(chart_data_start_row) + ":$A$" + str(chart_data_start_row + num_rows_top_10 - 1), # user_id
                'values':     "='User Performance'!$D$" + str(chart_data_start_row) + ":$D$" + str(chart_data_start_row + num_rows_top_10 - 1), # total_revenue_won
                'data_labels': {'value': True, 'num_format': '$#,##0'},
            })
            chart_up_revenue.set_title({'name': 'Top 10 Users by Total Revenue Won'})
            chart_up_revenue.set_x_axis({'name': 'Total Revenue Won (USD)'})
            chart_up_revenue.set_y_axis({'name': 'User ID'})
            chart_up_revenue.set_size({'width': 720, 'height': 432})
            up_ws.insert_chart('G2', chart_up_revenue)

            # Chart: Top 10 Users by Number of Closed Won Deals (Bar)
            top_10_deals_users = user_performance.sort_values(by='total_deals_won', ascending=False).head(10)
            num_rows_top_10_deals = len(top_10_deals_users)
            if num_rows_top_10_deals > 0:
                top_10_deals_users.to_excel(writer, sheet_name='User Performance', startrow=user_performance.shape[0] + num_rows_top_10 + 4, index=False)
                chart_data_start_row_deals = user_performance.shape[0] + num_rows_top_10 + 5
                chart_up_deals = workbook.add_chart({'type': 'bar'})
                chart_up_deals.add_series({
                    'name':       "='User Performance'!$E$" + str(chart_data_start_row_deals - 1), # total_deals_won header
                    'categories': "='User Performance'!$A$" + str(chart_data_start_row_deals) + ":$A$" + str(chart_data_start_row_deals + num_rows_top_10_deals - 1), # user_id
                    'values':     "='User Performance'!$E$" + str(chart_data_start_row_deals) + ":$E$" + str(chart_data_start_row_deals + num_rows_top_10_deals - 1), # total_deals_won
                    'data_labels': {'value': True},
                })
                chart_up_deals.set_title({'name': 'Top 10 Users by Number of Closed Won Deals'})
                chart_up_deals.set_x_axis({'name': 'Number of Closed Won Deals'})
                chart_up_deals.set_y_axis({'name': 'User ID'})
                chart_up_deals.set_size({'width': 720, 'height': 432})
                up_ws.insert_chart('G25', chart_up_deals)
            else:
                print("Skipping 'Top 10 Users by Number of Closed Won Deals' chart as data is empty.")
        else:
            print("Skipping 'User Performance' charts as top 10 data is empty.")
    else:
        print("Skipping 'User Performance' charts due to empty data.")

    # --- 6. UTM Attribution ---
    utm_attribution_source.to_excel(writer, sheet_name='UTM Attribution', index=False)
    utm_attribution_medium.to_excel(writer, sheet_name='UTM Attribution', startrow=utm_attribution_source.shape[0] + 2, index=False)
    ua_ws = writer.sheets['UTM Attribution']
    ua_ws.set_column('A:A', 25) # UTM Source/Medium
    ua_ws.set_column('B:D', 20) # Metrics

    # Chart: Total Revenue by UTM Source (Bar)
    if not utm_attribution_source.empty:
        chart_ua_source_revenue = workbook.add_chart({'type': 'bar'})
        num_rows = len(utm_attribution_source)
        chart_ua_source_revenue.add_series({
            'name':       "='UTM Attribution'!$C$1", # total_amount_usd header
            'categories': "='UTM Attribution'!$A$2:$A$" + str(num_rows + 1), # utm_source_cleaned
            'values':     "='UTM Attribution'!$C$2:$C$" + str(num_rows + 1), # total_amount_usd
            'data_labels': {'value': True, 'num_format': '$#,##0'},
        })
        chart_ua_source_revenue.set_title({'name': 'Total Revenue by UTM Source'})
        chart_ua_source_revenue.set_x_axis({'name': 'Total Revenue (USD)'})
        chart_ua_source_revenue.set_y_axis({'name': 'UTM Source'})
        if num_rows > 10: # If too many categories, show top N to avoid clutter
            chart_ua_source_revenue.set_y_axis({'num_font': {'sz': 9}, 'interval_unit': 1, 'max': 10}) # Limit categories if too many
        chart_ua_source_revenue.set_size({'width': 720, 'height': 432})
        ua_ws.insert_chart('E2', chart_ua_source_revenue)

        # Chart: Total Revenue by UTM Medium (Bar)
        if not utm_attribution_medium.empty:
            chart_ua_medium_revenue = workbook.add_chart({'type': 'bar'})
            num_rows_medium = len(utm_attribution_medium)
            chart_ua_medium_revenue.add_series({
                'name':       "='UTM Attribution'!$C$" + str(utm_attribution_source.shape[0] + 3), # total_amount_usd header for medium
                'categories': "='UTM Attribution'!$A$" + str(utm_attribution_source.shape[0] + 4) + ":$A$" + str(utm_attribution_source.shape[0] + 3 + num_rows_medium), # utm_medium
                'values':     "='UTM Attribution'!$C$" + str(utm_attribution_source.shape[0] + 4) + ":$C$" + str(utm_attribution_source.shape[0] + 3 + num_rows_medium), # total_amount_usd
                'data_labels': {'value': True, 'num_format': '$#,##0'},
            })
            chart_ua_medium_revenue.set_title({'name': 'Total Revenue by UTM Medium'})
            chart_ua_medium_revenue.set_x_axis({'name': 'Total Revenue (USD)'})
            chart_ua_medium_revenue.set_y_axis({'name': 'UTM Medium'})
            chart_ua_medium_revenue.set_size({'width': 720, 'height': 432})
            ua_ws.insert_chart('E25', chart_ua_medium_revenue)
        else:
            print("Skipping 'Total Revenue by UTM Medium' chart due to empty data.")
    else:
        print("Skipping 'UTM Attribution' charts due to empty data.")

print(f"\nAnalysis complete. Results exported to '{output_excel_file}'.")
print("Remember to install 'squarify' if you want the treemap: pip install squarify")