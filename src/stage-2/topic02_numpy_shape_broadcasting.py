"""NumPy shape inspection and broadcasting.

Data: synthetic matrix and vectors
Rows: matrix 3x4
Features: numeric matrix values
Target: none
Type: array operations
"""

import numpy as np


def main():
    a = np.arange(12).reshape(3, 4)
    row_bias = np.array([10, 20, 30, 40])      # shape (4,)
    col_scale = np.array([[1], [10], [100]])   # shape (3,1)

    add_result = a + row_bias
    scale_result = a * col_scale

    print("a shape:", a.shape)
    print("row_bias shape:", row_bias.shape)
    print("col_scale shape:", col_scale.shape)
    print()
    print("a + row_bias:")
    print(add_result)
    print()
    print("a * col_scale:")
    print(scale_result)


if __name__ == "__main__":
    main()
