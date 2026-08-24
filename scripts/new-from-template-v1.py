#!/usr/bin/env python3
"""Clone Template V1 into src/<slug>/. Does not copy STT/LLM/TTS — imports locked stack."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "amina" / "template_v1"
LOCKED = {"agent.py"}  # rewritten, still imports build_session


def _slug(s: str) -> str:
    out = re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")
    if not out or not re.match(r"^[a-z][a-z0-9_]*$", out):
        raise SystemExit("slug must be a Python package: firma_x")
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True, help="package folder, e.g. firma-x")
    p.add_argument("--agent-name", required=True, help="LiveKit dispatch name")
    p.add_argument("--persona", default="")
    p.add_argument("--company", default="")
    p.add_argument("--product", default="")
    p.add_argument("--display-name", default="")
    args = p.parse_args()
    slug = _slug(args.slug)
    dest = ROOT / "src" / slug
    if dest.exists():
        raise SystemExit(f"exists: {dest}")
    shutil.copytree(SRC, dest)
    toml = dest / "project.toml"
    text = toml.read_text()
    repl = {
        "agent_name": args.agent_name,
        "display_name": args.display_name or args.agent_name,
    }
    if args.persona:
        repl["persona_name"] = args.persona
    if args.company:
        repl["company"] = args.company
    if args.product:
        repl["product"] = args.product
    for key, val in repl.items():
        text = re.sub(
            rf'^({key}\s*=\s*)".*"$',
            rf'\1"{val}"',
            text,
            flags=re.MULTILINE,
        )
    toml.write_text(text)
    agent = dest / "agent.py"
    agent.write_text(
        agent.read_text()
        .replace("from amina.template_v1.prompts", f"from {slug.replace('-', '_')}.prompts")
        .replace("class TemplateV1Agent", f"class {_cls(slug)}Agent")
        .replace("TemplateV1Agent()", f"{_cls(slug)}Agent()")
        .replace("template_v1_entry", f"{slug.replace('-', '_')}_entry")
    )
    # hyphen slugs cannot be import packages — require underscore
    if "-" in slug:
        print("warning: slug has hyphen; rename to underscore for Python import", file=sys.stderr)
    print(dest)


def _cls(slug: str) -> str:
    return "".join(p.title() for p in slug.replace("-", "_").split("_"))


if __name__ == "__main__":
    main()
