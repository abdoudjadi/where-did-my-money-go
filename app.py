
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

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
    data["Description"] = (
        data["Description"].fillna("No description").astype(str)
    )

    data = data[data["Amount"] > 0].copy()

    if data.empty:
        return None, "No valid positive transactions were found."

    return data, None


def detect_anomalies(data):
    result = data.copy()

    # With very little data, the model cannot learn a useful pattern.
    if len(result) < 5 or result["Amount"].nunique() < 2:
        result["Anomaly"] = "Not evaluated"
        result["Anomaly Score"] = 0.0
        result["Reason"] = (
            "Not enough varied transactions for reliable detection."
        )
        return result

    # Use transaction amount as the first and simplest ML feature.
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
    )

    predictions = model.fit_predict(result[["Amount"]])
    scores = model.decision_function(result[["Amount"]])

    result["Anomaly"] = [
        "Unusual" if prediction == -1 else "Normal"
        for prediction in predictions
    ]

    # Lower decision scores indicate more unusual observations.
    result["Anomaly Score"] = scores

    median_amount = result["Amount"].median()

    def explain_row(row):
        if row["Anomaly"] != "Unusual":
            return "No unusual amount pattern detected."

        if row["Amount"] > median_amount:
            return "Amount is unusually high compared with this dataset."

        return "Amount is unusually low compared with this dataset."

    result["Reason"] = result.apply(explain_row, axis=1)
    return result


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

# Run the machine-learning model.
analyzed = detect_anomalies(transactions)

total_spending = analyzed["Amount"].sum()
average_transaction = analyzed["Amount"].mean()
largest_transaction = analyzed["Amount"].max()
unusual_count = (analyzed["Anomaly"] == "Unusual").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spending", f"{total_spending:.2f} PLN")
col2.metric("Average Transaction", f"{average_transaction:.2f} PLN")
col3.metric("Largest Transaction", f"{largest_transaction:.2f} PLN")
col4.metric("Unusual Transactions", int(unusual_count))


st.subheader("Spending Over Time")

daily_spending = (
    analyzed.assign(Date=analyzed["Date"].dt.date)
    .groupby("Date", as_index=False)["Amount"]
    .sum()
)

trend_fig = px.line(
    daily_spending,
    x="Date",
    y="Amount",
    markers=True,
    title="Daily Spending",
    labels={"Amount": "Spending (PLN)", "Date": "Transaction Date"},
)

st.plotly_chart(trend_fig, use_container_width=True)


st.subheader("Spending by Category")

category_totals = (
    analyzed.groupby("Category", as_index=False)["Amount"]
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


st.subheader("Machine Learning Results")

normal_count = (analyzed["Anomaly"] == "Normal").sum()
evaluated_count = (analyzed["Anomaly"] != "Not evaluated").sum()

eval_col1, eval_col2, eval_col3 = st.columns(3)
eval_col1.metric("Transactions Evaluated", int(evaluated_count))
eval_col2.metric("Flagged for Review", int(unusual_count))
eval_col3.metric("Not Flagged", int(normal_count))

st.info(
    "Evaluation note: Isolation Forest is an unsupervised anomaly-detection "
    "algorithm. Without independently verified labels, we cannot calculate "
    "meaningful precision, recall, or accuracy. These counts describe the "
    "model's output, not its proven ability to detect fraud."
)

st.write(
    "Isolation Forest compares transaction amounts and flags observations "
    "that look unusual within the uploaded dataset."
)

unusual = analyzed[analyzed["Anomaly"] == "Unusual"]

if unusual.empty:
    st.success("No unusual transactions were detected in this dataset.")
else:
    st.warning(
        f"{len(unusual)} transaction(s) were flagged for review. "
        "This does not mean they are fraudulent."
    )
    st.dataframe(
        unusual[
            ["Date", "Category", "Description", "Amount", "Anomaly Score", "Reason"]
        ].sort_values("Anomaly Score"),
        use_container_width=True,
        hide_index=True,
    )


st.subheader("Export Your Results")

export_data = analyzed.copy()
export_data["Date"] = export_data["Date"].dt.strftime("%Y-%m-%d")

csv_data = export_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Analyzed Transactions (CSV)",
    data=csv_data,
    file_name="analyzed_transactions.csv",
    mime="text/csv",
)


with st.expander("View all analyzed transactions"):
    st.dataframe(
        analyzed.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Demo application using fictional or user-provided data. "
    "Anomaly flags are statistical clues, not proof of fraud."
)
