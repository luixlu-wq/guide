"""NumPy vectorization vs Python loop.

Data: synthetic numeric array from numpy random generator
Rows: 1,000,000
Features: one numeric column (x)
Target: none
Type: numerical computation
"""

import time

import numpy as np


def main():
    rng = np.random.default_rng(42)
    x = rng.normal(loc=0.0, scale=1.0, size=1_000_000).astype(np.float64)

    t0 = time.perf_counter()
    loop_out = np.empty_like(x)
    for i, v in enumerate(x):
        loop_out[i] = v * 2.0 + 1.0
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    vec_out = x * 2.0 + 1.0
    t3 = time.perf_counter()

    same = np.allclose(loop_out, vec_out)

    print("shape:", x.shape, "dtype:", x.dtype)
    print(f"loop time       : {t1 - t0:.4f}s")
    print(f"vectorized time : {t3 - t2:.4f}s")
    print("outputs equal   :", same)
    if t3 - t2 > 0:
        print(f"speedup         : {(t1 - t0) / (t3 - t2):.2f}x")


if __name__ == "__main__":
    main()
