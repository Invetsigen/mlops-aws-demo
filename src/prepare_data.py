"""Step 1 - Data pipeline. Builds train, test and a 'new week' file with drift."""
import os
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from src.config import FEATURES, TARGET

os.makedirs("data", exist_ok=True)
df = load_breast_cancer(as_frame=True).frame[FEATURES + [TARGET]]
train, test = train_test_split(df, test_size=0.3, random_state=42, stratify=df[TARGET])
train.to_csv("data/train.csv", index=False)
test.to_csv("data/test.csv", index=False)

# Simulate next week's traffic: same rows, but two features shifted (data drift).
rng = np.random.default_rng(7)
new = test.drop(columns=[TARGET]).copy()
new["mean radius"] = new["mean radius"] * 1.25
new["mean texture"] = new["mean texture"] + rng.normal(4, 1, len(new))
new.to_csv("data/new_batch.csv", index=False)
print(f"train={len(train)} test={len(test)} new_batch={len(new)} rows written to data/")
