
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dominoz Predictive System", layout="wide")

st.title("🍕 Dominoz Predictive Purchase Order System")
st.subheader("Data Science Project")

st.write("Welcome! This application analyzes Dominoz sales and ingredient data.")




import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dominoz Predictive Purchase Order System",
    layout="wide"
)

st.title("🍕 Dominoz Predictive Purchase Order System")
st.subheader("Data Science Project")
st.write("This application analyzes Dominoz sales and ingredient data.")

# Load datasets
sales = pd.read_csv("data/sales_data.csv")
ingredients = pd.read_csv("data/ingredients_data.csv")

st.success("Datasets loaded successfully ✅")

# Show previews
st.header("📄 Sales Data Preview")
st.dataframe(sales.head())

st.header("📄 Ingredients Data Preview")
st.dataframe(ingredients.head())




st.write(sales.columns)
st.write(ingredients.columns)




st.header("📊 Key Sales Metrics")

daily_avg = sales["quantity"].mean()
weekly_avg = sales["quantity"].sum() / 7

col1, col2 = st.columns(2)
col1.metric("Average Daily Sales", f"{daily_avg:.2f}")
col2.metric("Average Weekly Sales", f"{weekly_avg:.2f}")




st.header("📈 Sales Trend")

# Convert date properly (Indian format: DD-MM-YYYY)
sales["order_date"] = pd.to_datetime(
    sales["order_date"],
    dayfirst=True,
    errors="coerce"
)

daily_sales = sales.groupby("order_date").size()

st.line_chart(daily_sales)





st.header("🧂 Ingredient Consumption Analysis")

ingredient_usage = ingredients.copy()

# Estimate daily usage based on average sales
ingredient_usage["estimated_usage"] = (
    ingredient_usage["Items_Qty_In_Grams"] * daily_avg
)

st.dataframe(
    ingredient_usage[
        ["pizza_name", "pizza_ingredients", "Items_Qty_In_Grams", "estimated_usage"]
    ]
)




# Remove duplicates by grouping properly
ingredient_usage = (
    ingredient_usage
    .groupby("pizza_ingredients", as_index=False)
    .agg({"estimated_usage": "sum"})
)

st.header("🚨 Low Stock Alert")

# Simulated available stock (for demo purposes)
ingredient_usage["available_stock"] = ingredient_usage["estimated_usage"] * 0.8

low_stock = ingredient_usage[
    ingredient_usage["available_stock"] < ingredient_usage["estimated_usage"]
]

if low_stock.empty:
    st.success("All ingredients are sufficiently stocked ✅")
else:
    st.warning("Some ingredients need restocking ⚠️")
    st.dataframe(
        low_stock[
            ["pizza_ingredients", "estimated_usage", "available_stock"]
        ]
    )




st.sidebar.header("🔍 Filters")

selected_category = st.sidebar.multiselect(
    "Select Pizza Category",
    sales["pizza_category"].unique(),
    default=sales["pizza_category"].unique()
)

filtered_sales = sales[sales["pizza_category"].isin(selected_category)]





st.markdown("---")
st.caption(
    "📌 Dominoz Predictive Purchase Order System | Data Science Project"
)




st.header("⏰ Hour-wise Order Demand")
# SAFE conversion (handles errors)
sales["order_time"] = pd.to_datetime(
    sales["order_time"],
    errors="coerce"
)

# Drop invalid times
sales_time = sales.dropna(subset=["order_time"])

# Extract hour
sales_time["order_hour"] = sales_time["order_time"].dt.hour

hourly_orders = sales_time.groupby("order_hour").size()

st.bar_chart(hourly_orders)



st.header("📦 Purchase Order Recommendation")

ingredient_usage["reorder_quantity"] = (
    ingredient_usage["estimated_usage"] - ingredient_usage["available_stock"]
)

purchase_order = ingredient_usage[
    ingredient_usage["reorder_quantity"] > 0
]

if purchase_order.empty:
    st.success("No purchase order needed today ✅")
else:
    st.warning("Purchase order required for below ingredients ⚠️")
    st.dataframe(
        purchase_order[
            ["pizza_ingredients", "reorder_quantity"]
        ]
    )




st.sidebar.title("🔍 Dashboard Controls")

st.markdown("---")
st.caption("🍕 Dominoz Predictive Purchase Order System | Data Science Project")





st.sidebar.subheader("⚙️ Stock Simulation")

stock_ratio = st.sidebar.slider(
    "Available Stock (% of Estimated Usage)",
    min_value=50,
    max_value=120,
    value=80
)

ingredient_usage["available_stock"] = (
    ingredient_usage["estimated_usage"] * stock_ratio / 100
)




st.header("🛡️ Safety Stock Concept")

st.write("""
Safety stock is extra inventory maintained to avoid stockouts due to:
- Sudden demand spikes
- Supplier delays
- Forecasting uncertainty

In this project, safety stock can be calculated as:

Safety Stock = (Maximum Daily Usage − Average Daily Usage) × Lead Time

This ensures uninterrupted operations even during demand fluctuations.
""")




st.header("📅 Weekly & Monthly Demand Forecast")

weekly_demand = daily_avg * 7
monthly_demand = daily_avg * 30

col1, col2 = st.columns(2)
col1.metric("Estimated Weekly Demand", f"{weekly_demand:.2f}")
col2.metric("Estimated Monthly Demand", f"{monthly_demand:.2f}")




st.header("📌 Key Insights & Recommendations")

st.write("""
• Peak demand occurs during specific hours – staffing and inventory should be adjusted accordingly  
• Certain ingredients frequently hit low-stock levels  
• Predictive ordering helps avoid last-minute shortages  
• This system supports cost-effective inventory management
""")





st.markdown("---")
st.caption("🍕 Dominoz Predictive Purchase Order System | MBA Data Science Project")





