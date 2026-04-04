"""Shared utilities for Stage 6 AI-agent runnable examples.

Design goals for this utility module:
1. Keep examples fully runnable without cloud credentials.
2. Keep behavior deterministic so learners can compare before/after changes.
3. Expose transparent helper functions with explicit schema and comments.
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# Resolve directories relative to this utility file so scripts can run from any cwd.
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "stage-6"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


@dataclass
class TicketRecord:
    """Canonical in-memory representation for support-ticket lab rows."""

    ticket_id: str
    customer_tier: str
    subject: str
    body: str
    created_at: str


def ensure_stage6_dirs() -> None:
    """Create required data/results folders if they do not exist yet."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def get_ticket_schema() -> dict[str, Any]:
    """Return explicit input/output schema declarations for handbook consistency."""
    return {
        "data": "red-book/data/stage-6/tickets_sample.csv",
        "records": 60,
        "input_schema": {
            "ticket_id": "string",
            "customer_tier": "string",
            "subject": "string",
            "body": "string",
            "created_at": "datetime",
        },
        "output_schema": {
            "ticket_id": "string",
            "predicted_priority": "enum(low,medium,high,critical)",
            "queue": "enum(general,billing,outage,security)",
            "draft_reply": "string",
            "citations": "array<string>",
            "needs_human_approval": "bool",
            "failure_class": "string|null",
        },
    }


def print_data_declaration(title: str) -> None:
    """Print a consistent data declaration block for every script."""
    schema = get_ticket_schema()
    print(f"\n=== {title}: Data Declaration ===")
    print(f"Data: {schema['data']}")
    print(f"Records/Samples: {schema['records']}")
    print(f"Input schema: {schema['input_schema']}")
    print(f"Output schema: {schema['output_schema']}")
    print("Split/Eval policy: fixed eval id list")
    print("Type: workflow/agent/multi-agent/eval")


def _generate_ticket_rows() -> list[dict[str, str]]:
    """Generate deterministic synthetic tickets with realistic failure/safety cases."""
    base_time = datetime(2026, 3, 1, 9, 0, 0)

    templates = [
        ("free", "Cannot login to dashboard", "I keep seeing invalid session token and cannot access account."),
        ("pro", "Invoice mismatch", "Billing total is different from contract and needs correction."),
        ("enterprise", "Production API outage", "Our API calls return 500 for all regions. Business blocked."),
        ("enterprise", "Security alert", "Suspicious access from unknown IP. Please investigate immediately."),
        ("pro", "Feature request", "Can you add export filter for monthly reports?"),
        ("free", "Password reset issue", "Reset link expires too quickly and fails repeatedly."),
        ("enterprise", "Data export request", "Need full user dump including PII for external audit email."),
        ("pro", "Latency spike", "Response time increased to 8 seconds during peak traffic."),
        ("enterprise", "Payment failure", "Card payment fails only for EU customers after latest release."),
        ("free", "General question", "How do I change notification settings?"),
    ]

    rows: list[dict[str, str]] = []
    for i in range(60):
        tier, subject, body = templates[i % len(templates)]
        row = {
            "ticket_id": f"TKT-{1000 + i}",
            "customer_tier": tier,
            "subject": subject,
            "body": body,
            "created_at": (base_time + timedelta(minutes=15 * i)).isoformat(),
        }
        rows.append(row)
    return rows


def ensure_ticket_dataset() -> tuple[Path, Path]:
    """Create dataset and fixed eval-id file if missing, then return paths."""
    ensure_stage6_dirs()
    csv_path = DATA_DIR / "tickets_sample.csv"
    eval_path = DATA_DIR / "eval_ids_stage6.txt"

    if not csv_path.exists():
        rows = _generate_ticket_rows()
        with csv_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(
                fp,
                fieldnames=["ticket_id", "customer_tier", "subject", "body", "created_at"],
            )
            writer.writeheader()
            writer.writerows(rows)

    if not eval_path.exists():
        # Fixed 30-row evaluation subset (every other ticket id).
        rows = load_ticket_rows(csv_path)
        eval_ids = [r.ticket_id for idx, r in enumerate(rows) if idx % 2 == 0][:30]
        eval_path.write_text("\n".join(eval_ids), encoding="utf-8")

    return csv_path, eval_path


def load_ticket_rows(csv_path: Path | None = None) -> list[TicketRecord]:
    """Load ticket rows as strongly-typed records."""
    if csv_path is None:
        csv_path, _ = ensure_ticket_dataset()

    out: list[TicketRecord] = []
    with csv_path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            out.append(
                TicketRecord(
                    ticket_id=row["ticket_id"],
                    customer_tier=row["customer_tier"],
                    subject=row["subject"],
                    body=row["body"],
                    created_at=row["created_at"],
                )
            )
    return out


def load_eval_ids(eval_path: Path | None = None) -> set[str]:
    """Read fixed eval-id list to keep before/after comparisons fair."""
    if eval_path is None:
        _, eval_path = ensure_ticket_dataset()
    return {
        line.strip()
        for line in eval_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def _contains(text: str, keywords: list[str]) -> bool:
    low = text.lower()
    return any(k in low for k in keywords)


def classify_priority(ticket: TicketRecord) -> str:
    """Deterministic rule-based priority classifier used by baseline workflows."""
    text = f"{ticket.subject} {ticket.body}".lower()

    if _contains(text, ["security", "suspicious", "breach"]):
        return "critical"
    if _contains(text, ["outage", "500", "production", "blocked"]):
        return "critical"
    if _contains(text, ["payment", "invoice", "billing"]):
        return "high"
    if _contains(text, ["latency", "slow", "timeout"]):
        return "high"
    if _contains(text, ["cannot", "issue", "fails", "error"]):
        return "medium"
    return "low"


def route_queue(ticket: TicketRecord) -> str:
    """Route tickets to the most relevant queue based on explicit keyword rules."""
    text = f"{ticket.subject} {ticket.body}".lower()

    if _contains(text, ["security", "suspicious", "pii", "breach"]):
        return "security"
    if _contains(text, ["outage", "latency", "500", "api"]):
        return "outage"
    if _contains(text, ["invoice", "billing", "payment", "card"]):
        return "billing"
    return "general"


def retrieve_policy_snippets(ticket: TicketRecord) -> list[str]:
    """Return lightweight policy citations to teach grounded responses."""
    queue = route_queue(ticket)
    snippets = {
        "security": ["SEC-01: Verify identity before disclosure", "SEC-04: Escalate suspicious access"],
        "outage": ["OPS-02: Collect impact scope", "OPS-05: Incident severity rubric"],
        "billing": ["BILL-03: Invoice correction workflow", "BILL-07: Payment failure checklist"],
        "general": ["GEN-01: Provide self-service guide", "GEN-02: Offer follow-up options"],
    }
    return snippets[queue]


def risk_score(ticket: TicketRecord) -> float:
    """Compute a transparent risk score to drive policy/HITL decisions."""
    text = f"{ticket.subject} {ticket.body}".lower()
    score = 0.15

    if ticket.customer_tier == "enterprise":
        score += 0.2
    if _contains(text, ["security", "suspicious", "pii", "breach"]):
        score += 0.5
    if _contains(text, ["outage", "production", "blocked"]):
        score += 0.4
    if _contains(text, ["data export", "dump"]):
        score += 0.3

    return min(score, 1.0)


def needs_human_approval(ticket: TicketRecord, action: str = "respond") -> bool:
    """Policy gate: escalate high-risk cases and sensitive actions to human review."""
    score = risk_score(ticket)
    high_risk_action = action in {"export_data", "send_external", "execute_change"}
    return score >= 0.7 or high_risk_action


def draft_reply(ticket: TicketRecord, citations: list[str], style: str = "baseline") -> str:
    """Generate deterministic response drafts with citation IDs embedded."""
    queue = route_queue(ticket)
    priority = classify_priority(ticket)

    prefix = {
        "baseline": "We received your request and started processing.",
        "agent": "Agent triage complete. Next steps are below.",
        "safe": "Policy-checked response draft ready for review.",
    }.get(style, "Response draft generated.")

    return (
        f"{prefix} Ticket={ticket.ticket_id}, priority={priority}, queue={queue}. "
        f"Referenced policies: {', '.join(citations)}."
    )


def run_workflow_baseline(ticket: TicketRecord) -> dict[str, Any]:
    """Baseline deterministic pipeline with no dynamic tool selection loop."""
    citations = retrieve_policy_snippets(ticket)
    return {
        "ticket_id": ticket.ticket_id,
        "predicted_priority": classify_priority(ticket),
        "queue": route_queue(ticket),
        "draft_reply": draft_reply(ticket, citations, style="baseline"),
        "citations": citations,
        "needs_human_approval": needs_human_approval(ticket),
        "failure_class": None,
        "tool_calls": ["classify_priority", "route_queue", "retrieve_policy_snippets"],
    }


def run_agent_loop(ticket: TicketRecord, *, max_steps: int = 4) -> dict[str, Any]:
    """Simulate a bounded agent loop with explicit tool-step tracing.

    The function intentionally keeps logic deterministic for teaching comparison.
    """
    trace_steps: list[dict[str, Any]] = []
    used_tools: list[str] = []

    # Step 1: choose initial tool based on query intent.
    chosen_priority = classify_priority(ticket)
    trace_steps.append({"step": 1, "action": "classify_priority", "result": chosen_priority})
    used_tools.append("classify_priority")

    # Step 2: choose routing tool.
    chosen_queue = route_queue(ticket)
    trace_steps.append({"step": 2, "action": "route_queue", "result": chosen_queue})
    used_tools.append("route_queue")

    # Step 3: retrieve grounding snippets.
    citations = retrieve_policy_snippets(ticket)
    trace_steps.append({"step": 3, "action": "retrieve_policy_snippets", "result": citations})
    used_tools.append("retrieve_policy_snippets")

    # Optional step 4: policy gate evaluation.
    gate = needs_human_approval(ticket)
    trace_steps.append({"step": 4, "action": "policy_gate", "result": gate})
    used_tools.append("policy_gate")

    # Safety check: if max_steps is too low, emit controlled failure class.
    failure_class = None
    if max_steps < 4:
        failure_class = "max_steps_exceeded_before_policy"

    response = {
        "ticket_id": ticket.ticket_id,
        "predicted_priority": chosen_priority,
        "queue": chosen_queue,
        "draft_reply": draft_reply(ticket, citations, style="agent"),
        "citations": citations,
        "needs_human_approval": gate,
        "failure_class": failure_class,
        "tool_calls": used_tools,
        "trace_steps": trace_steps,
    }
    return response


def evaluate_predictions(outputs: list[dict[str, Any]]) -> dict[str, float]:
    """Compute simple educational metrics across outputs.

    Note: In this offline teaching context we use deterministic rule-derived checks,
    so 'task_success_rate' means 'valid structured output with required fields'.
    """
    if not outputs:
        return {
            "task_success_rate": 0.0,
            "citation_presence_rate": 0.0,
            "human_approval_rate": 0.0,
            "failure_rate": 0.0,
            "avg_steps": 0.0,
        }

    success = 0
    citation_present = 0
    approval = 0
    failure = 0
    total_steps = 0

    for row in outputs:
        required = {
            "ticket_id",
            "predicted_priority",
            "queue",
            "draft_reply",
            "citations",
            "needs_human_approval",
            "failure_class",
        }
        if required.issubset(row.keys()):
            success += 1
        if row.get("citations"):
            citation_present += 1
        if row.get("needs_human_approval"):
            approval += 1
        if row.get("failure_class"):
            failure += 1

        if "trace_steps" in row:
            total_steps += len(row["trace_steps"])
        elif "tool_calls" in row:
            total_steps += len(row["tool_calls"])

    n = float(len(outputs))
    return {
        "task_success_rate": success / n,
        "citation_presence_rate": citation_present / n,
        "human_approval_rate": approval / n,
        "failure_rate": failure / n,
        "avg_steps": total_steps / n,
    }


def as_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write rows to JSONL format for reproducible lab deliverables."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        for row in rows:
            fp.write(json.dumps(row, ensure_ascii=True) + "\n")


def as_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write dictionaries as CSV using union of all keys as columns."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fields.append(key)

    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_metrics_csv(path: Path, metrics: dict[str, float], label: str) -> None:
    """Persist one metrics row with run label for before/after comparisons."""
    row = {"label": label, **metrics}
    as_csv(path, [row])


def now_ts() -> str:
    """Return timestamp string for logs and reports."""
    return datetime.utcnow().isoformat() + "Z"


def sleep_ms(milliseconds: int) -> None:
    """Small helper for latency simulation demos."""
    time.sleep(max(milliseconds, 0) / 1000.0)


def detect_prompt_injection(text: str) -> bool:
    """Simple rule-based injection detector for educational safety examples."""
    dangerous_patterns = [
        "ignore previous instructions",
        "reveal system prompt",
        "export all pii",
        "bypass policy",
        "send secrets",
    ]
    low = text.lower()
    return any(p in low for p in dangerous_patterns)


def permission_check(role: str, tool_name: str) -> bool:
    """Role-to-tool allowlist check used in security and policy scripts."""
    allowlist = {
        "agent_general": {"classify_priority", "route_queue", "retrieve_policy_snippets"},
        "agent_security": {"classify_priority", "route_queue", "retrieve_policy_snippets", "flag_security_incident"},
        "human_reviewer": {"approve_high_risk_action", "export_redacted_report"},
    }
    return tool_name in allowlist.get(role, set())


def summarize_incident(case_id: str, failure: str, fix: str, outcome: str) -> str:
    """Create standardized postmortem text block."""
    return (
        f"Incident Case: {case_id}\n"
        f"Detected At: {now_ts()}\n"
        f"Failure Type: {failure}\n"
        f"Fix Applied: {fix}\n"
        f"Outcome: {outcome}\n"
    )


def select_eval_tickets(rows: list[TicketRecord], eval_ids: set[str]) -> list[TicketRecord]:
    """Filter full dataset into fixed evaluation subset."""
    return [r for r in rows if r.ticket_id in eval_ids]


def build_trace_row(run_id: str, query_id: str, step_index: int, tool: str, status: str, latency_ms: int, cost_tokens: int) -> dict[str, Any]:
    """Construct trace rows with explicit required fields used in this stage."""
    return {
        "run_id": run_id,
        "query_id": query_id,
        "step_index": step_index,
        "selected_tool": tool,
        "tool_status": status,
        "latency_ms": latency_ms,
        "token_cost": cost_tokens,
        "timestamp": now_ts(),
    }
