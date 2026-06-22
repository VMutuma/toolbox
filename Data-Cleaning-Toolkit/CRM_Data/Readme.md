# CRM Elite Analytics Dashboard

## Overview

This Python script provides a comprehensive analytical dashboard for CRM (Customer Relationship Management) data. It automates the process of extracting, cleaning, and analyzing CRM deal data to offer insights into sales performance, funnel conversion, user productivity, and marketing attribution. A key feature is the calculation of Return on Investment (ROI) for marketing spend, with a particular focus on Year-To-Date (YTD) 2025 and quarterly breakdowns.

The output is a detailed Excel report (`crm_elite_analysis.xlsx`) containing various data summaries and embedded visualizations, along with standalone PNG charts for easy sharing and presentation.

## Features

* **Overall CRM Summary:** Provides high-level metrics on total deals, total revenue, and average deal sizes across the entire CRM dataset.
* **2025 High-Level Overview:**
    * Calculates Year-To-Date (YTD) performance for 2025, including total ad spend, total closed-won revenue, and the combined ROI.
    * **Crucially, it provides a detailed breakdown of closed-won revenue specifically attributed to key marketing channels such as Google (SEM), Google (Other/Organic), Facebook, YouTube, and Website-driven traffic, ensuring all specified fields are accounted for.**
* **Quarterly Trends Analysis:** Tracks deal volume, revenue, and stage progression across different quarters.
* **Sales Funnel Breakdown:** Analyzes deal conversion rates through various stages of the sales pipeline, with a focus on 'Negotiation' to 'Closed Won' conversion.
* **Closed Won Insights:** Delves deeper into successful deals, offering quarterly summaries of closed-won revenue and insights into the distribution of closed-won deal sizes.
* **User Performance Analysis:** Evaluates individual user contributions based on deals originated, total revenue influenced, and closed-won deals/revenue.
* **UTM Attribution:** Analyzes the effectiveness of different marketing UTM sources and mediums by correlating them with deal revenue and volume.
* **Deal Velocity & Timing:** Examines the average duration deals take to close, particularly for 'Closed Won' opportunities.
* **Automated Reporting:** All analyses are consolidated into a single, well-structured Excel workbook with dedicated sheets for each section.
* **Visualizations:** Generates various charts (bar plots, line graphs, histograms, treemaps) for better data comprehension, which are both embedded directly into the Excel report and saved as separate PNG image files.

## How to Use

### Prerequisites

* **Python 3.x**
* `pip` (Python package installer)

### Installation of Dependencies

Before running the script, install the necessary Python libraries:

```bash
pip install pandas numpy matplotlib seaborn openpyxl squarify xlsxwriter