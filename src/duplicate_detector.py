import os
import joblib
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import clean_text

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

# Load vectorizer
vectorizer = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "complaint_vectorizer.pkl"
    )
)

# Load dataset
dataset = pd.read_json(
    os.path.join(
        BASE_DIR,
        "data",
        "complaints.json"
    )
)

# Rename columns
dataset = dataset.rename(
    columns={
        "complaint_text": "complaint",
        "category": "department"
    }
)

# Clean complaints
dataset["complaint"] = (
    dataset["complaint"]
    .astype(str)
    .apply(clean_text)
)

# Create vectors
stored_vectors = vectorizer.transform(
    dataset["complaint"]
)


def find_duplicate(
    complaint,
    threshold=0.80
):
    complaint = clean_text(
        str(complaint)
    )

    vector = vectorizer.transform(
        [complaint]
    )

    similarities = cosine_similarity(
        vector,
        stored_vectors
    )[0]

    max_score = float(
        similarities.max()
    )

    if max_score >= threshold:

        index = similarities.argmax()

        return {
            "duplicate": True,
            "similarity": round(
                max_score,
                3
            ),
            "matchedComplaint":
                dataset.iloc[index][
                    "complaint"
                ],
            "department":
                dataset.iloc[index][
                    "department"
                ],
            "priority":
                dataset.iloc[index][
                    "priority"
                ]
        }

    return {
        "duplicate": False,
        "similarity": round(
            max_score,
            3
        )
    }