# src/eval/eval_detector.py
from __future__ import annotations
import csv, os
import numpy as np
from sklearn.metrics import precision_recall_curve, roc_curve, auc
import matplotlib.pyplot as plt
from src.detect.regex_detector import score as rx_score
from src.detect.ml_detector import score as ml_score

INP = "data/datasets/notes_dataset.csv"
OUT_DIR = "docs/fig"
os.makedirs(OUT_DIR, exist_ok=True)

def load_xy():
    X, y = [], []
    with open(INP, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            X.append(row["text"]); y.append(int(row["label"]))
    return X, np.array(y)

if __name__ == "__main__":
    X, y = load_xy()

    # Regex score -> simple integer
    rx = np.array([rx_score(x)["score"] for x in X], dtype=float)
    # Normalize to [0,1] for plotting
    rx = (rx - rx.min()) / (rx.max() - rx.min() + 1e-9)

    # ML probability
    ml = np.array([ml_score(x)["proba"] for x in X], dtype=float)

    # ROC/PR for ML
    fpr, tpr, _ = roc_curve(y, ml); roc_auc = auc(fpr, tpr)
    p, r, _ = precision_recall_curve(y, ml); pr_auc = auc(r, p)

    # Plot ROC
    plt.figure()
    plt.plot(fpr, tpr, label=f"ML ROC (AUC={roc_auc:.2f})")
    plt.plot([0,1],[0,1],'--',label="chance")
    plt.xlabel("FPR"); plt.ylabel("TPR"); plt.legend(); plt.title("ROC — ML Detector")
    plt.tight_layout(); plt.savefig(os.path.join(OUT_DIR, "roc_ml.png"))

    # Plot PR
    plt.figure()
    plt.plot(r, p, label=f"ML PR (AUC={pr_auc:.2f})")
    plt.xlabel("Recall"); plt.ylabel("Precision"); plt.legend(); plt.title("PR — ML Detector")
    plt.tight_layout(); plt.savefig(os.path.join(OUT_DIR, "pr_ml.png"))

    # (Optional) overlay regex as a baseline
    fpr2, tpr2, _ = roc_curve(y, rx); roc2 = auc(fpr2, tpr2)
    plt.figure()
    plt.plot(fpr2, tpr2, label=f"Regex ROC (AUC={roc2:.2f})")
    plt.plot([0,1],[0,1],'--',label="chance")
    plt.xlabel("FPR"); plt.ylabel("TPR"); plt.legend(); plt.title("ROC — Regex (normalized)")
    plt.tight_layout(); plt.savefig(os.path.join(OUT_DIR, "roc_regex.png"))

    print("[OK] wrote docs/fig/roc_ml.png, pr_ml.png, roc_regex.png")
