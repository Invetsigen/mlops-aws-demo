"""Step 3b - Batch inference: score a whole file at once."""
import sys
import joblib
import pandas as pd
from src.config import FEATURES, MODEL_PATH

src = sys.argv[1] if len(sys.argv) > 1 else "data/new_batch.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "data/predictions.csv"
df = pd.read_csv(src)
df["benign_probability"] = joblib.load(MODEL_PATH).predict_proba(df[FEATURES])[:, 1].round(4)
df.to_csv(out, index=False)
print(f"Scored {len(df)} rows -> {out}")
