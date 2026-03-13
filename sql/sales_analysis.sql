-- ============================================================
-- Sales Forecasting & Revenue Performance Analytics - SQL
-- Author: Phumelele Pearl Mlotshwa
-- Tools: SQLite | Python | Power BI
-- ============================================================

-- ── 1. MONTHLY REVENUE TREND ──────────────────────────────────
SELECT
    strftime('%Y', sale_date) AS year,
    strftime('%m', sale_date) AS month,
    strftime('%Y-%m', sale_date) AS year_month,
    COUNT(*) AS transactions,
    SUM(units_sold) AS total_units,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_transaction_value
FROM sales
GROUP BY year_month
ORDER BY year_month;

-- ── 2. YEAR-OVER-YEAR GROWTH (Window Function) ────────────────
WITH monthly AS (
    SELECT
        strftime('%Y', sale_date) AS yr,
        strftime('%m', sale_date) AS mo,
        strftime('%Y-%m', sale_date) AS year_month,
        ROUND(SUM(revenue), 2) AS monthly_revenue
    FROM sales
    GROUP BY year_month
),
yoy AS (
    SELECT *,
        LAG(monthly_revenue, 12) OVER (ORDER BY year_month) AS revenue_prev_year
    FROM monthly
)
SELECT
    year_month,
    monthly_revenue,
    revenue_prev_year,
    ROUND(100.0 * (monthly_revenue - revenue_prev_year) / NULLIF(revenue_prev_year, 0), 1) AS yoy_growth_pct
FROM yoy
WHERE revenue_prev_year IS NOT NULL
ORDER BY year_month;

-- ── 3. REGIONAL PERFORMANCE RANKING (Window Function) ─────────
WITH regional AS (
    SELECT
        region,
        strftime('%Y', sale_date) AS yr,
        ROUND(SUM(revenue), 2) AS annual_revenue,
        SUM(units_sold) AS total_units
    FROM sales
    GROUP BY region, yr
)
SELECT
    region,
    yr,
    annual_revenue,
    total_units,
    RANK() OVER (PARTITION BY yr ORDER BY annual_revenue DESC) AS revenue_rank,
    ROUND(100.0 * annual_revenue / SUM(annual_revenue) OVER (PARTITION BY yr), 1) AS revenue_share_pct
FROM regional
ORDER BY yr, revenue_rank;

-- ── 4. PARETO / TOP PRODUCT CONTRIBUTION ──────────────────────
WITH product_rev AS (
    SELECT
        product,
        category,
        ROUND(SUM(revenue), 2) AS total_revenue,
        SUM(units_sold) AS total_units
    FROM sales
    GROUP BY product
),
ranked AS (
    SELECT *,
        ROUND(100.0 * total_revenue / SUM(total_revenue) OVER (), 1) AS revenue_share_pct,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS running_total,
        SUM(total_revenue) OVER () AS grand_total
    FROM product_rev
)
SELECT
    product,
    category,
    total_revenue,
    revenue_share_pct,
    ROUND(100.0 * running_total / grand_total, 1) AS cumulative_pct
FROM ranked
ORDER BY total_revenue DESC;

-- ── 5. SEASONALITY ANALYSIS ───────────────────────────────────
SELECT
    CASE strftime('%m', sale_date)
        WHEN '01' THEN 'Jan' WHEN '02' THEN 'Feb' WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Apr' WHEN '05' THEN 'May' WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul' WHEN '08' THEN 'Aug' WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct' WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dec'
    END AS month_name,
    strftime('%m', sale_date) AS month_num,
    ROUND(AVG(daily_rev), 2) AS avg_monthly_revenue,
    COUNT(*) AS years_observed
FROM (
    SELECT strftime('%Y-%m', sale_date) AS ym,
           strftime('%m', sale_date) AS month,
           sale_date,
           SUM(revenue) OVER (PARTITION BY strftime('%Y-%m', sale_date)) AS daily_rev
    FROM sales
    GROUP BY ym
)
GROUP BY month_num
ORDER BY month_num;
