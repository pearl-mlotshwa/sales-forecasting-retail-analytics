import pandas as pd
import numpy as np
import sqlite3
import os

np.random.seed(7)

# 3+ years of sales data = ~5000 records
n = 5000
regions = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Mpumalanga', 'Limpopo', 'Eastern Cape']
products = ['Enterprise Suite', 'Analytics Pro', 'Data Connector', 'Cloud Sync', 'Reporting Lite']
categories = {'Enterprise Suite': 'Software', 'Analytics Pro': 'Software',
              'Data Connector': 'Integration', 'Cloud Sync': 'Infrastructure', 'Reporting Lite': 'Reporting'}

start_date = pd.Timestamp('2022-01-01')
end_date = pd.Timestamp('2024-12-31')
dates = pd.date_range(start_date, end_date, freq='D')
sampled_dates = np.random.choice(dates, n, replace=True)

product_col = np.random.choice(products, n)
base_prices = {'Enterprise Suite': 4500, 'Analytics Pro': 2800, 'Data Connector': 1200,
               'Cloud Sync': 900, 'Reporting Lite': 350}

units = np.random.randint(1, 25, n)
revenue = np.array([units[i] * base_prices[product_col[i]] * np.random.uniform(0.85, 1.15)
                    for i in range(n)])

df = pd.DataFrame({
    'sale_id': [f'SL{str(i).zfill(5)}' for i in range(1, n+1)],
    'sale_date': sampled_dates,
    'region': np.random.choice(regions, n),
    'product': product_col,
    'category': [categories[p] for p in product_col],
    'units_sold': units,
    'revenue': np.round(revenue, 2),
    'salesperson': [f'REP{np.random.randint(1, 20):02d}' for _ in range(n)],
})
df['sale_date'] = pd.to_datetime(df['sale_date'])
df = df.sort_values('sale_date').reset_index(drop=True)

os.makedirs('data', exist_ok=True)
df.to_csv('data/sales.csv', index=False)

conn = sqlite3.connect('data/sales.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()

print(f"Generated {len(df):,} sales records")
print(f"Date range: {df['sale_date'].min().date()} to {df['sale_date'].max().date()}")
print(f"Total revenue: R{df['revenue'].sum():,.0f}")
