"""Step 3a - Real-time inference API, deployed to ECS Express Mode."""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from src.config import FEATURES, MODEL_PATH

app = FastAPI(title="Cancer risk demo API")
model = joblib.load(MODEL_PATH)


class Record(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_smoothness: float
    mean_compactness: float
    mean_symmetry: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(r: Record):
    row = pd.DataFrame([[r.mean_radius, r.mean_texture, r.mean_smoothness,
                         r.mean_compactness, r.mean_symmetry]], columns=FEATURES)
    prob = float(model.predict_proba(row)[0][1])
    return {"benign_probability": round(prob, 4), "label": int(prob >= 0.5)}
