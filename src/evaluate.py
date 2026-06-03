import os
import joblib
import pandas as pd

from preprocessing import clean_text

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

# Load dataset
df = pd.read_json(
    os.path.join(
        BASE_DIR,
        "data",
        "complaints.json"
    )
)

df = df.rename(columns={
    "complaint_text": "complaint",
    "category": "department"
})

df["complaint"] = (
    df["complaint"]
    .astype(str)
    .apply(clean_text)
)

# Load models
priority_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "priority_model.pkl"
    )
)

department_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "department_model.pkl"
    )
)
CATEGORY_MAPPING = {
    "Roads & Potholes": "Road",
    "Street Lighting": "Electricity",
    "Water Supply": "Water",
    "Waste Management": "Sanitation",
    "Drainage & Sewer": "Drainage"
}

df["department"] = (
    df["department"]
    .map(CATEGORY_MAPPING)
    .fillna(df["department"])
)
# Train/Test Split for Priority
X_train, X_test, y_train, y_test = train_test_split(
    df["complaint"],
    df["priority"],
    test_size=0.2,
    random_state=42
)

priority_pred = priority_model.predict(
    X_test
)

print("\n===== PRIORITY MODEL =====")

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        priority_pred
    )
)

print(
    "Precision:",
    precision_score(
        y_test,
        priority_pred,
        average="weighted"
    )
)

print(
    "Recall:",
    recall_score(
        y_test,
        priority_pred,
        average="weighted"
    )
)

print(
    "F1:",
    f1_score(
        y_test,
        priority_pred,
        average="weighted"
    )
)

print(
    "\nClassification Report\n"
)

print(
    classification_report(
        y_test,
        priority_pred
    )
)

print(
    "\nConfusion Matrix\n"
)

print(
    confusion_matrix(
        y_test,
        priority_pred
    )
)

# Train/Test Split for Department
X_train, X_test, y_train, y_test = train_test_split(
    df["complaint"],
    df["department"],
    test_size=0.2,
    random_state=42
)

department_pred = department_model.predict(
    X_test
)

print("\n===== DEPARTMENT MODEL =====")

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        department_pred
    )
)

print(
    "Precision:",
    precision_score(
        y_test,
        department_pred,
        average="weighted"
    )
)

print(
    "Recall:",
    recall_score(
        y_test,
        department_pred,
        average="weighted"
    )
)

print(
    "F1:",
    f1_score(
        y_test,
        department_pred,
        average="weighted"
    )
)

print(
    "\nClassification Report\n"
)

print(
    classification_report(
        y_test,
        department_pred
    )
)

print(
    "\nConfusion Matrix\n"
)

print(
    confusion_matrix(
        y_test,
        department_pred
    )
)