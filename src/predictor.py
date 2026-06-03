import os
import joblib

from preprocessing import clean_text

from rules import (
    EMERGENCY_KEYWORDS,
    DEPARTMENT_RULES
)

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

priority_model = joblib.load(
    os.path.join(
        MODELS_DIR,
        "priority_model.pkl"
    )
)

department_model = joblib.load(
    os.path.join(
        MODELS_DIR,
        "department_model.pkl"
    )
)


def get_department_by_rules(complaint):

    for dept, keywords in DEPARTMENT_RULES.items():

        if any(
            keyword in complaint
            for keyword in keywords
        ):
            return dept

    return None


def predict_complaint(complaint):

    complaint = clean_text(
        str(complaint)
    )

    # ----------------------------
    # Priority Prediction
    # ----------------------------

    priority_probs = (
        priority_model.predict_proba(
            [complaint]
        )[0]
    )

    priority = (
        priority_model.predict(
            [complaint]
        )[0]
    )

    priority_confidence = float(
        priority_probs.max()
    )

    # ----------------------------
    # Department Prediction
    # ----------------------------

    department_probs = (
        department_model.predict_proba(
            [complaint]
        )[0]
    )

    department = (
        department_model.predict(
            [complaint]
        )[0]
    )

    department_confidence = float(
        department_probs.max()
    )

    # ----------------------------
    # Emergency Override
    # ----------------------------

    for keyword in EMERGENCY_KEYWORDS:

        if keyword in complaint:

            priority = "High"
            priority_confidence = 0.99

            rule_department = (
                get_department_by_rules(
                    complaint
                )
            )

            if rule_department:
                department = rule_department
                department_confidence = 0.99

            break

    # ----------------------------
    # Department Rule Fallback
    # ----------------------------

    if department_confidence < 0.70:

        rule_department = (
            get_department_by_rules(
                complaint
            )
        )

        if rule_department:
            department = rule_department
            department_confidence = 0.95

    # ----------------------------
    # Priority Rule Fallback
    # ----------------------------

    if any(
        word in complaint
        for word in [
            "burst",
            "flood",
            "accident",
            "danger",
            "fire",
            "explosion",
            "collapse",
            "live wire",
            "electrocution"
        ]
    ):

        priority = "High"

        if priority_confidence < 0.95:
            priority_confidence = 0.95

    return {

        "priority":
            priority,

        "priorityConfidence":
            round(
                priority_confidence,
                3
            ),

        "department":
            department,

        "departmentConfidence":
            round(
                department_confidence,
                3
            )
    }