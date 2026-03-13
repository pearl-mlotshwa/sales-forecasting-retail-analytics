#!/usr/bin/env python3
"""
Sales Forecasting & Revenue Performance Analytics
Author: Phumelele Pearl Mlotshwa
Tools: Python (Pandas, NumPy, Matplotlib), SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

os.makedirs('outputs', exist_ok=True)

# ── 1. Load Data ───────────────────────────────────────────────
conn = sqlite3.connect('data/sales.db')
df = pd.read_sql('SELECT * FROM sales', conn)
conn.close()

df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year'] = df['sale_date'].dt.year
df['month'] = df['sale_date'].dt.month
df['year_month'] = df['sale_date'].dt.to_period('M')

print("=" * 55)
print("  Sales Forecasting & Revenue Performance Report")
print("=" * 55)
print(f"\nTotal records   : {len(df):,}")
print(f"Date range      : {df['sale_date'].min().date()} → {df['sale_date'].max().date()}")
print(f"Total revenue   : R{df['revenue'].sum():,.0f}")

# ── 2. Monthly Revenue ─────────────────────────────────────────
monthly = df.groupby('year_month')['revenue'].sum().reset_index()
monthly['year_month_dt'] = monthly['year_month'].dt.to_timestamp()

# ── 3. YoY Growth ─────────────────────────────────────────────
monthly['prev_year'] = monthly['revenue'].shift(12)
monthly['yoy_growth'] = (monthly['revenue'] - monthly['prev_year']) / monthly['prev_year']

# ── 4. 6-Month Forecast (Linear Trend) ────────────────────────
x = np.arange(len(monthly))
y = monthly['revenue'].values
coeffs = np.polyfit(x, y, 1)
trend = np.poly1d(coeffs)

future_x = np.arange(len(monthly), len(monthly) + 6)
forecast = trend(future_x)

last_date = monthly['year_month_dt'].iloc[-1]
forecast_dates = pd.date_range(last_date + pd.offsets.MonthBegin(1), periods=6, freq='MS')

# ── 5. Pareto Analysis ────────────────────────────────────────
product_rev = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
cumulative = (product_rev.cumsum() / product_rev.sum() * 100)

# ── 6. Visualisations ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Sales Forecasting & Revenue Performance Dashboard', fontsize=15, fontweight='bold')

# 6a. Monthly revenue + forecast
axes[0, 0].plot(monthly['year_month_dt'], monthly['revenue'], color='#2980b9', linewidth=2, label='Actual')
axes[0, 0].plot(forecast_dates, forecast, color='#e74c3c', linewidth=2, linestyle='--', label='6-Month Forecast')
axes[0, 0].fill_between(forecast_dates, forecast * 0.92, forecast * 1.08, alpha=0.2, color='#e74c3c', label='Confidence Band')
axes[0, 0].set_title('Monthly Revenue & 6-Month Forecast')
axes[0, 0].set_ylabel('Revenue (R)')
axes[0, 0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R{x/1e6:.1f}M'))
axes[0, 0].legend()

# 6b. YoY Growth
yoy_data = monthly.dropna(subset=['yoy_growth'])
colors = ['#27ae60' if v >= 0 else '#e74c3c' for v in yoy_data['yoy_growth']]
axes[0, 1].bar(yoy_data['year_month_dt'], yoy_data['yoy_growth'] * 100, color=colors, width=20)
axes[0, 1].axhline(0, color='black', linewidth=0.8)
axes[0, 1].set_title('Year-over-Year Revenue Growth (%)')
axes[0, 1].set_ylabel('YoY Growth (%)')

# 6c. Regional revenue
region_rev = df.groupby('region')['revenue'].sum().sort_values(ascending=True)
region_rev.plot(kind='barh', ax=axes[1, 0], color='#8e44ad', edgecolor='white')
axes[1, 0].set_title('Total Revenue by Region')
axes[1, 0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R{x/1e6:.1f}M'))

# 6d. Pareto – product contribution
ax2 = axes[1, 1].twinx()
product_rev.plot(kind='bar', ax=axes[1, 1], color='#e67e22', edgecolor='white', label='Revenue')
ax2.plot(range(len(cumulative)), cumulative.values, 'r-o', linewidth=2, markersize=5, label='Cumulative %')
ax2.yaxis.set_major_formatter(mticker.PercentFormatter())
ax2.set_ylim(0, 115)
axes[1, 1].set_title('Pareto: Product Revenue Contribution')
axes[1, 1].set_ylabel('Revenue (R)')
axes[1, 1].tick_params(axis='x', rotation=20)

plt.tight_layout()
plt.savefig('outputs/sales_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nDashboard saved to outputs/sales_dashboard.png")

# ── 7. Export for Power BI ────────────────────────────────────
monthly_export = monthly.copy()
monthly_export['year_month'] = monthly_export['year_month'].astype(str)
monthly_export.to_csv('outputs/monthly_revenue.csv', index=False)

forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast_revenue': forecast.round(2)})
forecast_df.to_csv('outputs/revenue_forecast.csv', index=False)
print("Exported: monthly_revenue.csv, revenue_forecast.csv")

print("\nTop Products by Revenue:")
print(product_rev.apply(lambda x: f'R{x:,.0f}').to_string())
print("\nAnalysis complete.")
