import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Branch & Operations",
    page_icon="🏢",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🏢 Branch & Operations")

st.markdown(
    """
    ### Understanding Branch Performance & Operational Efficiency

    Analyze **revenue, orders, AOV, food cost, labour cost,
    prime cost and weekend/weekday performance** across the
    UAE restaurant chain.
    """
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

branches = pd.read_csv("data/branches.csv")
daily_operations = pd.read_csv("data/daily_operations.csv")


# ============================================================
# DATA PREPARATION
# ============================================================

daily_operations["business_date"] = pd.to_datetime(
    daily_operations["business_date"],
    errors="coerce"
)

numeric_columns = [
    "orders_count",
    "covers",
    "net_sales_aed",
    "discounts_aed",
    "net_revenue_aed",
    "food_cost_aed",
    "waste_cost_aed",
    "labour_hours",
    "labour_cost_aed",
    "prime_cost_pct",
    "avg_review_score"
]

for col in numeric_columns:
    if col in daily_operations.columns:
        daily_operations[col] = pd.to_numeric(
            daily_operations[col],
            errors="coerce"
        ).fillna(0)


# ============================================================
# BRANCH INFORMATION
# ============================================================

branch_info = branches[
    [
        "branch_id",
        "branch_name",
        "emirate",
        "concept"
    ]
].drop_duplicates("branch_id")


operations = daily_operations.merge(
    branch_info,
    on="branch_id",
    how="left"
)


# ============================================================
# DAY TYPE
# ============================================================

def convert_day_type(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip().lower()

    if value in [
        "true",
        "1",
        "1.0",
        "yes",
        "y",
        "weekend"
    ]:
        return "Weekend"

    if value in [
        "false",
        "0",
        "0.0",
        "no",
        "n",
        "weekday"
    ]:
        return "Weekday"

    return "Unknown"


operations["day_type"] = operations[
    "is_weekend"
].apply(convert_day_type)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🍽️ UAE Restaurant Analytics")
st.sidebar.caption("Branch & Operations Dashboard")
st.sidebar.divider()

st.sidebar.title("🔎 Branch Filters")


# ============================================================
# EMIRATE FILTER
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


# ============================================================
# CONCEPT FILTER
# ============================================================

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


# ============================================================
# BRANCH FILTER
# ============================================================

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
# DAY TYPE FILTER
# ============================================================

day_types = sorted(
    operations[
        operations["branch_name"]
        .astype(str)
        .isin(selected_branches)
    ]["day_type"]
    .dropna()
    .unique()
    .tolist()
)

selected_day_types = st.sidebar.multiselect(
    "Day Type",
    day_types,
    default=day_types
)


# ============================================================
# FILTER DATA
# ============================================================

filtered = operations[
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
    &
    operations["day_type"]
    .astype(str)
    .isin(selected_day_types)
].copy()


# ============================================================
# PAGE KPI CALCULATIONS
# ============================================================

total_revenue = filtered[
    "net_revenue_aed"
].sum()

total_orders = filtered[
    "orders_count"
].sum()

total_food_cost = filtered[
    "food_cost_aed"
].sum()

total_labour_cost = filtered[
    "labour_cost_aed"
].sum()

aov = (
    total_revenue / total_orders
    if total_orders != 0
    else 0
)

food_cost_pct = (
    total_food_cost / total_revenue * 100
    if total_revenue != 0
    else 0
)

prime_cost = (
    total_food_cost + total_labour_cost
)

prime_cost_pct = (
    prime_cost / total_revenue * 100
    if total_revenue != 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Branch Performance KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💰 Revenue",
        f"AED {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Orders",
        f"{total_orders:,.0f}"
    )

with col3:
    st.metric(
        "🧾 AOV",
        f"AED {aov:,.2f}"
    )

with col4:
    st.metric(
        "🥘 Food Cost",
        f"{food_cost_pct:.2f}%"
    )

with col5:
    st.metric(
        "⚙️ Prime Cost",
        f"{prime_cost_pct:.2f}%"
    )


st.divider()


# ============================================================
# REVENUE BY BRANCH
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("💰 Revenue by Branch")

    branch_revenue = (
        filtered
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

    chart = (
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
                title="Revenue (AED)",
                scale=alt.Scale(zero=True)
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
        chart,
        use_container_width=True
    )


# ============================================================
# ORDERS BY BRANCH
# ============================================================

with col2:

    st.subheader("🛒 Orders by Branch")

    branch_orders = (
        filtered
        .groupby(
            "branch_name",
            as_index=False
        )["orders_count"]
        .sum()
        .sort_values(
            "orders_count",
            ascending=False
        )
    )

    chart = (
        alt.Chart(branch_orders)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "orders_count:Q",
                title="Orders",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "orders_count:Q",
                    title="Orders",
                    format=","
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


# ============================================================
# AOV BY BRANCH
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🧾 AOV by Branch")

    branch_aov = (
        filtered
        .groupby(
            "branch_name",
            as_index=False
        )
        .agg(
            revenue=("net_revenue_aed", "sum"),
            orders=("orders_count", "sum")
        )
    )

    branch_aov["aov"] = (
        branch_aov["revenue"]
        / branch_aov["orders"].replace(0, pd.NA)
    )

    branch_aov["aov"] = (
        branch_aov["aov"].fillna(0)
    )

    branch_aov = branch_aov.sort_values(
        "aov",
        ascending=False
    )

    chart = (
        alt.Chart(branch_aov)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "aov:Q",
                title="AOV (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "aov:Q",
                    title="AOV",
                    format=".2f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


# ============================================================
# FOOD COST % BY BRANCH
# ============================================================

with col2:

    st.subheader("🥘 Food Cost % by Branch")

    food_cost_branch = (
        filtered
        .groupby(
            "branch_name",
            as_index=False
        )
        .agg(
            revenue=("net_revenue_aed", "sum"),
            food_cost=("food_cost_aed", "sum")
        )
    )

    food_cost_branch["food_cost_pct"] = (
        food_cost_branch["food_cost"]
        / food_cost_branch["revenue"].replace(0, pd.NA)
        * 100
    )

    food_cost_branch["food_cost_pct"] = (
        food_cost_branch["food_cost_pct"].fillna(0)
    )

    food_cost_branch = food_cost_branch.sort_values(
        "food_cost_pct",
        ascending=False
    )

    chart = (
        alt.Chart(food_cost_branch)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "food_cost_pct:Q",
                title="Food Cost (%)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "food_cost_pct:Q",
                    title="Food Cost %",
                    format=".2f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


# ============================================================
# PRIME COST % BY BRANCH
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("⚙️ Prime Cost % by Branch")

    prime_cost_branch = (
        filtered
        .groupby(
            "branch_name",
            as_index=False
        )
        .agg(
            revenue=("net_revenue_aed", "sum"),
            food_cost=("food_cost_aed", "sum"),
            labour_cost=("labour_cost_aed", "sum")
        )
    )

    prime_cost_branch["prime_cost_pct"] = (
        (
            prime_cost_branch["food_cost"]
            + prime_cost_branch["labour_cost"]
        )
        / prime_cost_branch["revenue"].replace(0, pd.NA)
        * 100
    )

    prime_cost_branch["prime_cost_pct"] = (
        prime_cost_branch["prime_cost_pct"].fillna(0)
    )

    prime_cost_branch = prime_cost_branch.sort_values(
        "prime_cost_pct",
        ascending=False
    )

    chart = (
        alt.Chart(prime_cost_branch)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "prime_cost_pct:Q",
                title="Prime Cost (%)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "prime_cost_pct:Q",
                    title="Prime Cost %",
                    format=".2f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


# ============================================================
# LABOUR COST BY BRANCH
# ============================================================

with col2:

    st.subheader("👷 Labour Cost by Branch")

    labour_branch = (
        filtered
        .groupby(
            "branch_name",
            as_index=False
        )["labour_cost_aed"]
        .sum()
        .sort_values(
            "labour_cost_aed",
            ascending=False
        )
    )

    chart = (
        alt.Chart(labour_branch)
        .mark_bar()
        .encode(
            x=alt.X(
                "branch_name:N",
                title="Branch",
                sort="-y"
            ),
            y=alt.Y(
                "labour_cost_aed:Q",
                title="Labour Cost (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "branch_name:N",
                    title="Branch"
                ),
                alt.Tooltip(
                    "labour_cost_aed:Q",
                    title="Labour Cost",
                    format=",.0f"
                )
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


# ============================================================
# WEEKEND VS WEEKDAY
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📅 Weekend vs Weekday Revenue")

    day_revenue = (
        filtered
        .groupby(
            "day_type",
            as_index=False
        )["net_revenue_aed"]
        .sum()
    )

    chart = (
        alt.Chart(day_revenue)
        .mark_bar()
        .encode(
            x=alt.X(
                "day_type:N",
                title="Day Type"
            ),
            y=alt.Y(
                "net_revenue_aed:Q",
                title="Revenue (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "day_type:N",
                    title="Day Type"
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
        chart,
        use_container_width=True
    )


# ============================================================
# REVENUE BY EMIRATE
# ============================================================

with col2:

    st.subheader("🌍 Revenue by Emirate")

    emirate_revenue = (
        filtered
        .groupby(
            "emirate",
            as_index=False
        )["net_revenue_aed"]
        .sum()
        .sort_values(
            "net_revenue_aed",
            ascending=False
        )
    )

    chart = (
        alt.Chart(emirate_revenue)
        .mark_bar()
        .encode(
            x=alt.X(
                "emirate:N",
                title="Emirate",
                sort="-y"
            ),
            y=alt.Y(
                "net_revenue_aed:Q",
                title="Revenue (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "emirate:N",
                    title="Emirate"
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
        chart,
        use_container_width=True
    )


# ============================================================
# DATA CHECK
# ============================================================

with st.expander("🔍 Data Check"):

    st.write(
        "Total operation records:",
        len(daily_operations)
    )

    st.write(
        "Filtered records:",
        len(filtered)
    )

    st.write(
        "Branches:",
        len(branches)
    )

    st.write(
        "Day Types:",
        operations["day_type"].unique().tolist()
    )

    st.write(
        "Filtered Revenue:",
        f"AED {total_revenue:,.2f}"
    )

    st.write(
        "Filtered Orders:",
        f"{total_orders:,.0f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UAE Restaurant Chain Analytics | "
    "Branch & Operations"
)