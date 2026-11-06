"""Scaffold a new AI employee rollout folder from the bundled templates."""

import json
import re
from pathlib import Path

TEMPLATES = Path(__file__).parent / "templates"


def slugify(name):
    """Turn a business name into a filesystem-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "business"


def _template(filename):
    return (TEMPLATES / filename).read_text(encoding="utf-8")


def _fill(text, business_name):
    return text.replace("__BUSINESS_NAME__", business_name)


def _one_pager(business_name, lane):
    text = _template("one-pager.md")
    tools = lane.get("tools") or []
    approvals = lane.get("approval_required_for") or []
    replacements = {
        "__BUSINESS_NAME__": business_name,
        "__LANE_NAME__": lane.get("name", ""),
        "__OWNS__": lane.get("owns", ""),
        "__HUMAN_OWNER__": lane.get("human_owner", ""),
        "__TOOLS__": "\n".join(f"- {tool}" for tool in tools) or "- (none yet)",
        "__APPROVALS__": "\n".join(f"- {item}" for item in approvals)
        or "- Nothing may leave the business from this lane.",
    }
    for token, value in replacements.items():
        text = text.replace(token, value)
    return text


def init_rollout(business_name, base_dir=None):
    """Create ./<slug>-rollout/ for business_name and return its Path."""
    base = Path(base_dir) if base_dir is not None else Path.cwd()
    folder = base / f"{slugify(business_name)}-rollout"
    (folder / "memory").mkdir(parents=True, exist_ok=True)
    (folder / "one-pagers").mkdir(parents=True, exist_ok=True)

    data = json.loads(_fill(_template("rollout.json"), business_name))
    (folder / "rollout.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "governance.md").write_text(
        _fill(_template("governance.md"), business_name), encoding="utf-8"
    )
    (folder / "staff-guide.md").write_text(
        _fill(_template("staff-guide.md"), business_name), encoding="utf-8"
    )
    (folder / "checklist.md").write_text(
        _fill(_template("checklist.md"), business_name), encoding="utf-8"
    )
    (folder / "memory" / "MEMORY.md").write_text(
        _fill(_template("memory.md"), business_name), encoding="utf-8"
    )
    for lane in data.get("lanes", []):
        (folder / "one-pagers" / f"{lane['name']}.md").write_text(
            _one_pager(business_name, lane), encoding="utf-8"
        )
    return folder


def list_files(folder):
    """All files inside a rollout folder, as sorted relative paths."""
    folder = Path(folder)
    return sorted(
        str(path.relative_to(folder)) for path in folder.rglob("*") if path.is_file()
    )
