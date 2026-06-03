import os
import joblib
import pandas as pd

from preprocessing import clean_text

from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "complaints.json"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

df = pd.read_json(DATA_PATH)
df = df.rename(columns={
    "complaint_text": "complaint",
    "category": "department"
})

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

df = df.rename(columns={
    "complaint_text": "complaint",
    "category": "department"
})

df = df.dropna()

df["complaint"] = (
    df["complaint"]
    .astype(str)
    .apply(clean_text)
)

X = df["complaint"]

# Shared Vectorizer

vectorizer = TfidfVectorizer(
    max_features=15000,
    ngram_range=(1,2),
    stop_words="english"
)

vectorizer.fit(X)

joblib.dump(
    vectorizer,
    os.path.join(
        MODEL_DIR,
        "complaint_vectorizer.pkl"
    )
)

# Priority Model

priority_model = Pipeline([
    (
        "tfidf",
        vectorizer
    ),
    (
        "clf",
        LogisticRegression(
            max_iter=2000
        )
    )
])

priority_model.fit(
    X,
    df["priority"]
)

joblib.dump(
    priority_model,
    os.path.join(
        MODEL_DIR,
        "priority_model.pkl"
    )
)

# Department Model

department_model = Pipeline([
    (
        "tfidf",
        vectorizer
    ),
    (
        "clf",
        LogisticRegression(
            max_iter=2000
        )
    )
])

department_model.fit(
    X,
    df["department"]
)

joblib.dump(
    department_model,
    os.path.join(
        MODEL_DIR,
        "department_model.pkl"
    )
)

print(
    "Training completed"
)
