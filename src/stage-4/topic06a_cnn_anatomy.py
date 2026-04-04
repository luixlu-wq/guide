"""Stage 4 Section 6A: CNN anatomy with manual Sobel filtering.

Data Source: sklearn.datasets.load_digits
Schema: grayscale image [H, W] from digits sample
Preprocessing: method-chaining normalization to [0,1]
Null Handling: none (source dataset is complete)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
from sklearn.datasets import load_digits

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def conv2d_same(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # Manual 2D convolution (same output size) to expose filter mechanics.
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
    out = np.zeros_like(image, dtype=np.float64)
    for i in range(h):
        for j in range(w):
            patch = padded[i : i + kh, j : j + kw]
            out[i, j] = float(np.sum(patch * kernel))
    return out


# Workflow:
# 1) Load one digit image via method-chaining style table normalization.
# 2) Apply manual Sobel-X and Sobel-Y filters.
# 3) Visualize original vs edge maps and save evidence artifact.
def main() -> None:
    data = load_digits(as_frame=True).frame
    feature_cols = [c for c in data.columns if c != "target"]
    df = (
        data
        .assign(**{c: data[c].astype("float32") / 16.0 for c in feature_cols})
        .loc[:, [*feature_cols, "target"]]
    )

    row_idx = 0
    image = df.loc[row_idx, feature_cols].to_numpy(dtype=np.float64).reshape(8, 8)
    target = int(df.loc[row_idx, "target"])

    sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=np.float64)
    sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float64)

    gx = conv2d_same(image, sobel_x)
    gy = conv2d_same(image, sobel_y)
    mag = np.sqrt(gx**2 + gy**2)

    print("Data declaration")
    print("source=sklearn.load_digits(as_frame=True)")
    print("input_shape=(8,8) target=", target)
    print("CNN contract reminder: model input should be NCHW -> (N,1,H,W)")
    print(f"edge_stats gx_mean={gx.mean():.4f} gy_mean={gy.mean():.4f} mag_max={mag.max():.4f}")

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Original")
    axes[1].imshow(gx, cmap="gray")
    axes[1].set_title("Sobel X")
    axes[2].imshow(gy, cmap="gray")
    axes[2].set_title("Sobel Y")
    axes[3].imshow(mag, cmap="gray")
    axes[3].set_title("Gradient Magnitude")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    img_path = out_dir / "topic06a_sobel_demo.png"
    plt.savefig(img_path, dpi=140)
    plt.close(fig)

    pd.DataFrame(
        [
            {
                "sample_index": row_idx,
                "target": target,
                "gx_mean": float(gx.mean()),
                "gy_mean": float(gy.mean()),
                "mag_max": float(mag.max()),
            }
        ]
    ).to_csv(out_dir / "topic06a_sobel_summary.csv", index=False)

    print(f"Saved: {img_path}")
    print(f"Saved: {out_dir / 'topic06a_sobel_summary.csv'}")
    print("Interpretation: Sobel filters show how CNN kernels extract local edge patterns.")


if __name__ == "__main__":
    main()
