"""Stage 5 Topic 00A: PyTorch + CUDA basics (simple).

Data: synthetic random tensors
Records/Samples: 2 matrices
Input schema: float tensors [rows, cols]
Output schema: tensor operations summary + device report
Split/Eval policy: not applicable
Type: framework/device basics
"""

from __future__ import annotations

import time

import torch


# Workflow:
# 1) Detect available compute device (cpu or cuda).
# 2) Create tensors on the selected device.
# 3) Run basic operations and print results.
def main() -> None:
    torch.manual_seed(7)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Data declaration")
    print("source=synthetic_random_tensors")
    print("records=2")
    print("input_schema=tensor:float[4,4]")
    print("output_schema=op_results + device_metadata")
    print(f"torch_version={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"selected_device={device.type}")
    if torch.cuda.is_available():
        print(f"cuda_device_count={torch.cuda.device_count()}")
        print(f"cuda_device_name={torch.cuda.get_device_name(0)}")

    a = torch.randn(4, 4, device=device)
    b = torch.randn(4, 4, device=device)

    start = time.perf_counter()
    c = a @ b
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(f"a_device={a.device}")
    print(f"b_device={b.device}")
    print(f"c_shape={tuple(c.shape)}")
    print(f"c_mean={float(c.mean().item()):.6f}")
    print(f"single_matmul_ms={elapsed_ms:.3f}")
    print("Interpretation: PyTorch runs on CPU by default and uses CUDA when available.")


if __name__ == "__main__":
    main()
