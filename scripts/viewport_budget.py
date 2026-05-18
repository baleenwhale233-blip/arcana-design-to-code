#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Viewport:
    width: float
    height: float


@dataclass(frozen=True)
class NamedSize:
    name: str
    value: float


def parse_viewport(value: str) -> Viewport:
    parts = value.lower().replace(" ", "").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("viewport must be WIDTHxHEIGHT, for example 390x844")
    try:
        width = float(parts[0])
        height = float(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("viewport values must be numbers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("viewport values must be positive")
    return Viewport(width=width, height=height)


def parse_named_size(value: str) -> NamedSize:
    if ":" not in value:
        raise argparse.ArgumentTypeError("value must be name:px, for example header:48")
    name, raw = value.split(":", 1)
    name = name.strip()
    if not name:
        raise argparse.ArgumentTypeError("name must not be empty")
    try:
        parsed = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("size must be a number") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("size must not be negative")
    return NamedSize(name=name, value=parsed)


def rounded(value: float) -> float | int:
    rounded_value = round(value, 2)
    return int(rounded_value) if rounded_value == int(rounded_value) else rounded_value


def build_report(args: argparse.Namespace) -> dict:
    reserve_total = sum(item.value for item in args.reserve)
    item_total = sum(item.value for item in args.item)
    gap_total = sum(item.value for item in args.gap)
    available = args.viewport.height - reserve_total
    planned = item_total + gap_total
    remaining = available - planned

    return {
        "viewport": {"width": rounded(args.viewport.width), "height": rounded(args.viewport.height)},
        "scroll_policy": args.scroll_policy,
        "reserved_height": rounded(reserve_total),
        "available_height": rounded(available),
        "sections": [{"name": item.name, "height": rounded(item.value)} for item in args.item],
        "gaps": [{"name": item.name, "height": rounded(item.value)} for item in args.gap],
        "section_total": rounded(item_total),
        "gap_total": rounded(gap_total),
        "planned_height": rounded(planned),
        "remaining_height": rounded(remaining),
        "status": "pass" if remaining >= 0 else "overflow",
        "notes": (
            "No-scroll screens should pass without relying on page scroll."
            if args.scroll_policy == "no-scroll"
            else "Scroll is allowed by policy; still avoid accidental overflow from hidden min-heights."
        ),
    }


def render_markdown(report: dict) -> str:
    lines = [
        "## Viewport Budget",
        "",
        f"- target viewport: {report['viewport']['width']}x{report['viewport']['height']}",
        f"- scroll policy: {report['scroll_policy']}",
        f"- reserved shell/safe height: {report['reserved_height']}px",
        f"- available height: {report['available_height']}px",
        "",
        "| section | height |",
        "|---|---:|",
    ]
    for item in report["sections"]:
        lines.append(f"| {item['name']} | {item['height']}px |")

    if report["gaps"]:
        lines.extend(["", "| gap/padding | height |", "|---|---:|"])
        for item in report["gaps"]:
            lines.append(f"| {item['name']} | {item['height']}px |")

    lines.extend(
        [
            "",
            f"- section total: {report['section_total']}px",
            f"- gap total: {report['gap_total']}px",
            f"- total planned height: {report['planned_height']}px",
            f"- remaining/overflow: {report['remaining_height']}px",
            f"- status: {report['status']}",
            f"- notes: {report['notes']}",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check CSS viewport height budget for constrained UI layouts.")
    parser.add_argument("--viewport", required=True, type=parse_viewport, help="Target viewport, for example 390x844.")
    parser.add_argument("--scroll-policy", choices=("no-scroll", "content-scroll", "panel-scroll"), default="no-scroll")
    parser.add_argument("--reserve", type=parse_named_size, action="append", default=[], help="Reserved shell/safe/chrome height: name:px.")
    parser.add_argument("--item", type=parse_named_size, action="append", default=[], help="Section height: name:px.")
    parser.add_argument("--gap", type=parse_named_size, action="append", default=[], help="Gap, margin, or padding height: name:px.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write output to a file instead of stdout.")

    args = parser.parse_args()
    report = build_report(args)
    output = json.dumps(report, indent=2, ensure_ascii=False) if args.format == "json" else render_markdown(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
