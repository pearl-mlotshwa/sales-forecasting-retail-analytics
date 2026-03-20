# Retail Sales Analysis

## Overview
Having historical sales data is not enough if you cannot see where 
things are heading. This project was built to give a business clear 
visibility into its revenue trends, understand which products and 
regions are actually driving performance, and forecast what the next 
six months will look like.

## The Approach
I worked with 5,000+ sales records spanning 3+ years. The first step 
was understanding the data, identifying revenue trends over time and 
spotting seasonal patterns that repeat annually. Seasonality matters 
because a forecast that ignores it will consistently be wrong at the 
same time every year.

I used advanced SQL techniques including CTEs and window functions to 
calculate year-on-year growth, running totals, and regional performance 
rankings. CTEs kept the queries clean and readable. Window functions 
let me compare month-on-month performance without losing the detail of 
individual records.

I then applied Pareto analysis to identify which 20% of products were 
driving 80% of revenue. That finding tells a business exactly where to 
focus its energy and which products may not be worth their operational 
cost.

For the forecast I decomposed the time series in Python into its trend, 
seasonal, and noise components, projected the trend forward six months, 
and layered the seasonal adjustment back on top. I validated the model 
through backtesting, hiding the last six months of known data and 
measuring how closely the forecast matched reality.

Everything landed in an interactive Power BI dashboard with the forecast 
overlaid on the historical trend line so stakeholders could see exactly 
where revenue was heading.

## Tools Used
Python, Pandas, NumPy, SQL, Power BI, DAX

## Key Insight
Seasonal patterns account for a significant portion of revenue variance. 
Forecasts that ignore seasonality consistently underestimate peak period 
performance, which leads to poor inventory, staffing, and investment 
decisions.

---
Built by Pearl Mlotshwa
github.com/pearl-mlotshwa
