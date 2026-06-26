-- ====================================================================
-- PROJECT: SUPERSTORE SALES ANALYTICS
-- DESCRIPTION: Production-grade SQL queries for business insight generation.
-- AUTHOR: Fredrick Juma Mathias
-- ====================================================================

-- 1. EXECUTIVE SUMMARY: Total Sales, Total Profit, and Overall Profit Margin
-- Purpose: Provides high-level financial health metrics for C-level executives.
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_percentage,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales;


-- 2. PRODUCT PERFORMANCE: Top 5 Most Profitable Product Categories
-- Purpose: Identifies which segments drive the highest financial returns.
SELECT 
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY category, sub_category
ORDER BY total_profit DESC
LIMIT 5;


-- 3. GEOGRAPHICAL ANALYSIS: Top 5 States by Sales Volume
-- Purpose: Highlights key geographical markets for targeted marketing campaigns.
SELECT 
    state,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY state
ORDER BY total_sales DESC
LIMIT 5;


-- 4. SHIPPING EFFICIENCY: Average Shipping Days by Ship Mode
-- Purpose: Analyzes operational efficiency and logistics performance.
-- Note: Uses Julian Day functions to calculate accurate date differences in SQLite.
SELECT 
    ship_mode,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS avg_shipping_days,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost
FROM sales
GROUP BY ship_mode
ORDER BY avg_shipping_days ASC;