"""Tests for the AI Rollout Pack: scaffold, checker, map, and CLI demo."""

import json
from pathlib import Path

import pytest

from rollout_pack.checker import check_rollout
from rollout_pack.cli import main
from rollout_pack.mapping import build_mermaid
from rollout_pack.scaffold import init_rollout, slugify

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = REPO_ROOT / "examples" / "maple-street-dental"


@pytest.fixture()
def fresh(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return init_rollout("Acme Dental")


def _results_by_rule(folder):
    return {result.rule: result for result in check_rollout(folder)}


def _edit_rollout(folder, mutate):
    path = folder / "rollout.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


# --- scaffold ------------------------------------------------------------


def test_init_creates_rollout_json(fresh):
    assert (fresh / "rollout.json").exists()


def test_init_creates_governance(fresh):
    assert (fresh / "governance.md").exists()


def test_init_creates_staff_guide_and_checklist(fresh):
    assert (fresh / "staff-guide.md").exists()
    assert (fresh / "checklist.md").exists()


def test_init_creates_memory_file(fresh):
    memory = fresh / "memory" / "MEMORY.md"
    assert memory.exists()
    assert memory.read_text(encoding="utf-8").strip()


def test_init_creates_starter_one_pager(fresh):
    assert (fresh / "one-pagers" / "front-desk.md").exists()


def test_init_substitutes_business_name(fresh):
    data = json.loads((fresh / "rollout.json").read_text(encoding="utf-8"))
    assert data["business"] == "Acme Dental"
    assert "Acme Dental" in (fresh / "governance.md").read_text(encoding="utf-8")


def test_slugify():
    assert slugify("Acme Dental Care!") == "acme-dental-care"
    assert slugify("  Bob's  Shop ") == "bob-s-shop"


# --- checker: happy path ---------------------------------------------------


def test_check_passes_on_fresh_init(fresh):
    results = check_rollout(fresh)
    assert all(result.passed for result in results)
    assert main(["check", str(fresh)]) == 0


def test_check_passes_on_bundled_example():
    results = check_rollout(EXAMPLE)
    assert all(result.passed for result in results), [
        (r.rule, r.reason) for r in results if not r.passed
    ]


# --- checker: targeted failures --------------------------------------------


def test_check_fails_r3_when_lane_acts_without_approvals(fresh):
    _edit_rollout(fresh, lambda d: d["lanes"][0].update(approval_required_for=[]))
    results = _results_by_rule(fresh)
    assert not results["R3"].passed
    assert main(["check", str(fresh)]) == 1


def test_check_fails_r4_when_send_is_not_gated(fresh):
    def mutate(data):
        data["lanes"][0]["approval_required_for"] = ["publish"]

    _edit_rollout(fresh, mutate)
    results = _results_by_rule(fresh)
    assert not results["R4"].passed


def test_check_fails_r5_when_memory_missing(fresh):
    (fresh / "memory" / "MEMORY.md").unlink()
    results = _results_by_rule(fresh)
    assert not results["R5"].passed


def test_check_fails_r6_when_governance_loses_kill_switch(fresh):
    path = fresh / "governance.md"
    text = path.read_text(encoding="utf-8").replace("kill switch", "stop button")
    text = text.replace("Kill switch", "Stop button").replace("Kill Switch", "Stop Button")
    path.write_text(text, encoding="utf-8")
    results = _results_by_rule(fresh)
    assert not results["R6"].passed


def test_check_fails_r7_when_one_pager_missing(fresh):
    (fresh / "one-pagers" / "front-desk.md").unlink()
    results = _results_by_rule(fresh)
    assert not results["R7"].passed


def test_check_fails_r1_when_business_name_empty(fresh):
    _edit_rollout(fresh, lambda d: d.update(business=""))
    results = _results_by_rule(fresh)
    assert not results["R1"].passed


def test_check_fails_r2_when_lane_has_no_owner(fresh):
    _edit_rollout(fresh, lambda d: d["lanes"][0].update(human_owner=""))
    results = _results_by_rule(fresh)
    assert not results["R2"].passed


# --- map -------------------------------------------------------------------


def test_map_contains_lane_names_and_live_node(fresh):
    data = json.loads((fresh / "rollout.json").read_text(encoding="utf-8"))
    mermaid = build_mermaid(data)
    assert "front-desk" in mermaid
    assert "Acme Dental" in mermaid
    assert '"Live"' in mermaid


def test_map_has_gate_for_gated_action(fresh):
    data = json.loads((fresh / "rollout.json").read_text(encoding="utf-8"))
    mermaid = build_mermaid(data)
    assert "Approval gate: send" in mermaid


def test_map_command_writes_workflow_map(fresh, capsys):
    assert main(["map", str(fresh)]) == 0
    written = fresh / "workflow-map.md"
    assert written.exists()
    assert "front-desk" in written.read_text(encoding="utf-8")
    assert "front-desk" in capsys.readouterr().out


def test_example_map_has_all_three_lanes_and_one_gate():
    data = json.loads((EXAMPLE / "rollout.json").read_text(encoding="utf-8"))
    mermaid = build_mermaid(data)
    for lane in ("front-desk", "faq", "billing-watch"):
        assert lane in mermaid
    assert mermaid.count("Approval gate:") == 1


# --- demo ------------------------------------------------------------------


def test_demo_exits_clean(capsys):
    assert main(["demo"]) == 0
    out = capsys.readouterr().out
    assert "PASS" in out
    assert "Demo complete" in out
