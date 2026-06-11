<div align="center">

# 🎯 Target Business Case Study

### SQL-based E-commerce Insights & Operational Analysis on Target Brazil Orders (2016–2018) using BigQuery

![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br>

*A comprehensive, end-to-end analytical case study dissecting Target's Brazilian e-commerce operations — uncovering customer behavior, order trends, delivery performance & payment patterns through structured SQL queries.*

---

</div>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Dataset Description](#-dataset-description)
- [Key Analysis Performed](#-key-analysis-performed)
- [Tools & Technologies](#️-tools--technologies)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Business Insights](#-business-insights)
- [Business Recommendations](#-business-recommendations)
- [Author](#-author)
- [License](#-license)

---

## 🔬 Project Overview

This project presents an **end-to-end SQL-based analytical case study** on **Target's Brazilian e-commerce operations**. The objective is to analyze:

- 🛒 **Customer Behavior** — purchasing habits, preferences & demographics  
- 📈 **Order Trends** — growth trajectories, seasonal patterns & volume shifts  
- 🚚 **Delivery Performance** — actual vs. estimated delivery timelines  
- 💳 **Payment Patterns** — method usage, installment behavior & affordability signals  

> The analysis spans **2016–2018**, covering thousands of orders across multiple Brazilian states, providing actionable insights for strategic decision-making.

---

## 📊 Dataset Description

The dataset consists of **multiple interrelated tables** that collectively capture the full e-commerce transaction lifecycle:

| Table | Description |
|:------|:------------|
| `customers` | Customer demographics, unique IDs & geographic location (city, state) |
| `orders` | Order-level data including timestamps, status & delivery dates |
| `order_items` | Line-item details — product IDs, seller info, freight costs & prices |
| `payments` | Payment method, installment count & transaction values |

> **Key Data Points:** Customer demographics · Purchase timestamps · Freight costs · Delivery timelines · Payment methods & installments

---

## 🔑 Key Analysis Performed

| # | Analysis Area | Focus |
|:-:|:---|:---|
| 1 | **Exploratory Data Analysis** | Customer distribution, order time range & geographic coverage |
| 2 | **Order Trends** | Year-wise and month-wise order growth & seasonality patterns |
| 3 | **Customer Behavior** | Time-of-day analysis for order placement |
| 4 | **Regional Insights** | State-wise order volume & customer distribution |
| 5 | **Economic Impact** | Order value growth, freight costs & revenue contribution by state |
| 6 | **Delivery Performance** | Actual vs. estimated delivery time analysis |
| 7 | **Payment Analysis** | Payment methods usage & installment behavior |

---

## 🛠️ Tools & Technologies

| Tool / Technology | Purpose |
|:---|:---|
| **SQL** | Core querying language for data extraction & analysis |
| **Google BigQuery** | Cloud-based data warehouse for running analytical queries |
| **Relational Database Concepts** | Schema design, table joins & data modeling |
| **Analytical Query Design** | Window functions, aggregations & subqueries for insight generation |

---

## 📁 Project Structure

```
TARGET_BUSINESS_CASE_STUDY/
│
├── 📄 README.md                            # Project documentation (this file)
├── 📑 TARGET_SQL_BUSINESS_CASE_STUDY.pdf   # Complete analysis report with SQL queries & results
└── 📜 LICENSE                              # MIT License
```

---

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/PritamPalit-official/TARGET_BUSINESS_CASE_STUDY.git
cd TARGET_BUSINESS_CASE_STUDY
```

**2. Open the analysis report**

```
Open TARGET_SQL_BUSINESS_CASE_STUDY.pdf to view the complete SQL queries, results & visualizations.
```

**3. Run queries on BigQuery**

```sql
-- Example: Monthly order trend analysis
SELECT
    EXTRACT(YEAR FROM order_purchase_timestamp)  AS order_year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month,
    COUNT(order_id)                              AS total_orders
FROM `target.orders`
GROUP BY order_year, order_month
ORDER BY order_year, order_month;
```

> 💡 **Tip:** Each query in the report is modular and can be adapted to similar e-commerce datasets. Use this repository as a reference for **SQL analytics interviews**, **academic submissions** & **real-world BI case studies**.

---

## 📈 Business Insights

The analysis uncovered several critical findings across Target Brazil's e-commerce operations:

| Insight Area | Key Finding |
|:---|:---|
| 📈 **Growth** | Strong year-on-year growth in e-commerce adoption across the analysis period |
| 🗓️ **Seasonality** | Clear seasonal purchasing patterns with identifiable peak and off-peak periods |
| 🚚 **Freight & Delivery** | Significant variation in freight costs and delivery efficiency across Brazilian states |
| 💳 **Payments** | Heavy reliance on credit cards and installment-based transactions |
| 🧠 **Affordability** | Installment usage signals customer affordability behavior and purchasing preferences |

---

## 💡 Business Recommendations

Based on the data-driven insights uncovered in this analysis, the following strategic recommendations are proposed:

| # | Recommendation | Expected Impact |
|:-:|:---|:---|
| 1 | 🚚 **Optimize logistics in high-freight-cost states** — Renegotiate carrier contracts, establish regional fulfillment centers & streamline last-mile delivery | Reduced freight costs & improved delivery margins |
| 2 | 📣 **Target marketing during peak seasonal periods** — Allocate ad spend & promotional budgets to coincide with identified high-demand windows | Higher conversion rates & maximized seasonal revenue |
| 3 | 💳 **Expand payment flexibility** — Offer more installment options & introduce BNPL (Buy Now, Pay Later) for higher-value orders | Increased average order value & customer acquisition |
| 4 | ⏱️ **Improve delivery estimation accuracy** — Refine delivery prediction models to narrow the gap between estimated and actual delivery times | Enhanced customer satisfaction & reduced complaints |
| 5 | 🌎 **Focus expansion on high-growth states** — Prioritize inventory, marketing & logistics investment in states showing strongest order growth trajectories | Accelerated market penetration & revenue growth |

---

## 👤 Author

<div align="center">

**Pritam Palit**

🎓 Electronics & Communication Engineering Graduate  
📊 Focus Areas: Data Analytics · Statistics · Business Intelligence

[![GitHub](https://img.shields.io/badge/GitHub-PritamPalit--official-181717?style=for-the-badge&logo=github)](https://github.com/PritamPalit-official)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pritam%20Palit-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/pritam-palit-77b2071b4/)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ **If you found this project useful, consider giving it a star!** ⭐

</div>
