"""Stage 4 Topic 01: neural anatomy with PyTorch (baseline, industry-style).

Data Source: synthetic regression data generated in script
Schema: 2 numeric features | target continuous scalar
Preprocessing: none required (already standardized synthetic draw)
Null Handling: none (generated tensors are complete)
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset, random_split

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 8_000):
    generator = torch.Generator(device="cpu").manual_seed(7)
    x = torch.randn((n_rows, 2), generator=generator)
    noise = 0.15 * torch.randn((n_rows, 1), generator=generator)
    y = 1.8 * x[:, :1] - 0.7 * x[:, 1:] + 0.5 + noise
    return x, y


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def evaluate(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module, device: torch.device) -> float:
    model.eval()
    total_loss = 0.0
    total_rows = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            pred = model(xb)
            loss = loss_fn(pred, yb)
            batch = xb.size(0)
            total_loss += float(loss.item()) * batch
            total_rows += batch
    return total_loss / total_rows


def grad_l2(model: torch.nn.Module) -> float:
    sq = 0.0
    for p in model.parameters():
        if p.grad is not None:
            sq += float(torch.sum(p.grad.detach() ** 2).item())
    return sq**0.5


def write_artifacts(
    run_id: str,
    rows: list[dict],
    first_val_mse: float,
    last_val_mse: float,
    device: torch.device,
    diagnosis: str,
    decision: str,
) -> None:
    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)

    trace_df = pd.DataFrame(rows)
    trace_path = out_dir / "topic01_loop_training_trace.csv"
    trace_df.to_csv(trace_path, index=False)

    evidence = [
        {
            "run_id": run_id,
            "stage": "4",
            "topic_or_module": "topic01_pytorch_neural_anatomy",
            "metric_name": "val_mse",
            "before_value": first_val_mse,
            "after_value": last_val_mse,
            "delta": last_val_mse - first_val_mse,
            "dataset_or_eval_set": "synthetic_2d_regression",
            "seed_or_config_id": "seed7",
            "decision": decision,
            "failure_class": "training_or_optimization",
            "diagnosis": diagnosis,
            "device": device.type,
        }
    ]
    evidence_csv = out_dir / "topic01_before_after_metrics.csv"
    evidence_json = out_dir / "topic01_before_after_metrics.json"
    pd.DataFrame(evidence).to_csv(evidence_csv, index=False)
    evidence_json.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    print(f"Saved: {trace_path}")
    print(f"Saved: {evidence_csv}")
    print(f"Saved: {evidence_json}")


# Workflow:
# 1) Generate synthetic regression data and fixed train/validation split.
# 2) Execute the 5-step loop on selected device:
#    move -> forward -> loss -> backward -> optimizer step.
# 3) Track train/validation MSE and gradient norms.
# 4) Print diagnosis and save evidence artifacts.
def main() -> None:
    torch.manual_seed(7)
    device = pick_device()
    run_id = f"stage4_topic01_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    x, y = make_data(n_rows=scaled_int(8_000, quick_value=3_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic, rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))
    print(f"selected_device={device}")

    dataset = TensorDataset(x, y)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    split_gen = torch.Generator().manual_seed(7)
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=split_gen)

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(train_ds, batch_size=128, shuffle=True, pin_memory=pin_memory)
    val_loader = DataLoader(val_ds, batch_size=256, shuffle=False, pin_memory=pin_memory)

    model = torch.nn.Sequential(
        torch.nn.Linear(2, 16),
        torch.nn.ReLU(),
        torch.nn.Linear(16, 1),
    ).to(device)
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)

    epochs = scaled_int(25, quick_value=10)
    trace_rows: list[dict] = []
    first_val_mse = None
    last_val_mse = None

    for epoch in range(1, epochs + 1):
        model.train()
        grad_last = 0.0
        for xb, yb in train_loader:
            # Step 1) Move batch to device.
            xb = xb.to(device, non_blocking=pin_memory)
            yb = yb.to(device, non_blocking=pin_memory)

            # Step 2) Forward pass.
            pred = model(xb)

            # Step 3) Loss computation.
            loss = loss_fn(pred, yb)

            # Step 4) Backward pass.
            optimizer.zero_grad()
            loss.backward()
            grad_last = grad_l2(model)

            # Step 5) Optimizer update.
            optimizer.step()

        if epoch in (1, 5, 10, 15, 20, 25):
            train_mse = evaluate(model, train_loader, loss_fn, device)
            val_mse = evaluate(model, val_loader, loss_fn, device)
            if first_val_mse is None:
                first_val_mse = val_mse
            last_val_mse = val_mse
            trace_rows.append(
                {
                    "epoch": epoch,
                    "train_mse": train_mse,
                    "val_mse": val_mse,
                    "grad_l2_last_batch": grad_last,
                }
            )
            print(
                f"epoch={epoch:02d} train_mse={train_mse:.4f} "
                f"val_mse={val_mse:.4f} grad_l2={grad_last:.4f}"
            )

    if first_val_mse is None or last_val_mse is None:
        raise RuntimeError("Missing validation checkpoints in training trace.")

    delta = last_val_mse - first_val_mse
    if last_val_mse < first_val_mse * 0.45:
        diagnosis = "healthy_convergence"
        decision = "promote"
        print("DIAGNOSIS: Healthy convergence with stable gradient behavior.")
    elif last_val_mse < first_val_mse:
        diagnosis = "slow_convergence"
        decision = "hold"
        print("DIAGNOSIS: Learning is slow. Tune LR/epochs or model width.")
    else:
        diagnosis = "optimization_failure"
        decision = "rollback"
        print("DIAGNOSIS: Validation did not improve. Audit loop ordering and LR settings.")

    print(f"Validation MSE delta: {delta:.6f} ({first_val_mse:.6f} -> {last_val_mse:.6f})")
    write_artifacts(run_id, trace_rows, first_val_mse, last_val_mse, device, diagnosis, decision)
    print("Interpretation: this baseline script mirrors the production PyTorch training loop pattern.")


if __name__ == "__main__":
    main()

