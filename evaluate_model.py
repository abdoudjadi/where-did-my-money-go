
from sklearn.ensemble import IsolationForest

# Synthetic data for a controlled experiment.
# These labels are known because we created the dataset ourselves.

normal_amounts = [
    5, 8, 12, 15, 18, 22, 25, 30, 35, 40,
    45, 50, 60, 75, 90, 110, 12, 20, 28, 38,
    48, 55, 65, 80, 95, 10, 16, 24, 32, 42,
    52, 62, 72, 85, 100, 7, 14, 21, 29, 37,
    46, 58, 68, 78, 88, 9, 17, 26, 34, 44,
    54, 64, 74, 84, 105, 11, 19, 27, 36, 49,
]

unusual_amounts = [450, 650, 950, 1200, 1800]

amounts = normal_amounts + unusual_amounts

# 0 = expected normal transaction, 1 = deliberately unusual transaction
actual_labels = [0] * len(normal_amounts) + [1] * len(unusual_amounts)

# Use the same Isolation Forest settings as the website.
model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42,
)

predictions = model.fit_predict([[amount] for amount in amounts])

# Convert the model output: -1 means anomaly; 1 means normal.
predicted_labels = [1 if prediction == -1 else 0 for prediction in predictions]

true_positives = sum(
    actual == 1 and predicted == 1
    for actual, predicted in zip(actual_labels, predicted_labels)
)
false_positives = sum(
    actual == 0 and predicted == 1
    for actual, predicted in zip(actual_labels, predicted_labels)
)
false_negatives = sum(
    actual == 1 and predicted == 0
    for actual, predicted in zip(actual_labels, predicted_labels)
)
true_negatives = sum(
    actual == 0 and predicted == 0
    for actual, predicted in zip(actual_labels, predicted_labels)
)

precision = (
    true_positives / (true_positives + false_positives)
    if true_positives + false_positives else 0
)
recall = (
    true_positives / (true_positives + false_negatives)
    if true_positives + false_negatives else 0
)
accuracy = (
    (true_positives + true_negatives) / len(amounts)
)

print("WHERE DID MY MONEY GO? — CONTROLLED EXPERIMENT")
print("-" * 48)
print(f"Total transactions: {len(amounts)}")
print(f"Expected unusual transactions: {sum(actual_labels)}")
print(f"Transactions flagged by model: {sum(predicted_labels)}")
print()
print("Confusion matrix counts:")
print(f"True positives:  {true_positives}")
print(f"False positives: {false_positives}")
print(f"False negatives: {false_negatives}")
print(f"True negatives:  {true_negatives}")
print()
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"Accuracy:  {accuracy:.2%}")
print()
print("Flagged transaction amounts:")
for amount, prediction in zip(amounts, predicted_labels):
    if prediction == 1:
        print(f"{amount:.2f} PLN")
print()
print("Important: these metrics apply only to this synthetic dataset.")
