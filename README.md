<div align="center">

# 🎯 Target Business Case Study

### SQL-based E-commerce Insights & Operational Analysis on Target Brazil Orders (2016–2018) using BigQuery & SQLite

![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br>

*A comprehensive, end-to-end analytical case study dissecting Target's Brazilian e-commerce operations — uncovering customer behavior, order trends, delivery performance & payment patterns through structured SQL queries and Python visualizations.*

---

</div>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Dataset Description](#-dataset-description)
- [Project Architecture](#-project-architecture)
- [Key Analysis & SQL Queries](#-key-analysis--sql-queries)
- [Visualizations & Business Insights](#-visualizations--business-insights)
- [Business Recommendations](#-business-recommendations)
- [Getting Started](#-getting-started)
- [Author](#-author)

---

## 🔬 Project Overview

This project presents an **end-to-end SQL-based analytical case study** on **Target's Brazilian e-commerce operations** (based on the Olist database). The objective is to analyze customer purchase lifecycles, logistical constraints, and payment dynamics to identify strategic operational improvements.

Key dimensions analyzed:
- 🛒 **Customer Behavior** — purchasing habits, time-of-day purchase windows, and customer densities.
- 📈 **Order Trends** — Year-over-Year (YoY) order count growth and monthly seasonality patterns.
- 🚚 **Delivery Performance** — Actual delivery times, estimated delivery buffers, and regional variance across states.
- 💳 **Payment Patterns** — financing behaviors, payment type frequencies, and installment counts.

---

## 📊 Dataset Description

The analysis is driven by **four main relational tables**:

1. **`customers`**: Demographics and location details.
   - `customer_id`, `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`
2. **`orders`**: Transaction timestamps and status logs.
   - `order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`
3. **`order_items`**: Order line items, item pricing, and freights.
   - `order_id`, `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price`, `freight_value`
4. **`payments`**: Transaction values and installments structure.
   - `order_id`, `payment_sequential`, `payment_type`, `payment_installments`, `payment_value`

---

## 📁 Project Architecture

```
TARGET_BUSINESS_CASE_STUDY/
│
├── 📄 README.md                            # Project documentation (this file)
├── 📑 TARGET_SQL_BUSINESS_CASE_STUDY.pdf   # Case study guidelines
├── 📜 LICENSE                              # MIT License
│
├── 🗃️ data/
│   ├── customers.csv                       # Demographics dataset
│   ├── orders.csv                          # Orders timestamps dataset
│   ├── order_items.csv                     # Item level pricing and freight
│   ├── payments.csv                        # Installment and value dataset
│   └── target.db                           # SQLite database file containing all tables
│
├── 🖼️ images/                              # Generated visualization charts
│   ├── customer_distribution.png
│   ├── delivery_times_distribution.png
│   ├── monthly_seasonality.png
│   ├── orders_time_of_day.png
│   ├── payment_installments_dist.png
│   ├── payment_types_share.png
│   ├── revenue_pricing_by_state.png
│   └── yoy_orders.png
│
├── ⚙️ generate_data.py                    # Script to generate realistic mock datasets
├── 📜 Target_SQL_Analysis.py               # Core python analysis & query script
└── 📓 Target_SQL_Analysis.ipynb            # Interactive executed analysis notebook
```

---

## 🔑 Key Analysis & SQL Queries

### 1. In-Depth Trend & Seasonality Analysis
Understand month-over-month seasonality and order counts.
```sql
SELECT 
    CAST(strftime('%Y', order_purchase_timestamp) AS INTEGER) AS order_year, 
    CAST(strftime('%m', order_purchase_timestamp) AS INTEGER) AS order_month, 
    COUNT(order_id) AS total_orders 
FROM orders 
GROUP BY order_year, order_month 
ORDER BY order_year, order_month;
```

### 2. Time of Day Purchasing Behavior
Identifies when Brazilian customers place their orders (Dawn, Morning, Afternoon, or Night).
```sql
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
```

### 3. Economic Impact: Revenue Growth
Calculates the percentage increase in e-commerce spend between Jan-Aug of 2017 and 2018.
```sql
SELECT 
    ((SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2018' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)
     - SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END))
    / SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' AND CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) BETWEEN 1 AND 8 THEN p.payment_value ELSE 0 END)) * 100 AS percentage_increase 
FROM orders o 
JOIN payments p ON o.order_id = p.order_id;
```

---

## 🖼️ Visualizations & Business Insights

### 1. Seasonal Order Trends
- **Growth Pattern**: Orders grew by over **43%** from 2017 to 2018, showing a strong e-commerce adoption trend.
- **Monthly Seasonality**: Ordering patterns show a consistent climb towards the middle of the year, with a strong YoY increase in order values.

### 2. Hour of Day Distribution
- **Afternoon & Morning Peaks**: Almost **75%** of all orders are placed between 07:00 and 18:00 (Afternoon being the highest, followed by Morning). Only a tiny fraction of orders are placed at Dawn.

### 3. Payment Financing Share
- **Financing Reliance**: Credit cards dominate payments (**73.1%** of all transactions), followed by Boleto (**20.0%**).
- **Installments Structure**: A massive chunk of customers finance their purchases, with a significant number of transactions split across 2 to 12 months.

---

## 💡 Business Recommendations

Based on the transactional audit, we outline three core pillars of strategic recommendations:

| Pillar | Recommendation | Impact |
|:---|:---|:---|
| 🚚 **Logistics** | **Build Local Hubs in Remote States**: Remote Northern states like `AM` (Amazonas) and `PA` (Pará) suffer from slow delivery times (22+ days) and high freight costs (65+ INR average). Establishing fulfillment hubs in these sectors will slash transit times and drive margins. | Reduced shipping costs & faster turnarounds |
| ⏱️ **Operations** | **Refine ETA Predictions**: Estimated delivery dates are heavily pessimistic (on average, items arrive 6 days early). Narrowing this gap at checkout will significantly improve purchase conversion rates. | Increased conversion rate & customer trust |
| 💳 **Payments** | **Promote BNPL Options**: With over 70% of transactions relying on credit card payments and installments, introducing structured Buy Now, Pay Later (BNPL) options will increase the average ticket size. | Higher average order values (AOV) |

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/PritamPalit-official/TARGET_BUSINESS_CASE_STUDY.git
cd TARGET_BUSINESS_CASE_STUDY
```

**2. Setup environment and install dependencies**
```bash
pip install -r requirements.txt
```
*(If dependencies are not installed, install: `pandas`, `numpy`, `matplotlib`, `seaborn`)*

**3. Run the notebook**
Open `Target_SQL_Analysis.ipynb` using Jupyter Notebook or VS Code to explore the complete interactive execution of SQL queries and generated visualizations.

---

## 🛠️ Development & Testing

To maintain production-ready code quality, this repository includes dev dependencies, unit testing configurations, and automated CI pipelines:

### 📦 Setup Developer Dependencies
Install the required development and testing packages:
```bash
pip install -r requirements-dev.txt
```

### 🧪 Run Unit Tests Locally
Run the test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### ⚙️ Continuous Integration (CI)
A GitHub Actions workflow is configured in `.github/workflows/ci.yml`. On every `push` and `pull_request` to the repository, it automatically:
1. Provisions an Ubuntu runner with Python 3.10.
2. Installs dependencies from both `requirements.txt` and `requirements-dev.txt`.
3. Runs the test suite to verify code integrity and prevent regressions.

---

## 👤 Author

**Pritam Palit**
🎓 Electronics & Communication Engineering Graduate  
📊 Focus Areas: Data Analytics · Statistics · Business Intelligence

[![GitHub](https://img.shields.io/badge/GitHub-PritamPalit--official-181717?style=for-the-badge&logo=github)](https://github.com/PritamPalit-official)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pritam%20Palit-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/pritam-palit-77b2071b4/)
