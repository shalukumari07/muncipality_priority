from flask import (
    Flask,
    request,
    jsonify
)

from predictor import (
    predict_complaint
)

from duplicate_detector import (
    find_duplicate
)

app = Flask(__name__)


@app.route("/health")
def health():

    return jsonify({
        "status": "running"
    })


@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    data = request.get_json()

    complaint = data.get(
        "complaint",
        ""
    )

    prediction = predict_complaint(
        complaint
    )

    duplicate = find_duplicate(
        complaint
    )

    return jsonify({

        "success": True,

        "prediction":
            prediction,

        "duplicate":
            duplicate
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )