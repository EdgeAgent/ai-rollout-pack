"""Governance linter for a rollout folder.

Seven rules (R1-R7). A rollout should not go live unless every rule passes.
The checker only reads files; it never modifies the rollout.
"""

import json
from dataclasses import dataclass
from pathlib import Path

WRITE_ACTIONS = ("send", "publish", "pay")


@dataclass
class RuleResult:
    rule: str
    passed: bool
    reason: str


def _load(folder):
    """Return (data, error) for rollout.json inside folder."""
    path = folder / "rollout.json"
    if not path.exists():
        return None, "rollout.json is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, "rollout.json does not parse as JSON"
    if not isinstance(data, dict):
        return None, "rollout.json is not a JSON object"
    return data, None


def _lanes(data):
    lanes = data.get("lanes") if data else None
    return lanes if isinstance(lanes, list) else []


def check_rollout(folder):
    """Run all seven governance rules against folder. Returns [RuleResult]."""
    folder = Path(folder)
    results = []
    data, error = _load(folder)
    lanes = _lanes(data)

    # R1 — rollout.json exists, parses, names the business.
    if error:
        results.append(RuleResult("R1", False, error))
    elif not str(data.get("business", "")).strip():
        results.append(RuleResult("R1", False, "business name is empty"))
    else:
        results.append(
            RuleResult("R1", True, f"rollout.json names '{data['business']}'")
        )

    # R2 — at least one lane; every lane fully described.
    if error:
        results.append(RuleResult("R2", False, "rollout.json unavailable (see R1)"))
    elif not lanes:
        results.append(RuleResult("R2", False, "no lanes defined"))
    else:
        incomplete = [
            lane.get("name", "?")
            for lane in lanes
            if not (
                str(lane.get("name", "")).strip()
                and str(lane.get("owns", "")).strip()
                and str(lane.get("human_owner", "")).strip()
            )
        ]
        if incomplete:
            results.append(
                RuleResult(
                    "R2",
                    False,
                    "lane(s) missing name, owns, or human_owner: "
                    + ", ".join(incomplete),
                )
            )
        else:
            results.append(
                RuleResult("R2", True, f"{len(lanes)} lane(s), each with an owner")
            )

    # R3 — every lane is read-only or has approval gates.
    if error:
        results.append(RuleResult("R3", False, "rollout.json unavailable (see R1)"))
    else:
        ungated = [
            lane.get("name", "?")
            for lane in lanes
            if lane.get("read_only") is not True
            and not lane.get("approval_required_for")
        ]
        if ungated:
            results.append(
                RuleResult(
                    "R3",
                    False,
                    "lane(s) can act but require no approval: " + ", ".join(ungated),
                )
            )
        else:
            results.append(
                RuleResult("R3", True, "every lane is read-only or approval-gated")
            )

    # R4 — write actions (send/publish/pay) must themselves be gated.
    if error:
        results.append(RuleResult("R4", False, "rollout.json unavailable (see R1)"))
    else:
        problems = []
        for lane in lanes:
            tools = lane.get("tools") or []
            approvals = lane.get("approval_required_for") or []
            for action in WRITE_ACTIONS:
                if action in tools and action not in approvals:
                    problems.append(f"{lane.get('name', '?')}: '{action}' ungated")
        if problems:
            results.append(RuleResult("R4", False, "; ".join(problems)))
        else:
            results.append(
                RuleResult("R4", True, "every send/publish/pay tool is gated")
            )

    # R5 — the memory file exists and is non-empty.
    memory = folder / "memory" / "MEMORY.md"
    if not memory.exists():
        results.append(RuleResult("R5", False, "memory/MEMORY.md is missing"))
    elif not memory.read_text(encoding="utf-8").strip():
        results.append(RuleResult("R5", False, "memory/MEMORY.md is empty"))
    else:
        results.append(RuleResult("R5", True, "memory/MEMORY.md exists and is written"))

    # R6 — governance names the kill switch and the scrub rule.
    governance = folder / "governance.md"
    if not governance.exists():
        results.append(RuleResult("R6", False, "governance.md is missing"))
    else:
        text = governance.read_text(encoding="utf-8").lower()
        missing = []
        if "kill switch" not in text:
            missing.append("'kill switch'")
        if "do-not-contact" not in text and "scrub" not in text:
            missing.append("'do-not-contact' or 'scrub'")
        if missing:
            results.append(
                RuleResult("R6", False, "governance.md is missing: " + ", ".join(missing))
            )
        else:
            results.append(
                RuleResult("R6", True, "governance names the kill switch and scrub rule")
            )

    # R7 — every lane has its one-pager.
    if error:
        results.append(RuleResult("R7", False, "rollout.json unavailable (see R1)"))
    else:
        missing = [
            lane.get("name", "?")
            for lane in lanes
            if not (folder / "one-pagers" / f"{lane.get('name', '')}.md").exists()
        ]
        if missing:
            results.append(
                RuleResult("R7", False, "missing one-pager(s): " + ", ".join(missing))
            )
        else:
            results.append(RuleResult("R7", True, "every lane has a one-pager"))

    return results


def all_passed(results):
    return all(result.passed for result in results)


def format_results(results):
    lines = []
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"{result.rule} {status} - {result.reason}")
    return "\n".join(lines)
