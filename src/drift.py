"""Step 4 - Drift check: compare training data with new data, feature by feature (KS test)."""
import sys
import pandas as pd
from scipy.stats import ks_2samp
from src.config import FEATURES

ref = pd.read_csv("data/train.csv")
new = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/new_batch.csv")
drifted = []
print(f"{'feature':20} {'p_value':>8}  status")
for f in FEATURES:
    p = ks_2samp(ref[f], new[f]).pvalue
    status = "DRIFT" if p < 0.05 else "ok"
    if status == "DRIFT":
        drifted.append(f)
    print(f"{f:20} {p:8.4f}  {status}")
print(f"\n{len(drifted)} of {len(FEATURES)} features drifted: {drifted}")
sys.exit(1 if drifted else 0)
