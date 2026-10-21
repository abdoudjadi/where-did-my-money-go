
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

REQUIRED_COLUMNS = ["Date", "Category", "Description", "Amount"]


def load_sample_data():
    return pd.read_csv("sample_transactions.csv")


def validate_transactions(data):
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]

    if missing:
        return None, f"Missing required columns: {', '.join(missing)}"

    data = data[REQUIRED_COLUMNS].copy()

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")

    invalid_rows = data["Date"].isna() | data["Amount"].isna()
    data = data.loc[~invalid_rows].copy()

    data["Category"] = data["Category"].fillna("Other").astype(str)
    data["Description"] = data["Description"].fillna("No description").astype(str)

    # Expenses should be positive numbers in this demo.
    data = data[data["Amount"] > 0].copy()

    if data.empty:
        return None, "No valid positive transactions were found."

    return data, None


st.sidebar.header("Transaction Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        raw_data = pd.read_csv(uploaded_file)
        transactions, error = validate_transactions(raw_data)

        if error:
            st.error(error)
            st.stop()

        st.sidebar.success("CSV uploaded successfully.")
        st.sidebar.caption(
            "Invalid dates, invalid amounts, zero amounts, "
            "and negative amounts are excluded."
        )
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()
else:
    try:
        raw_data = load_sample_data()
        transactions, error = validate_transactions(raw_data)

        if error:
            st.error(error)
            st.stop()
    except FileNotFoundError:
        st.error("sample_transactions.csv was not found in the project folder.")
        st.stop()

    st.sidebar.info("Using fictional sample transactions.")

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
    "Demo application using fictional or user-provided data. "
    "All amounts are treated as expenses in PLN."
)
