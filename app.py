
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Where Did My Money Go?",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Where Did My Money Go?")
st.write("Track your spending and discover unusual transactions.")

# Sample transaction data for our first version
transactions = pd.DataFrame({
    "Date": [
        "2026-10-02", "2026-10-03", "2026-10-04",
        "2026-10-05", "2026-10-06", "2026-10-07",
        "2026-10-08", "2026-10-09", "2026-10-10",
        "2026-10-11", "2026-10-12", "2026-10-13",
    ],
    "Category": [
        "Food", "Transport", "Shopping", "Food",
        "Bills", "Transport", "Food", "Entertainment",
        "Shopping", "Food", "Bills", "Transport",
    ],
    "Description": [
        "Groceries", "Bus ticket", "Clothes", "Lunch",
        "Phone bill", "Tram ticket", "Supermarket",
        "Cinema", "Headphones", "Restaurant",
        "Internet bill", "Train ticket",
    ],
    "Amount": [
        45.50, 8.00, 120.00, 22.00,
        65.00, 6.00, 38.50, 35.00,
        250.00, 75.00, 55.00, 18.00,
    ],
})

transactions["Date"] = pd.to_datetime(transactions["Date"])

# Dashboard statistics
total_spending = transactions["Amount"].sum()
average_transaction = transactions["Amount"].mean()
largest_transaction = transactions["Amount"].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Spending", f"{total_spending:.2f} PLN")
col2.metric("Average Transaction", f"{average_transaction:.2f} PLN")
col3.metric("Largest Transaction", f"{largest_transaction:.2f} PLN")

st.subheader("Spending by Category")

category_totals = (
    transactions.groupby("Category", as_index=False)["Amount"]
    .sum()
    .sort_values("Amount", ascending=False)
)

fig = px.bar(
    category_totals,
    x="Category",
    y="Amount",
    color="Category",
    title="Total Spending per Category",
    labels={"Amount": "Spending (PLN)"},
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Your Transactions")
st.dataframe(transactions, use_container_width=True, hide_index=True)

st.caption(
    "Demo application using fictional transaction data. "
    "All amounts are in PLN."
)
