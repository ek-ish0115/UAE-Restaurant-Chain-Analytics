import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="UAE Restaurant Analytics",
    page_icon="🍽️",
    layout="wide"
)


# ============================================================
# PROFESSIONAL HEADER
# ============================================================

st.title("🍽️ UAE Restaurant Chain Analytics")

st.markdown(
    """
    ### Turning Restaurant Data into Business Insights

    An interactive analytics application designed to analyze
    **sales performance, branch operations, costs, profitability
    and sales channels** across the UAE restaurant chain.
    """
)

st.divider()


# ============================================================
# PROJECT OVERVIEW CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏢 Branches", "18")

with col2:
    st.metric("🌍 Emirates", "6")

with col3:
    st.metric("📊 Dashboard Pages", "3")

with col4:
    st.metric("🛠️ Tools", "5")

st.divider()


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.subheader("📌 Project Overview")

st.write(
    """
    This project provides a centralized view of restaurant business
    performance by analyzing sales, branch operations, costs,
    profitability and sales channels across the UAE restaurant chain.

    The project uses **Snowflake, Databricks, Python, Power BI and
    Streamlit** for descriptive, diagnostic and predictive analysis.
    """
)

st.divider()


# ============================================================
# DASHBOARD NAVIGATION OVERVIEW
# ============================================================

st.subheader("📂 Explore the Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        ### 🏠 Executive Overview

        Monitor overall revenue, orders, AOV, gross margin,
        prime cost and business performance.
        """
    )

with col2:
    st.markdown(
        """
        ### 🏢 Branch & Operations

        Analyze branch performance, operational costs,
        food cost, labour cost and prime cost.
        """
    )

with col3:
    st.markdown(
        """
        ### 📊 Sales & Channel Insights

        Compare order channels, revenue, discounts,
        aggregator commissions and sales trends.
        """
    )

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

branches = pd.read_csv("data/branches.csv")
channel_daily = pd.read_csv("data/channel_daily.csv")
daily_operations = pd.read_csv("data/daily_operations.csv")
item_monthly_sales = pd.read_csv("data/item_monthly_sales.csv")
menu_items = pd.read_csv("data/menu_items.csv")


# ============================================================
# PREPARE DATA
# ============================================================

branch_info = branches[
    ["branch_id", "branch_name", "emirate", "concept"]
].drop_duplicates("branch_id")

operations = daily_operations.merge(
    branch_info,
    on="branch_id",
    how="left"
)

channels = channel_daily.merge(
    branch_info,
    on="branch_id",
    how="left"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🍽️ UAE Restaurant Analytics")
st.sidebar.caption("Business Intelligence Dashboard")
st.sidebar.divider()

st.sidebar.title("🔎 Filters")


# ============================================================
# FILTERS
# ============================================================

emirates = sorted(
    operations["emirate"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_emirates = st.sidebar.multiselect(
    "Emirate",
    emirates,
    default=emirates
)


concepts = sorted(
    operations[
        operations["emirate"]
        .astype(str)
        .isin(selected_emirates)
    ]["concept"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_concepts = st.sidebar.multiselect(
    "Concept",
    concepts,
    default=concepts
)


branches_available = sorted(
    operations[
        operations["concept"]
        .astype(str)
        .isin(selected_concepts)
    ]["branch_name"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_branches = st.sidebar.multiselect(
    "Branch",
    branches_available,
    default=branches_available
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_operations = operations[
    operations["emirate"]
    .astype(str)
    .isin(selected_emirates)
    &
    operations["concept"]
    .astype(str)
    .isin(selected_concepts)
    &
    operations["branch_name"]
    .astype(str)
    .isin(selected_branches)
].copy()


filtered_channels = channels[
    channels["emirate"]
    .astype(str)
    .isin(selected_emirates)
    &
    channels["concept"]
    .astype(str)
    .isin(selected_concepts)
    &
    channels["branch_name"]
    .astype(str)
    .isin(selected_branches)
].copy()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.header("📈 Executive Overview")

st.caption(
    "Overall sales, order and profitability performance"
)


# ============================================================
# KPIs
# ============================================================

total_revenue = filtered_operations[
    "net_revenue_aed"
].sum()

total_orders = filtered_operations[
    "orders_count"
].sum()

total_food_cost = filtered_operations[
    "food_cost_aed"
].sum()

total_labour_cost = filtered_operations[
    "labour_cost_aed"
].sum()

gross_profit = total_revenue - total_food_cost

gross_margin = (
    gross_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)

prime_cost = total_food_cost + total_labour_cost

prime_cost_pct = (
    prime_cost / total_revenue * 100
    if total_revenue != 0
    else 0
)

aov = (
    total_revenue / total_orders
    if total_orders != 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"AED {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,.0f}"
    )

with col3:
    st.metric(
        "🧾 Average Order Value",
        f"AED {aov:,.2f}"
    )

with col4:
    st.metric(
        "📈 Gross Margin",
        f"{gross_margin:.2f}%"
    )

with col5:
    st.metric(
        "⚙️ Prime Cost",
        f"{prime_cost_pct:.2f}%"
    )


st.divider()


# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

st.subheader("📈 Monthly Revenue Trend")

filtered_operations["business_date"] = pd.to_datetime(
    filtered_operations["business_date"],
    errors="coerce"
)

monthly_revenue = (
    filtered_operations
    .groupby(
        filtered_operations["business_date"]
        .dt.to_period("M")
        .astype(str),
        as_index=False
    )["net_revenue_aed"]
    .sum()
)

monthly_revenue.columns = [
    "month",
    "net_revenue"
]


monthly_chart = (
    alt.Chart(monthly_revenue)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "month:N",
            title="Month",
            sort=None,
            axis=alt.Axis(labelAngle=-45)
        ),
        y=alt.Y(
            "net_revenue:Q",
            title="Revenue (AED)",
            scale=alt.Scale(zero=False)
        ),
        tooltip=[
            alt.Tooltip(
                "month:N",
                title="Month"
            ),
            alt.Tooltip(
                "net_revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    )
    .properties(height=280)
)

st.altair_chart(
    monthly_chart,
    use_container_width=True
)


# ============================================================
# REVENUE BY BRANCH
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏢 Revenue by Branch")

    branch_revenue = (
        filtered_operations
        .groupby(
            "branch_name",
            as_index=False
        )["net_revenue_aed"]
        .sum()
        .sort_values(
            "net_revenue_aed",
            ascending=False
        )
    )

    branch_chart = (
        alt.Chart(branch_revenue)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "net_revenue_aed:Q",
                title="Revenue (AED)"
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "net_revenue_aed:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        branch_chart,
        use_container_width=True
    )


# ============================================================
# REVENUE BY ORDER CHANNEL
# ============================================================

with col2:

    st.subheader("📊 Revenue by Order Channel")

    channel_revenue = (
        filtered_channels
        .groupby(
            "order_channel",
            as_index=False
        )["net_revenue_aed"]
        .sum()
        .sort_values(
            "net_revenue_aed",
            ascending=False
        )
    )

    channel_chart = (
        alt.Chart(channel_revenue)
        .mark_bar()
        .encode(
            x=alt.X(
                "order_channel:N",
                title="Order Channel",
                sort="-y"
            ),
            y=alt.Y(
                "net_revenue_aed:Q",
                title="Revenue (AED)"
            ),
            tooltip=[
                alt.Tooltip(
                    "order_channel:N",
                    title="Channel"
                ),
                alt.Tooltip(
                    "net_revenue_aed:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        channel_chart,
        use_container_width=True
    )


# ============================================================
# REVENUE BY CONCEPT
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🍽️ Revenue by Restaurant Concept")

    concept_revenue = (
        filtered_operations
        .groupby(
            "concept",
            as_index=False
        )["net_revenue_aed"]
        .sum()
        .sort_values(
            "net_revenue_aed",
            ascending=False
        )
    )

    concept_chart = (
        alt.Chart(concept_revenue)
        .mark_bar()
        .encode(
            x=alt.X(
                "concept:N",
                title="Restaurant Concept",
                sort="-y"
            ),
            y=alt.Y(
                "net_revenue_aed:Q",
                title="Revenue (AED)"
            ),
            tooltip=[
                alt.Tooltip(
                    "concept:N",
                    title="Concept"
                ),
                alt.Tooltip(
                    "net_revenue_aed:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=260)
    )

    st.altair_chart(
        concept_chart,
        use_container_width=True
    )


# ============================================================
# MONTHLY ORDERS
# ============================================================

with col2:

    st.subheader("🛒 Monthly Orders Trend")

    monthly_orders = (
        filtered_operations
        .groupby(
            filtered_operations["business_date"]
            .dt.to_period("M")
            .astype(str),
            as_index=False
        )["orders_count"]
        .sum()
    )

    monthly_orders.columns = [
        "month",
        "orders"
    ]

    orders_chart = (
        alt.Chart(monthly_orders)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "month:N",
                title="Month",
                sort=None,
                axis=alt.Axis(labelAngle=-45)
            ),
            y=alt.Y(
                "orders:Q",
                title="Orders"
            ),
            tooltip=[
                alt.Tooltip(
                    "month:N",
                    title="Month"
                ),
                alt.Tooltip(
                    "orders:Q",
                    title="Orders",
                    format=","
                )
            ]
        )
        .properties(height=260)
    )

    st.altair_chart(
        orders_chart,
        use_container_width=True
    )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.divider()

st.subheader("💡 Executive Summary")

st.markdown(
    f"""
    - **Total Revenue:** AED {total_revenue:,.0f}
    - **Total Orders:** {total_orders:,.0f}
    - **Average Order Value:** AED {aov:,.2f}
    - **Gross Margin:** {gross_margin:.2f}%
    - **Prime Cost:** {prime_cost_pct:.2f}%
    - **Branches Analyzed:** {len(selected_branches)}
    - **Emirates Analyzed:** {len(selected_emirates)}
    """
)


# ============================================================
# DATA CHECK
# ============================================================

with st.expander("🔍 Data Check"):

    st.write(
        "Branches:",
        len(branches)
    )

    st.write(
        "Channel records:",
        len(channel_daily)
    )

    st.write(
        "Operations records:",
        len(daily_operations)
    )

    st.write(
        "Item sales records:",
        len(item_monthly_sales)
    )

    st.write(
        "Menu items:",
        len(menu_items)
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UAE Restaurant Chain Analytics | "
    "Snowflake • Databricks • Python • Power BI • Streamlit"
)