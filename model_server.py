from flask import Flask, request, jsonify
import base64
import random
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "server": "EC2-damage-detection",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image provided"}), 400

        img_b64 = data['image']

        # Validate base64
        try:
            img_data = base64.b64decode(img_b64)
            logger.info(f"Received image of size: {len(img_data)} bytes")
        except Exception:
            return jsonify({"error": "Invalid base64 image"}), 400

        # Simulated ML inference
        classes = ["damaged", "no_damage", "unknown"]
        predicted_class = random.choice(classes)
        confidence = round(random.uniform(0.80, 0.97), 4)
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        logger.info(
            f"Prediction: {predicted_class} "
            f"({confidence}) — ID: {prediction_id}"
        )

        return jsonify({
            "prediction_id":    prediction_id,
            "predicted_class":  predicted_class,
            "confidence":       confidence,
            "timestamp":        timestamp,
            "server":           "EC2",
            "image_size_bytes": len(img_data)
        })

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)