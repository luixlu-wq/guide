"""Stage 4 Topic 06: PyTorch/CUDA bridge (intermediate).

Data: synthetic regression data generated in-script
Rows: 30,000
Input shape: [N, 8]
Target: linear regression target, shape [N, 1]
Split: fixed train/validation split
Type: device-aware training + timing
"""

from __future__ import annotations

import time

import torch
from torch.utils.data import DataLoader, TensorDataset, random_split

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 30_000):
    generator = torch.Generator(device="cpu").manual_seed(62)
    x = torch.randn((n_rows, 8), generator=generator)
    w = torch.tensor([[1.4], [-0.7], [0.9], [0.4], [0.1], [-0.2], [0.3], [0.8]])
    y = x @ w + 0.15 * torch.randn((n_rows, 1), generator=generator)
    return x, y


def eval_loss(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module, device: torch.device) -> float:
    model.eval()
    total = 0.0
    rows = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            loss = loss_fn(model(xb), yb)
            total += float(loss.item()) * xb.size(0)
            rows += xb.size(0)
    return total / rows


def avg_matmul_time(device: torch.device, size: int, iters: int) -> float:
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)
    if device.type == "cuda":
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(iters):
        _ = a @ b
    if device.type == "cuda":
        torch.cuda.synchronize()
    t1 = time.perf_counter()
    return (t1 - t0) / iters


# Workflow:
# 1) Select cpu/cuda device and move model/tensors consistently.
# 2) Train mini-batch regression and report train/validation loss.
# 3) Show optional CPU vs GPU matrix timing when CUDA is available.
def main() -> None:
    torch.manual_seed(62)

    x, y = make_data(n_rows=scaled_int(30_000, quick_value=10_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    dataset = TensorDataset(x, y)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    split_gen = torch.Generator().manual_seed(62)
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=split_gen)

    train_loader = DataLoader(train_ds, batch_size=256, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=512, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.nn.Sequential(
        torch.nn.Linear(8, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 1),
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()

    epochs = scaled_int(15, quick_value=6)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, max(2, epochs // 2), epochs):
            train_mse = eval_loss(model, train_loader, loss_fn, device)
            val_mse = eval_loss(model, val_loader, loss_fn, device)
            print(f"epoch={epoch:02d} train_mse={train_mse:.4f} val_mse={val_mse:.4f}")

    print("selected_device=", device)
    matmul_size = scaled_int(1024, quick_value=512)
    matmul_iters = scaled_int(20, quick_value=8)
    cpu_time = avg_matmul_time(torch.device("cpu"), size=matmul_size, iters=matmul_iters)
    print(f"cpu_matmul_avg_s={cpu_time:.6f}")

    if torch.cuda.is_available():
        gpu_time = avg_matmul_time(torch.device("cuda"), size=matmul_size, iters=matmul_iters)
        print(f"gpu_matmul_avg_s={gpu_time:.6f}")
        print(f"cpu_gpu_speedup={cpu_time / gpu_time:.2f}x")
    else:
        print("gpu_timing_skipped=CUDA unavailable (CPU fallback path used)")


if __name__ == "__main__":
    main()
