
# Where Did My Money Go? — Anomaly Detector

## 1. Project Overview

Where Did My Money Go? is a web application that helps users explore their expenses and identify unusual transactions.

The application uses Python, Streamlit, Pandas, Plotly, and Scikit-learn. It provides spending statistics, interactive charts, CSV upload, CSV export, and anomaly detection using the Isolation Forest algorithm.

An anomaly is a transaction that differs from patterns in the available dataset. A flagged transaction is not necessarily fraudulent.

## 2. Features

- Upload transactions from a CSV file.
- Validate transaction columns and values.
- View total spending, average transaction, and largest transaction.
- Explore spending by category and over time.
- Detect unusual transaction amounts using Isolation Forest.
- Review anomaly scores and simple explanations.
- Download analyzed transactions as a CSV file.
- Run automated tests for important application functions.

## 3. Technologies

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly
- Pytest

## 4. CSV Format

The input CSV must contain these columns:

| Column | Description |
|---|---|
| Date | Transaction date |
| Category | Expense category |
| Description | Transaction description |
| Amount | Positive expense amount in PLN |

A sample dataset is included in `sample_transactions.csv`.

## 5. Installation

Clone the repository, enter the project directory, and create a virtual environment.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd where-did-my-money-go
python -m venv .venv
```

Activate the environment on Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually http://localhost:8501.

## 7. Run the Tests

```bash
python -m pytest -v
```

## 8. Machine Learning Method

The application uses Isolation Forest, an unsupervised anomaly-detection algorithm. In the current version, the model uses transaction amount as its input feature.

The model's output identifies unusual observations relative to the dataset. The score is not a fraud probability, and the application does not establish whether a transaction is fraudulent.

## 9. Limitations

- The model currently uses transaction amount only.
- Results depend on the data supplied by the user.
- Small datasets may not represent normal spending patterns.
- The current model has not been validated against a labelled real-world fraud dataset.
- The explanation shown in the interface is a simple rule-based description, not a detailed explanation of the model.

## 10. Privacy and Data

The included sample transactions are fictional. Users should avoid uploading sensitive financial information to any public deployment.

## 11. Future Improvements

- Add category and time-based features.
- Allow users to adjust anomaly-detection sensitivity.
- Add filters and monthly comparisons.
- Evaluate the model using a labelled test dataset.
- Improve anomaly explanations.

## 12. Academic Use

This project demonstrates data processing, web application development, unsupervised machine learning, testing, and data visualization.
