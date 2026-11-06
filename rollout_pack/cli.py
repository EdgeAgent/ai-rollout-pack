"""Command line interface for the AI Rollout Pack.

Subcommands:
  init <business-name>   scaffold a rollout folder
  check <folder>         lint a rollout folder against the governance rules
  map <folder>           print a Mermaid workflow map (and write workflow-map.md)
  demo                   init + check + map on a fictional business, end to end
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

from . import __version__
from .checker import all_passed, check_rollout, format_results
from .mapping import build_mermaid, write_map
from .scaffold import init_rollout, list_files

DEMO_BUSINESS = "Demo Dental Co"


def _load_rollout(folder):
    path = Path(folder) / "rollout.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _cmd_init(args):
    folder = init_rollout(args.business_name)
    print(f"Created rollout for '{args.business_name}': {folder}")
    for name in list_files(folder):
        print(f"  {name}")
    print("\nNext: fill in the one-pager and memory, then run:")
    print(f"  rollout-pack check {folder}")
    return 0


def _cmd_check(args):
    results = check_rollout(args.folder)
    print(format_results(results))
    if all_passed(results):
        print(f"\nAll 7 governance rules pass for {args.folder}.")
        return 0
    print(f"\nGovernance check FAILED for {args.folder}. Fix the FAIL lines before go-live.")
    return 1


def _cmd_map(args):
    folder = Path(args.folder)
    data = _load_rollout(folder)
    print(build_mermaid(data))
    written = write_map(folder, data)
    print(f"\nWrote {written}", file=sys.stderr)
    return 0


def _cmd_demo(args):
    print(f"=== demo: AI Rollout Pack {__version__} ===")
    with tempfile.TemporaryDirectory() as tmp:
        print(f"\n--- rollout-pack init '{DEMO_BUSINESS}' ---")
        folder = init_rollout(DEMO_BUSINESS, base_dir=tmp)
        for name in list_files(folder):
            print(f"  {name}")

        print("\n--- rollout-pack check ---")
        results = check_rollout(folder)
        print(format_results(results))
        if not all_passed(results):
            print("\nDemo FAILED: a fresh rollout should pass every rule.")
            return 1

        print("\n--- rollout-pack map ---")
        data = _load_rollout(folder)
        print(build_mermaid(data))
        write_map(folder, data)

    print("\nDemo complete: init -> check (all PASS) -> map.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="rollout-pack",
        description="Scaffold and lint an AI employee rollout for a small business.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="scaffold a rollout folder")
    p_init.add_argument("business_name", help="name of the business, e.g. 'Acme Dental'")
    p_init.set_defaults(func=_cmd_init)

    p_check = sub.add_parser("check", help="lint a rollout folder (exit 1 on any FAIL)")
    p_check.add_argument("folder", help="path to the rollout folder")
    p_check.set_defaults(func=_cmd_check)

    p_map = sub.add_parser("map", help="print a Mermaid workflow map for a rollout")
    p_map.add_argument("folder", help="path to the rollout folder")
    p_map.set_defaults(func=_cmd_map)

    p_demo = sub.add_parser("demo", help="run init + check + map on a fictional business")
    p_demo.set_defaults(func=_cmd_demo)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
