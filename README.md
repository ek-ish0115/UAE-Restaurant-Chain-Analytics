# UAE Restaurant Chain Analytics

## 📌 Project Overview

An end-to-end data analytics project focused on analyzing the performance of a UAE-based restaurant chain.

The project combines **Snowflake, SQL, Databricks, Python, Power BI, and Streamlit** to transform raw restaurant data into business insights and interactive dashboards.

The analysis covers sales performance, branch operations, sales channels, costs, profitability, menu performance, and revenue prediction.

---

## 🎯 Business Problem

The restaurant management team needs a centralized view of business performance across branches, emirates, concepts, sales channels, and menu categories.

The key business questions include:

- How is revenue performing over time?
- Which branches and emirates generate the highest revenue?
- Which sales channels perform best?
- How do food, labour, waste, and prime costs affect profitability?
- Which menu categories and items contribute most to sales?
- What business factors are associated with restaurant revenue?
- How can management improve operational efficiency and profitability?

---

## 🎯 Project Objectives

- Analyze overall sales and revenue performance
- Compare branch and emirate performance
- Analyze sales channel contribution
- Monitor food, labour, waste, and prime costs
- Evaluate menu category and item performance
- Build interactive business dashboards
- Perform exploratory data analysis using Python
- Develop a feature-based revenue prediction model
- Generate actionable business insights

---

## 🛠️ Technology Stack

| Tool | Purpose |
|---|---|
| Snowflake | Cloud data storage and SQL analysis |
| SQL | Data cleaning, transformation and analytical queries |
| Databricks | Python-based EDA and predictive modeling |
| Python | Data analysis, visualization and machine learning |
| Power BI | Interactive business dashboards |
| Streamlit | Portfolio web application |
| GitHub | Project version control and documentation |

---

## 📊 Dataset

The project uses five main datasets.

### 1. BRANCHES

Contains branch-level information including:

- Branch ID
- Branch Name
- Emirate
- Area
- Restaurant Concept
- Seats
- Drive-through availability
- Delivery availability
- Opening Date
- Monthly Rent

### 2. CHANNEL_DAILY

Contains daily sales and sales-channel information including:

- Orders
- Covers
- Gross Sales
- Discounts
- Net Sales
- Service Charges
- VAT
- Total Billed
- Aggregator Commission
- Net Revenue
- Food Cost
- Average Preparation Time
- Review Score
- Order Channel

### 3. DAILY_OPERATIONS

Contains daily operational information including:

- Orders
- Covers
- Net Sales
- Discounts
- Aggregator Commission
- Net Revenue
- Food Cost
- Waste Cost
- Labour Hours
- Labour Cost
- Prime Cost
- Review Score

### 4. ITEM_MONTHLY_SALES

Contains monthly menu-item sales information including:

- Branch
- Business Month
- Item
- Menu Category
- Quantity Sold
- Gross Sales
- Food Cost
- Gross Margin

### 5. MENU_ITEMS

Contains menu-item master information including:

- Item Name
- Menu Category
- Menu Price
- Item Cost
- Preparation Time
- Vegetarian Status
- Calories
- Active Status
- Launch Date

---

## 🔄 Project Workflow

```text
Raw Restaurant Data
        ↓
Snowflake
        ↓
SQL Data Cleaning & Transformation
        ↓
Databricks + Python
        ↓
EDA & Predictive Modeling
        ↓
Power BI
        ↓
Interactive Dashboards
        ↓
Streamlit Portfolio Application
        ↓
GitHub
```

---

# 📈 Power BI Dashboards

The Power BI reporting layer consists of three interactive dashboards designed to provide management with a clear view of sales, operations, profitability, and channel performance.

## 1. Executive Overview

Provides a high-level view of overall restaurant business performance.

### Key KPIs

- Total Revenue
- Total Orders
- Average Order Value
- Gross Margin %
- Prime Cost %
- Net Profit

### Visualizations

- Monthly Revenue Trend
- Monthly Orders Trend
- Revenue by Branch
- Revenue by Order Channel
- Revenue by Restaurant Concept

---

## 2. Branch & Operations

Focuses on branch-level performance and operational efficiency.

### Key KPIs

- Revenue
- Orders
- Average Order Value
- Food Cost %
- Prime Cost %

### Analysis

- Revenue by Branch
- Orders by Branch
- AOV by Branch
- Food Cost % by Branch
- Prime Cost % by Branch
- Labour Cost by Branch
- Weekend vs Weekday Revenue
- Revenue by Emirate

---

## 3. Sales & Channel Insights

Focuses on sales-channel performance, discounts, and aggregator commissions.

### Key KPIs

- Net Revenue
- Total Orders
- Average Order Value
- Discount Rate
- Commission Rate

### Analysis

- Monthly Net Revenue Trend
- Revenue by Order Channel
- Orders by Order Channel
- Discount Amount by Channel
- Aggregator Commission by Channel
- Discount Rate by Channel
- Gross Sales vs Net Revenue by Channel

---

# 🤖 Predictive Analysis

A **Linear Regression** model was developed using Python and Scikit-learn to analyze the relationship between restaurant business features and revenue.

## Model Performance

| Metric | Result |
|---|---:|
| R² | 0.9768 |
| MAE | AED 2,756.69 |
| RMSE | AED 3,976.36 |

The model was evaluated using a train-test split.

> **Note:** This is a feature-based revenue prediction model using same-period aggregated business features. It should not be interpreted as a true future time-series forecast.

---

# 📊 Python Exploratory Data Analysis

Python was used for:

- Data cleaning
- Data type validation
- Missing-value analysis
- Duplicate checks
- Descriptive statistics
- Feature engineering
- Exploratory data analysis
- Revenue analysis
- Branch analysis
- Channel analysis
- Menu analysis
- Cost analysis
- Predictive modeling

## Key Visualizations

- Monthly Revenue Trend
- Monthly Orders Trend
- Revenue by Branch
- Revenue by Channel
- Revenue by Menu Category
- Net Revenue vs Food Cost
- Weekend vs Weekday Performance
- Prime Cost % by Branch

---

# 💡 Key Business Insights

The analysis provides visibility into:

- Revenue trends across the business
- Differences in branch performance
- Sales contribution across channels
- Food and labour cost behavior
- Prime cost and profitability drivers
- Menu category performance
- High-performing menu items
- Weekend versus weekday performance
- Operational efficiency
- Revenue drivers identified through predictive modeling

---

# 🚀 Business Recommendations

Based on the analysis, management can:

- Monitor branch-level performance regularly
- Optimize underperforming sales channels
- Track food and labour costs closely
- Reduce unnecessary waste
- Monitor aggregator commissions and discounts
- Focus on high-performing menu categories and items
- Review operational efficiency across branches
- Use revenue-driver analysis to support business planning

---

# 🌐 Streamlit Application

The project includes an interactive **Streamlit portfolio application** with three pages.

## Page 1 — Executive Overview

Provides an overall view of restaurant performance through KPIs, revenue trends, branch performance, channel performance, and restaurant concepts.

## Page 2 — Branch & Operations

Provides branch-level operational analysis including revenue, orders, AOV, food cost, prime cost, labour cost, weekend/weekday performance, and emirate analysis.

## Page 3 — Sales & Channel Insights

Provides sales-channel analysis including revenue, orders, discounts, commissions, AOV, and channel-level performance.

The application includes interactive filters and business-focused visualizations for exploring restaurant performance.

---

# 📂 Project Structure

```text
UAE-Restaurant-Chain-Analytics/
│
├── app.py
│
├── data/
│   ├── branches.csv
│   ├── channel_daily.csv
│   ├── daily_operations.csv
│   ├── item_monthly_sales.csv
│   └── menu_items.csv
│
├── pages/
│   ├── 2_Branch_Operations.py
│   └── 3_Sales_Channel_Insights.py
│
└── README.md
```

---

# ▶️ Run the Streamlit Application

## Step 1 — Install Required Libraries

```bash
pip install streamlit pandas numpy matplotlib
```

## Step 2 — Run the Application

```bash
python -m streamlit run app.py
```

The Streamlit application will open in your web browser.

---

# 🔍 Analytical Approach

## Descriptive Analysis

Used to understand:

- Revenue
- Orders
- AOV
- Branch performance
- Channel performance
- Menu performance
- Cost structure

## Diagnostic Analysis

Used to investigate:

- Revenue differences between branches
- Food and labour cost behavior
- Prime cost variation
- Channel performance
- Discount and commission impact
- Weekend vs weekday performance

## Predictive Analysis

Used **Linear Regression** to analyze revenue relationships with business and operational features.

---

# 📌 Key Business Metrics

## Average Order Value

```text
AOV = Total Revenue / Total Orders
```

## Gross Margin

```text
Gross Margin = Net Revenue - Food Cost
```

## Prime Cost

```text
Prime Cost = Food Cost + Labour Cost
```

## Prime Cost %

```text
Prime Cost % = Prime Cost / Net Revenue × 100
```

## Food Cost %

```text
Food Cost % = Food Cost / Net Revenue × 100
```

## Discount Rate

```text
Discount Rate = Discounts / Gross Sales × 100
```

## Aggregator Commission Rate

```text
Commission Rate = Aggregator Commission / Gross Sales × 100
```

---

# ⭐ Project Highlights

- End-to-end data analytics project
- Cloud-based data analysis using Snowflake
- SQL-based data transformation
- Python-based EDA and predictive modeling
- Databricks notebook workflow
- Interactive Power BI dashboards
- Streamlit portfolio application
- Business-focused KPI analysis
- Revenue prediction model
- GitHub project documentation

---

# 👩‍💻 Author

## Ekta Grewal

**Data Analyst | SQL | Python | Power BI | Snowflake | Databricks**

📍 Gurgaon, Haryana, India

---

# 📫 Contact

**Email:** grewalektaig98@gmail.com

**LinkedIn:** [Ekta Grewal](https://www.linkedin.com/in/ekta-grewal-121500224/)

---

# ⭐ Thank You

Thank you for visiting this project.

This project demonstrates an end-to-end approach to transforming restaurant data into meaningful business insights using modern data analytics and business intelligence tools.
