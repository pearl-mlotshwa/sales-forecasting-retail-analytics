# Sales Forecasting & Revenue Performance Analytics

## Project Overview
End-to-end revenue analytics pipeline analysing **3+ years of sales data (5,000+ records)** to identify revenue trends, seasonality, and regional performance — with a **6-month forward revenue forecast**.

**Tools:** SQL (SQLite) | Python (Pandas, NumPy, Matplotlib) | Power BI

---

## Business Problem
The business needs visibility into which products, regions, and time periods drive the most revenue, and requires a forward-looking forecast to support budget planning and sales targets.

## Key Results
| Metric | Value |
|--------|-------|
| Records Analysed | 5,000+ sales transactions |
| Date Range | 3 full years (2022–2024) |
| Forecast Horizon | 6 months |
| Analysis Dimensions | Region, Product, Time, Salesperson |

## Project Structure
```
sales-forecasting/
│
├── data/
│   ├── generate_data.py        # Synthetic sales dataset generator
│   └── sales.csv               # Generated sales data (after running)
│
├── sql/
│   └── sales_analysis.sql      # SQL: monthly trends, YoY growth, Pareto, seasonality
│
├── notebooks/
│   └── sales_analysis.py       # Python: forecasting, visualisations, export
│
├── outputs/                    # Charts and exports (after running)
│
└── README.md
```

## How to Run

### 1. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

### 2. Generate the dataset
```bash
cd data
python generate_data.py
cd ..
```

### 3. Run the Python analysis
```bash
cd notebooks
python sales_analysis.py
```

### 4. Run SQL queries
```bash
sqlite3 data/sales.db < sql/sales_analysis.sql
```

## Analysis Highlights

### Revenue Trend & Forecasting
- Monthly revenue aggregated and trended over 36 months
- Linear trend model used to generate 6-month forward forecast with confidence band
- YoY growth calculated using `LAG()` window function in SQL

### Regional Performance Ranking
- All 6 regions ranked by annual revenue contribution
- Revenue share percentage calculated per year using window functions

### Pareto Product Analysis
- Top products identified by total revenue contribution
- Cumulative revenue percentage plotted to identify 80/20 split

### Seasonality
- Monthly averages calculated across all years to detect recurring seasonal patterns

## Power BI Dashboard
Import these files from `outputs/` into Power BI:
- `monthly_revenue.csv` — for trend and forecast visuals
- `revenue_forecast.csv` — overlay forecast line on actuals

---
*Project by Phumelele Pearl Mlotshwa | Junior Data Analyst*
*GitHub: [pearl-mlotshwa](https://github.com/pearl-mlotshwa)*
