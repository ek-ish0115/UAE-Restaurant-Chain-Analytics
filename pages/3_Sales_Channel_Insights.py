import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales & Channel Insights",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Sales & Channel Insights")

st.markdown(
    """
    ### Understanding Revenue Performance Across Sales Channels

    Analyze **net revenue, orders, AOV, discounts, aggregator
    commissions and channel-level sales performance** across the
    UAE restaurant chain.
    """
)

st.divider()


# ============================================================
# PROJECT FOCUS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Focus", "Sales")

with col2:
    st.metric("🛒 Channels", "Order Channels")

with col3:
    st.metric("🏷️ Analysis", "Discounts")

with col4:
    st.metric("💳 Analysis", "Commissions")

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

branches = pd.read_csv("data/branches.csv")
channel_daily = pd.read_csv("data/channel_daily.csv")


# ============================================================
# DATA PREPARATION
# ============================================================

channel_daily["business_date"] = pd.to_datetime(
    channel_daily["business_date"],
    errors="coerce"
)

numeric_columns = [
    "orders_count",
    "covers",
    "gross_sales_aed",
    "discounts_aed",
    "net_sales_aed",
    "service_charge_aed",
    "vat_aed",
    "total_billed_aed",
    "aggregator_commission_aed",
    "net_revenue_aed",
    "food_cost_aed"
]

for col in numeric_columns:

    if col in channel_daily.columns:

        channel_daily[col] = pd.to_numeric(
            channel_daily[col],
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


channels = channel_daily.merge(
    branch_info,
    on="branch_id",
    how="left"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🍽️ UAE Restaurant Analytics")
st.sidebar.caption("Sales & Channel Dashboard")
st.sidebar.divider()

st.sidebar.title("🔎 Sales Filters")


# ============================================================
# EMIRATE FILTER
# ============================================================

emirates = sorted(
    channels["emirate"]
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
    channels[
        channels["emirate"]
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
    channels[
        channels["concept"]
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
# CHANNEL FILTER
# ============================================================

channels_available = sorted(
    channels[
        channels["branch_name"]
        .astype(str)
        .isin(selected_branches)
    ]["order_channel"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_channels = st.sidebar.multiselect(
    "Order Channel",
    channels_available,
    default=channels_available
)


# ============================================================
# FILTER DATA
# ============================================================

filtered = channels[
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
    &
    channels["order_channel"]
    .astype(str)
    .isin(selected_channels)
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered[
    "net_revenue_aed"
].sum()

total_orders = filtered[
    "orders_count"
].sum()

total_gross_sales = filtered[
    "gross_sales_aed"
].sum()

total_discounts = filtered[
    "discounts_aed"
].sum()

total_commission = filtered[
    "aggregator_commission_aed"
].sum()


aov = (
    total_revenue / total_orders
    if total_orders != 0
    else 0
)

discount_rate = (
    total_discounts
    / total_gross_sales
    * 100
    if total_gross_sales != 0
    else 0
)

commission_rate = (
    total_commission
    / total_gross_sales
    * 100
    if total_gross_sales != 0
    else 0
)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Sales Performance KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "💰 Net Revenue",
        f"AED {total_revenue:,.0f}"
    )

with col2:

    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,.0f}"
    )

with col3:

    st.metric(
        "🧾 AOV",
        f"AED {aov:,.2f}"
    )

with col4:

    st.metric(
        "🏷️ Discount Rate",
        f"{discount_rate:.2f}%"
    )

with col5:

    st.metric(
        "💳 Commission Rate",
        f"{commission_rate:.2f}%"
    )


st.divider()


# ============================================================
# MONTHLY NET REVENUE
# ============================================================

st.subheader("📈 Monthly Net Revenue Trend")

monthly_revenue = (
    filtered
    .groupby(
        filtered["business_date"]
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


chart = (
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
            title="Net Revenue (AED)",
            scale=alt.Scale(zero=False)
        ),
        tooltip=[
            alt.Tooltip(
                "month:N",
                title="Month"
            ),
            alt.Tooltip(
                "net_revenue:Q",
                title="Net Revenue",
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
# REVENUE & ORDERS BY CHANNEL
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("💰 Revenue by Order Channel")

    channel_revenue = (
        filtered
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

    chart = (
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
                title="Net Revenue (AED)",
                scale=alt.Scale(zero=True)
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
        chart,
        use_container_width=True
    )


with col2:

    st.subheader("🛒 Orders by Order Channel")

    channel_orders = (
        filtered
        .groupby(
            "order_channel",
            as_index=False
        )["orders_count"]
        .sum()
        .sort_values(
            "orders_count",
            ascending=False
        )
    )

    chart = (
        alt.Chart(channel_orders)
        .mark_bar()
        .encode(
            x=alt.X(
                "order_channel:N",
                title="Order Channel",
                sort="-y"
            ),
            y=alt.Y(
                "orders_count:Q",
                title="Orders",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "order_channel:N",
                    title="Channel"
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
# DISCOUNTS & COMMISSIONS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏷️ Discount Amount by Channel")

    discount_channel = (
        filtered
        .groupby(
            "order_channel",
            as_index=False
        )["discounts_aed"]
        .sum()
        .sort_values(
            "discounts_aed",
            ascending=False
        )
    )

    chart = (
        alt.Chart(discount_channel)
        .mark_bar()
        .encode(
            x=alt.X(
                "order_channel:N",
                title="Order Channel",
                sort="-y"
            ),
            y=alt.Y(
                "discounts_aed:Q",
                title="Discounts (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "order_channel:N",
                    title="Channel"
                ),
                alt.Tooltip(
                    "discounts_aed:Q",
                    title="Discounts",
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


with col2:

    st.subheader("💳 Aggregator Commission by Channel")

    commission_channel = (
        filtered
        .groupby(
            "order_channel",
            as_index=False
        )["aggregator_commission_aed"]
        .sum()
        .sort_values(
            "aggregator_commission_aed",
            ascending=False
        )
    )

    chart = (
        alt.Chart(commission_channel)
        .mark_bar()
        .encode(
            x=alt.X(
                "order_channel:N",
                title="Order Channel",
                sort="-y"
            ),
            y=alt.Y(
                "aggregator_commission_aed:Q",
                title="Commission (AED)",
                scale=alt.Scale(zero=True)
            ),
            tooltip=[
                alt.Tooltip(
                    "order_channel:N",
                    title="Channel"
                ),
                alt.Tooltip(
                    "aggregator_commission_aed:Q",
                    title="Commission",
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
# DISCOUNT RATE BY CHANNEL
# ============================================================

st.subheader("📊 Discount Rate by Channel")

discount_rate_channel = (
    filtered
    .groupby(
        "order_channel",
        as_index=False
    )
    .agg(
        gross_sales=(
            "gross_sales_aed",
            "sum"
        ),
        discounts=(
            "discounts_aed",
            "sum"
        )
    )
)

discount_rate_channel["discount_rate"] = (
    discount_rate_channel["discounts"]
    /
    discount_rate_channel["gross_sales"]
    .replace(0, pd.NA)
    * 100
)

discount_rate_channel["discount_rate"] = (
    discount_rate_channel["discount_rate"]
    .fillna(0)
)

discount_rate_channel = (
    discount_rate_channel
    .sort_values(
        "discount_rate",
        ascending=False
    )
)


chart = (
    alt.Chart(discount_rate_channel)
    .mark_bar()
    .encode(
        x=alt.X(
            "order_channel:N",
            title="Order Channel",
            sort="-y"
        ),
        y=alt.Y(
            "discount_rate:Q",
            title="Discount Rate (%)",
            scale=alt.Scale(zero=True)
        ),
        tooltip=[
            alt.Tooltip(
                "order_channel:N",
                title="Channel"
            ),
            alt.Tooltip(
                "discount_rate:Q",
                title="Discount Rate",
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
# GROSS SALES VS NET REVENUE
# ============================================================

st.subheader("📈 Gross Sales vs Net Revenue by Channel")

sales_comparison = (
    filtered
    .groupby(
        "order_channel",
        as_index=False
    )
    .agg(
        gross_sales=(
            "gross_sales_aed",
            "sum"
        ),
        net_revenue=(
            "net_revenue_aed",
            "sum"
        )
    )
)

sales_comparison_long = sales_comparison.melt(
    id_vars="order_channel",
    value_vars=[
        "gross_sales",
        "net_revenue"
    ],
    var_name="metric",
    value_name="amount"
)

sales_comparison_long["metric"] = (
    sales_comparison_long["metric"].map(
        {
            "gross_sales": "Gross Sales",
            "net_revenue": "Net Revenue"
        }
    )
)


chart = (
    alt.Chart(sales_comparison_long)
    .mark_bar()
    .encode(
        x=alt.X(
            "order_channel:N",
            title="Order Channel"
        ),
        xOffset="metric:N",
        y=alt.Y(
            "amount:Q",
            title="Amount (AED)",
            scale=alt.Scale(zero=True)
        ),
        tooltip=[
            alt.Tooltip(
                "order_channel:N",
                title="Channel"
            ),
            alt.Tooltip(
                "metric:N",
                title="Metric"
            ),
            alt.Tooltip(
                "amount:Q",
                title="Amount",
                format=",.0f"
            )
        ]
    )
    .properties(height=300)
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
        "Total channel records:",
        len(channels)
    )

    st.write(
        "Filtered records:",
        len(filtered)
    )

    st.write(
        "Order Channels:",
        channels[
            "order_channel"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    st.write(
        "Net Revenue:",
        f"AED {total_revenue:,.2f}"
    )

    st.write(
        "Gross Sales:",
        f"AED {total_gross_sales:,.2f}"
    )

    st.write(
        "Total Discounts:",
        f"AED {total_discounts:,.2f}"
    )

    st.write(
        "Aggregator Commission:",
        f"AED {total_commission:,.2f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UAE Restaurant Chain Analytics | "
    "Sales & Channel Insights"
)