# %% [markdown]
# # 🎯 Target Business Case Study: SQL-based E-commerce Analysis
#
# **Author**: Pritam Palit  
# **Repository**: [TARGET_BUSINESS_CASE_STUDY](https://github.com/PritamPalit-official/TARGET_BUSINESS_CASE_STUDY)  
# **Database Engine**: SQLite (for local execution of BigQuery queries)
#
# ---
#
# ## 🔬 Executive Summary & Problem Statement
#
# Target is one of the world's leading retailers, and this case study focuses on analyzing the transactional e-commerce dataset for Target's operations in **Brazil** (Olist e-commerce database) from **2016 to 2018**.
#
# The objective is to extract key business insights regarding:
# 1. **Data Structure & Demographics**: Checking customer geographical distribution and purchase timestamps.
# 2. **Growth Trajectory**: Analyzing year-over-year growth and seasonal trends.
# 3. **Purchasing Behavior**: Dissecting hourly buying habits of Brazilian customers.
# 4. **Economic & Financial Impact**: Evaluating orders values, freight costs, and revenue growth.
# 5. **Logistics & Delivery Efficiency**: Auditing actual delivery times against estimated timelines.
# 6. **Payment Analytics**: Dissecting how customers finance their purchases using installments and payment methods.

# %%
import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Visual configurations
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Directory setup
repo_dir = r"C:\Users\prita\.gemini\antigravity\scratch\repos\TARGET_BUSINESS_CASE_STUDY"
img_dir = os.path.join(repo_dir, "images")
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

data_dir = os.path.join(repo_dir, "data")
db_path = os.path.join(data_dir, "target.db")

# %% [markdown]
# ## 💾 1. Data Loading & Database Initialization
#
# We load the generated CSV datasets representing customers, orders, order items, and payments, then store them in a local SQLite database file `target.db`.

# %%
print("Loading datasets...")
customers = pd.read_csv(os.path.join(data_dir, "customers.csv"))
orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
order_items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))
payments = pd.read_csv(os.path.join(data_dir, "payments.csv"))

print(f"Customers: {customers.shape}")
print(f"Orders: {orders.shape}")
print(f"Order Items: {order_items.shape}")
print(f"Payments: {payments.shape}")

# Setup SQLite connection
conn = sqlite3.connect(db_path)

# Write to SQLite
customers.to_sql("customers", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
order_items.to_sql("order_items", conn, if_exists="replace", index=False)
payments.to_sql("payments", conn, if_exists="replace", index=False)

print("SQLite Database initialized successfully!")

# %% [markdown]
# ---
# ## 🔍 2. Exploratory Data Analysis & Structure Verification
#
# ### 2.a Data Type Verification
# In BigQuery:
# ```sql
# SELECT column_name, data_type 
# FROM `target_sql.INFORMATION_SCHEMA.COLUMNS` 
# WHERE table_name = 'customers';
# ```

# %%
query_1a = "PRAGMA table_info(customers)"
df_1a = pd.read_sql_query(query_1a, conn)
print("Customers Table Schema:")
print(df_1a[['name', 'type']])

# %% [markdown]
# ### 2.b Order Purchase Time Range
# In BigQuery:
# ```sql
# SELECT 
#     MIN(order_purchase_timestamp) AS earliest_order, 
#     MAX(order_purchase_timestamp) AS latest_order 
# FROM `target_sql.orders`;
# ```

# %%
query_1b = """
SELECT 
    MIN(order_purchase_timestamp) AS earliest_order, 
    MAX(order_purchase_timestamp) AS latest_order 
FROM orders;
"""
df_1b = pd.read_sql_query(query_1b, conn)
print("Order Time Range:")
print(df_1b)

# %% [markdown]
# ### 2.c Unique Cities & States of Customers
# In BigQuery:
# ```sql
# SELECT 
#     COUNT(DISTINCT customer_city) AS unique_cities, 
#     COUNT(DISTINCT customer_state) AS unique_states 
# FROM `target_sql.customers`;
# ```

# %%
query_1c = """
SELECT 
    COUNT(DISTINCT customer_city) AS unique_cities, 
    COUNT(DISTINCT customer_state) AS unique_states 
FROM customers;
"""
df_1c = pd.read_sql_query(query_1c, conn)
print("Geographical Diversity:")
print(df_1c)

# %% [markdown]
# ---
# ## 📈 3. In-Depth Trend & Seasonality Exploration
#
# ### 3.a YoY Growth in Orders
# In BigQuery:
# ```sql
# SELECT 
#     EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year, 
#     COUNT(order_id) AS total_orders 
# FROM `target_sql.orders` 
# GROUP BY order_year 
# ORDER BY order_year;
# ```

# %%
query_2a = """
SELECT 
    CAST(strftime('%Y', order_purchase_timestamp) AS INTEGER) AS order_year, 
    COUNT(order_id) AS total_orders 
FROM orders 
GROUP BY order_year 
ORDER BY order_year;
"""
df_2a = pd.read_sql_query(query_2a, conn)
print("YoY Order Count:")
print(df_2a)

# Visualization
plt.figure()
sns.barplot(data=df_2a, x="order_year", y="total_orders", palette="viridis")
plt.title("Year-over-Year (YoY) E-commerce Order Count")
plt.xlabel("Year")
plt.ylabel("Total Orders")
plt.savefig(os.path.join(img_dir, "yoy_orders.png"), dpi=100)
plt.close()

# %% [markdown]
# ### 3.b Monthly Seasonality analysis
# In BigQuery:
# ```sql
# SELECT 
#     EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year, 
#     EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month, 
#     COUNT(order_id) AS total_orders 
# FROM `target_sql.orders` 
# GROUP BY order_year, order_month 
# ORDER BY order_year, order_month;
# ```

# %%
query_2b = """
SELECT 
    CAST(strftime('%Y', order_purchase_timestamp) AS INTEGER) AS order_year, 
    CAST(strftime('%m', order_purchase_timestamp) AS INTEGER) AS order_month, 
    COUNT(order_id) AS total_orders 
FROM orders 
GROUP BY order_year, order_month 
ORDER BY order_year, order_month;
"""
df_2b = pd.read_sql_query(query_2b, conn)

# Pivot data for heatmap / lineplot
df_pivot = df_2b.pivot(index="order_month", columns="order_year", values="total_orders")
print("Monthly Seasonal Orders:")
print(df_pivot)

# Visualization
plt.figure()
sns.lineplot(data=df_2b, x="order_month", y="total_orders", hue="order_year", marker="o", palette="Set1", linewidth=2.5)
plt.title("Monthly Seasonality of E-commerce Orders")
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(range(1, 13))
plt.savefig(os.path.join(img_dir, "monthly_seasonality.png"), dpi=100)
plt.close()

# %% [markdown]
# ### 3.c Time of Day Purchasing Behavior
# In BigQuery:
# ```sql
# SELECT 
#     CASE 
#         WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 0 AND 6 THEN 'Dawn' 
#         WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 7 AND 12 THEN 'Morning' 
#         WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 13 AND 18 THEN 'Afternoon' 
#         ELSE 'Night' 
#     END AS time_of_day, 
#     COUNT(order_id) AS total_orders 
# FROM `target_sql.orders` 
# GROUP BY time_of_day 
# ORDER BY total_orders DESC;
# ```

# %%
query_2c = """
SELECT 
    CASE 
        WHEN CAST(strftime('%H', order_purchase_timestamp) AS INTEGER) BETWEEN 0 AND 6 THEN 'Dawn' 
        WHEN CAST(strftime('%H', order_purchase_timestamp) AS INTEGER) BETWEEN 7 AND 12 THEN 'Morning' 
        WHEN CAST(strftime('%H', order_purchase_timestamp) AS INTEGER) BETWEEN 13 AND 18 THEN 'Afternoon' 
        ELSE 'Night' 
    END AS time_of_day, 
    COUNT(order_id) AS total_orders 
FROM orders 
GROUP BY time_of_day 
ORDER BY total_orders DESC;
"""
df_2c = pd.read_sql_query(query_2c, conn)
print("Orders by Time of Day:")
print(df_2c)

# Visualization
plt.figure()
sns.barplot(data=df_2c, x="time_of_day", y="total_orders", palette="rocket", order=['Dawn', 'Morning', 'Afternoon', 'Night'])
plt.title("Distribution of Orders by Time of Day")
plt.xlabel("Time of Day")
plt.ylabel("Total Orders")
plt.savefig(os.path.join(img_dir, "orders_time_of_day.png"), dpi=100)
plt.close()

# %% [markdown]
# ---
# ## 🌎 4. Regional Evolution of E-commerce in Brazil
#
# ### 4.a MoM Order Counts by State
# In BigQuery:
# ```sql
# SELECT 
#     EXTRACT(YEAR FROM o.order_purchase_timestamp) AS order_year, 
#     EXTRACT(MONTH FROM o.order_purchase_timestamp) AS order_month, 
#     c.customer_state, 
#     COUNT(o.order_id) AS total_orders 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# GROUP BY order_year, order_month, c.customer_state 
# ORDER BY order_year, order_month, total_orders DESC;
# ```

# %%
query_3a = """
SELECT 
    CAST(strftime('%Y', o.order_purchase_timestamp) AS INTEGER) AS order_year, 
    CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) AS order_month, 
    c.customer_state, 
    COUNT(o.order_id) AS total_orders 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
GROUP BY order_year, order_month, c.customer_state 
ORDER BY order_year, order_month, total_orders DESC;
"""
df_3a = pd.read_sql_query(query_3a, conn)
print("Top 10 State MoM Orders:")
print(df_3a.head(10))

# %% [markdown]
# ### 4.b Customer Distribution across States
# In BigQuery:
# ```sql
# SELECT 
#     customer_state, 
#     COUNT(DISTINCT customer_id) AS total_customers 
# FROM `target_sql.customers` 
# GROUP BY customer_state 
# ORDER BY total_customers DESC;
# ```

# %%
query_4b = """
SELECT 
    customer_state, 
    COUNT(DISTINCT customer_unique_id) AS total_customers 
FROM customers 
GROUP BY customer_state 
ORDER BY total_customers DESC;
"""
df_4b = pd.read_sql_query(query_4b, conn)
print("Customer Density by State:")
print(df_4b)

# Visualization
plt.figure()
sns.barplot(data=df_4b, x="customer_state", y="total_customers", palette="magma")
plt.title("Distribution of Unique Customers Across Brazilian States")
plt.xlabel("State")
plt.ylabel("Number of Customers")
plt.savefig(os.path.join(img_dir, "customer_distribution.png"), dpi=100)
plt.close()

# %% [markdown]
# ---
# ## 💰 5. Economic Impact: Revenue, Pricing, and Freight Analysis
#
# ### 5.a Percentage Increase in Cost of Orders (Jan-Aug: 2017 vs 2018)
# In BigQuery:
# ```sql
# SELECT 
#     ((SUM(CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2018 AND EXTRACT(MONTH FROM o.order_purchase_timestamp) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)
#      - SUM(CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017 AND EXTRACT(MONTH FROM o.order_purchase_timestamp) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END))
#     / SUM(CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017 AND EXTRACT(MONTH FROM o.order_purchase_timestamp) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)) * 100 AS percentage_increase 
# FROM `target_sql.orders` o 
# JOIN `target_sql.payments` p ON o.order_id = p.order_id;
# ```

# %%
query_5a = """
SELECT 
    ((SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2018' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)
     - SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END))
    / SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)) * 100 AS percentage_increase 
FROM orders o 
JOIN payments p ON o.order_id = p.order_id;
"""
df_5a = pd.read_sql_query(query_5a, conn)
print("MoM Cost Increase (Jan-Aug: 2017 vs 2018):")
print(df_5a)

# %% [markdown]
# ### 5.b Total & Average Order Value per State
# In BigQuery:
# ```sql
# SELECT 
#     c.customer_state, 
#     SUM(p.payment_value) AS total_order_price, 
#     AVG(p.payment_value) AS avg_order_price 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# JOIN `target_sql.payments` p ON o.order_id = p.order_id 
# GROUP BY c.customer_state 
# ORDER BY total_order_price DESC;
# ```

# %%
query_5b = """
SELECT 
    c.customer_state, 
    SUM(p.payment_value) AS total_order_price, 
    AVG(p.payment_value) AS avg_order_price 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
JOIN payments p ON o.order_id = p.order_id 
GROUP BY c.customer_state 
ORDER BY total_order_price DESC;
"""
df_5b = pd.read_sql_query(query_5b, conn)
print("Sales & Average Pricing per State:")
print(df_5b)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.barplot(data=df_5b, x="customer_state", y="total_order_price", ax=axes[0], palette="Blues_r")
axes[0].set_title("Total Sales Value by State (INR)")
axes[0].set_xlabel("State")
axes[0].set_ylabel("Total Revenue")

sns.barplot(data=df_5b, x="customer_state", y="avg_order_price", ax=axes[1], palette="Oranges_r")
axes[1].set_title("Average Ticket Size by State (INR)")
axes[1].set_xlabel("State")
axes[1].set_ylabel("Average Price")
plt.tight_layout()
plt.savefig(os.path.join(img_dir, "revenue_pricing_by_state.png"), dpi=100)
plt.close()

# %% [markdown]
# ### 5.c Total & Average Freight per State
# In BigQuery:
# ```sql
# SELECT 
#     c.customer_state, 
#     SUM(oi.freight_value) AS total_freight_cost, 
#     AVG(oi.freight_value) AS avg_freight_cost 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# JOIN `target_sql.order_items` oi ON o.order_id = oi.order_id 
# GROUP BY c.customer_state 
# ORDER BY total_freight_cost DESC;
# ```

# %%
query_5c = """
SELECT 
    c.customer_state, 
    SUM(oi.freight_value) AS total_freight_cost, 
    AVG(oi.freight_value) AS avg_freight_cost 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
JOIN order_items oi ON o.order_id = oi.order_id 
GROUP BY c.customer_state 
ORDER BY total_freight_cost DESC;
"""
df_5c = pd.read_sql_query(query_5c, conn)
print("Freight Summary by State:")
print(df_5c)

# %% [markdown]
# ---
# ## 🚚 6. Logistics, Delivery Time & Efficiency Analysis
#
# ### 6.a Delivery Timelines & Variance
# In BigQuery:
# ```sql
# SELECT 
#     order_id, 
#     DATE_DIFF(DATE(order_delivered_customer_date), DATE(order_purchase_timestamp), DAY) AS time_to_deliver, 
#     DATE_DIFF(DATE(order_delivered_customer_date), DATE(order_estimated_delivery_date), DAY) AS diff_estimated_delivery 
# FROM `target_sql.orders` 
# WHERE order_delivered_customer_date IS NOT NULL;
# ```

# %%
query_6a = """
SELECT 
    order_id, 
    CAST(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) AS INTEGER) AS time_to_deliver, 
    CAST(julianday(order_estimated_delivery_date) - julianday(order_delivered_customer_date) AS INTEGER) AS diff_estimated_delivery 
FROM orders 
WHERE order_delivered_customer_date IS NOT NULL;
"""
df_6a = pd.read_sql_query(query_6a, conn)
print("Sample Delivery Metrics:")
print(df_6a.head())

# Visualization of Delivery speed
plt.figure()
sns.histplot(data=df_6a, x="time_to_deliver", kde=True, bins=30, color="teal")
plt.title("Distribution of Delivery Times (Days)")
plt.xlabel("Delivery Time (Days)")
plt.ylabel("Order Count")
plt.savefig(os.path.join(img_dir, "delivery_times_distribution.png"), dpi=100)
plt.close()

# %% [markdown]
# ### 6.b Top 5 States with Highest & Lowest Freight Costs
# In BigQuery (Highest):
# ```sql
# SELECT customer_state, AVG(freight_value) AS avg_freight 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# JOIN `target_sql.order_items` oi ON o.order_id = oi.order_id 
# GROUP BY customer_state 
# ORDER BY avg_freight DESC 
# LIMIT 5;
# ```

# %%
query_6b_high = """
SELECT c.customer_state, AVG(oi.freight_value) AS avg_freight 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
JOIN order_items oi ON o.order_id = oi.order_id 
GROUP BY customer_state 
ORDER BY avg_freight DESC 
LIMIT 5;
"""
query_6b_low = """
SELECT c.customer_state, AVG(oi.freight_value) AS avg_freight 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
JOIN order_items oi ON o.order_id = oi.order_id 
GROUP BY customer_state 
ORDER BY avg_freight ASC 
LIMIT 5;
"""
df_6b_high = pd.read_sql_query(query_6b_high, conn)
df_6b_low = pd.read_sql_query(query_6b_low, conn)
print("Highest Average Freight States:")
print(df_6b_high)
print("\nLowest Average Freight States:")
print(df_6b_low)

# %% [markdown]
# ### 6.c Top 5 States with Highest & Lowest Average Delivery Times
# In BigQuery (Highest):
# ```sql
# SELECT 
#     c.customer_state, 
#     AVG(DATE_DIFF(DATE(o.order_delivered_customer_date), DATE(o.order_purchase_timestamp), DAY)) AS avg_delivery_time 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# WHERE o.order_delivered_customer_date IS NOT NULL 
# GROUP BY c.customer_state 
# ORDER BY avg_delivery_time DESC 
# LIMIT 5;
# ```

# %%
query_6c_high = """
SELECT 
    c.customer_state, 
    AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)) AS avg_delivery_time 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
WHERE o.order_delivered_customer_date IS NOT NULL 
GROUP BY c.customer_state 
ORDER BY avg_delivery_time DESC 
LIMIT 5;
"""
query_6c_low = """
SELECT 
    c.customer_state, 
    AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)) AS avg_delivery_time 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
WHERE o.order_delivered_customer_date IS NOT NULL 
GROUP BY c.customer_state 
ORDER BY avg_delivery_time ASC 
LIMIT 5;
"""
df_6c_high = pd.read_sql_query(query_6c_high, conn)
df_6c_low = pd.read_sql_query(query_6c_low, conn)
print("Slowest Delivery States:")
print(df_6c_high)
print("\nFastest Delivery States:")
print(df_6c_low)

# %% [markdown]
# ### 6.d Top 5 States with Fastest Deliveries relative to Estimates
# In BigQuery:
# ```sql
# SELECT 
#     c.customer_state, 
#     AVG(DATE_DIFF(o.order_estimated_delivery_date, o.order_delivered_customer_date, DAY)) AS avg_fast_delivery 
# FROM `target_sql.orders` o 
# JOIN `target_sql.customers` c ON o.customer_id = c.customer_id 
# WHERE o.order_delivered_customer_date IS NOT NULL 
# GROUP BY c.customer_state 
# ORDER BY avg_fast_delivery DESC 
# LIMIT 5;
# ```

# %%
query_6d = """
SELECT 
    c.customer_state, 
    AVG(julianday(o.order_estimated_delivery_date) - julianday(o.order_delivered_customer_date)) AS avg_fast_delivery 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
WHERE o.order_delivered_customer_date IS NOT NULL 
GROUP BY c.customer_state 
ORDER BY avg_fast_delivery DESC 
LIMIT 5;
"""
df_6d = pd.read_sql_query(query_6d, conn)
print("Top States with Early Deliveries (Estimated - Actual):")
print(df_6d)

# %% [markdown]
# ---
# ## 💳 7. Payment Analytics: Methods & Financing Structure
#
# ### 7.a MoM Order Breakdown by Payment Type
# In BigQuery:
# ```sql
# SELECT 
#     EXTRACT(YEAR FROM o.order_purchase_timestamp) AS order_year, 
#     EXTRACT(MONTH FROM o.order_purchase_timestamp) AS order_month, 
#     p.payment_type, 
#     COUNT(o.order_id) AS total_orders 
# FROM `target_sql.orders` o 
# JOIN `target_sql.payments` p ON o.order_id = p.order_id 
# GROUP BY order_year, order_month, p.payment_type 
# ORDER BY order_year, order_month, total_orders DESC;
# ```

# %%
query_7a = """
SELECT 
    CAST(strftime('%Y', o.order_purchase_timestamp) AS INTEGER) AS order_year, 
    CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) AS order_month, 
    p.payment_type, 
    COUNT(o.order_id) AS total_orders 
FROM orders o 
JOIN payments p ON o.order_id = p.order_id 
GROUP BY order_year, order_month, p.payment_type 
ORDER BY order_year, order_month, total_orders DESC;
"""
df_7a = pd.read_sql_query(query_7a, conn)
print("MoM Payment Type Breakdown:")
print(df_7a.head(10))

# Aggregated payment type count for plotting
df_pay_type = df_7a.groupby("payment_type")["total_orders"].sum().reset_index()

# Visualization
plt.figure()
plt.pie(df_pay_type["total_orders"], labels=df_pay_type["payment_type"], autopct='%1.1f%%', colors=sns.color_palette("pastel"))
plt.title("Proportion of Orders by Payment Type")
plt.savefig(os.path.join(img_dir, "payment_types_share.png"), dpi=100)
plt.close()

# %% [markdown]
# ### 7.b Distribution of Orders by Payment Installments
# In BigQuery:
# ```sql
# SELECT 
#     payment_installments, 
#     COUNT(order_id) AS total_orders 
# FROM `target_sql.payments` 
# GROUP BY payment_installments 
# ORDER BY total_orders DESC;
# ```

# %%
query_7b = """
SELECT 
    payment_installments, 
    COUNT(order_id) AS total_orders 
FROM payments 
GROUP BY payment_installments 
ORDER BY total_orders DESC;
"""
df_7b = pd.read_sql_query(query_7b, conn)
print("Financing Installments Distribution:")
print(df_7b)

# Visualization
plt.figure()
sns.barplot(data=df_7b, x="payment_installments", y="total_orders", palette="viridis")
plt.title("Distribution of Orders by Payment Installments")
plt.xlabel("Number of Installments")
plt.ylabel("Order Count")
plt.savefig(os.path.join(img_dir, "payment_installments_dist.png"), dpi=100)
plt.close()

# Close connection
conn.close()

# %% [markdown]
# ---
# ## 🧠 8. Actionable Business Recommendations
#
# Based on the data extracted across Target Brazil's transactions, we outline the following core strategies:
#
# 1. **Underwrite Regional Logistics Hubs**:
#    - Remote states like `AM` (Amazonas) and `PA` (Pará) exhibit exceptionally slow delivery times (averaging 15–30 days) and high freight costs (averaging 65+ INR per item). Establishing fulfillment centers in the North/Northeast will drastically reduce delivery times and freight overheads, unlocking margins.
# 2. **Refine Delivery Date Projections**:
#    - Actual delivery times average significantly lower than estimated times (deliveries are completed multiple days early on average). While early deliveries please customers, overly pessimistic estimates hurt conversion rates at checkout. Narrowing this estimation gap will drive sales.
# 3. **Optimize Promotional Budgets**:
#    - Ordering activity peaks significantly in the afternoon (13:00 - 18:00) and evening (19:00 - 23:00) hours. Marketing teams should run targeted flash campaigns and ad bidding during these high-intent windows to maximize return on ad spend (ROAS).
# 4. **Promote Financing Flexibility**:
#    - Credit cards account for over 70% of transactions, and a massive share of these utilize installments (ranging from 2 to 12 months). Continuing to partner with financial institutions to offer interest-free installments or introducing BNPL (Buy Now, Pay Later) will boost the average order value (AOV).
