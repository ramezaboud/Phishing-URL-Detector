# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
import sys
from .feature_extractor import extract_features

app = FastAPI(title="PhishGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class WebsiteScanRequest(BaseModel):
    url: str


# --- Model Loading with Proper Error Handling ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_engine/phishing_nn_model.pkl')
model = None

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"WARNING: Model file not found at: {MODEL_PATH}")
    print("   Please run 'python ml_engine/train.py' first to train and save the model.")
except Exception as e:
    print(f"ERROR: Could not load model: {e}")


@app.post("/predict")
async def predict_phishing(request: WebsiteScanRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first by running: python ml_engine/train.py"
        )

    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required.")

    try:
        feature_vector = extract_features(request.url)
        feature_array = np.array(feature_vector).reshape(1, -1)

        prediction = model.predict(feature_array)[0]
        confidence = np.max(model.predict_proba(feature_array))

        final_verdict = "Legitimate" if prediction == 1 else "Phishing"

        return {
            "verdict": final_verdict,
            "confidenceScore": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))