#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - exercised in environments without Pillow
    raise SystemExit("Pillow is required. Install it with: python3 -m pip install Pillow") from exc


@dataclass(frozen=True)
class Viewport:
    width: float
    height: float


@dataclass(frozen=True)
class NamedViewport:
    name: str
    viewport: Viewport


@dataclass(frozen=True)
class Rect:
    name: str
    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class Point:
    name: str
    x: float
    y: float


@dataclass(frozen=True)
class Distance:
    name: str
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True)
class TextBox:
    name: str
    x: float
    y: float
    width: float
    height: float
    lines: int


@dataclass(frozen=True)
class ManualValue:
    name: str
    value: float


@dataclass(frozen=True)
class Scale:
    x: float
    y: float

    @property
    def uniform(self) -> float:
        return (self.x + self.y) / 2

    @property
    def is_uniform(self) -> bool:
        return math.isclose(self.x, self.y, rel_tol=0.01, abs_tol=0.01)


def parse_viewport(value: str) -> Viewport:
    parts = value.lower().replace(" ", "").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("viewport must be WIDTHxHEIGHT, for example 390x844")
    try:
        width, height = float(parts[0]), float(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("viewport values must be numbers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("viewport values must be positive")
    return Viewport(width=width, height=height)


def parse_named_viewport(value: str) -> NamedViewport:
    if ":" in value:
        name, raw = value.split(":", 1)
        name = name.strip()
        if not name:
            raise argparse.ArgumentTypeError("target viewport name must not be empty")
    else:
        name = value
        raw = value
    viewport = parse_viewport(raw)
    return NamedViewport(name=name, viewport=viewport)


def parse_rect(value: str) -> Rect:
    name, raw = split_name_value(value, "rect")
    nums = parse_numbers(raw, 4, "rect must be name:x,y,w,h")
    x, y, width, height = nums
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("rect width and height must be positive")
    return Rect(name=name, x=x, y=y, width=width, height=height)


def parse_point(value: str) -> Point:
    name, raw = split_name_value(value, "point")
    x, y = parse_numbers(raw, 2, "point must be name:x,y")
    return Point(name=name, x=x, y=y)


def parse_distance(value: str) -> Distance:
    name, raw = split_name_value(value, "distance")
    x1, y1, x2, y2 = parse_numbers(raw, 4, "distance must be name:x1,y1,x2,y2")
    return Distance(name=name, x1=x1, y1=y1, x2=x2, y2=y2)


def parse_text_box(value: str) -> TextBox:
    name, raw = split_name_value(value, "text")
    nums = parse_numbers(raw, 4, "text must be name:x,y,w,h or name:x,y,w,h,lines", allow_extra_one=True)
    lines = int(nums[4]) if len(nums) == 5 else 1
    if lines <= 0:
        raise argparse.ArgumentTypeError("text line count must be positive")
    x, y, width, height = nums[:4]
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("text width and height must be positive")
    return TextBox(name=name, x=x, y=y, width=width, height=height, lines=lines)


def parse_manual_value(value: str) -> ManualValue:
    name, raw = split_name_value(value, "value")
    try:
        parsed = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("manual value must be name:number") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("manual value must not be negative")
    return ManualValue(name=name, value=parsed)


def split_name_value(value: str, label: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError(f"{label} must include a name, for example name:1,2")
    name, raw = value.split(":", 1)
    name = name.strip()
    if not name:
        raise argparse.ArgumentTypeError(f"{label} name must not be empty")
    return name, raw


def parse_numbers(value: str, count: int, message: str, allow_extra_one: bool = False) -> list[float]:
    parts = [part.strip() for part in value.split(",")]
    valid_counts = {count, count + 1} if allow_extra_one else {count}
    if len(parts) not in valid_counts:
        raise argparse.ArgumentTypeError(message)
    try:
        return [float(part) for part in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(message) from exc


def css_x(value: float, scale: Scale) -> float:
    return value / scale.x


def css_y(value: float, scale: Scale) -> float:
    return value / scale.y


def css_len(value: float, scale: Scale) -> float:
    return value / scale.uniform


def rounded(value: float) -> float | int:
    rounded_value = round(value, 2)
    if math.isclose(rounded_value, round(rounded_value), abs_tol=0.001):
        return int(round(rounded_value))
    return rounded_value


def clamp_box(x: float, y: float, width: float, height: float, image_width: int, image_height: int) -> tuple[int, int, int, int]:
    left = max(0, min(image_width, int(math.floor(x))))
    top = max(0, min(image_height, int(math.floor(y))))
    right = max(left + 1, min(image_width, int(math.ceil(x + width))))
    bottom = max(top + 1, min(image_height, int(math.ceil(y + height))))
    return left, top, right, bottom


def average_color(img: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    crop = img.crop(box).convert("RGBA")
    raw_pixels = crop.get_flattened_data() if hasattr(crop, "get_flattened_data") else crop.getdata()
    pixels = list(raw_pixels)
    count = len(pixels)
    return tuple(round(sum(pixel[channel] for pixel in pixels) / count) for channel in range(4))  # type: ignore[return-value]


def color_to_hex(color: tuple[int, int, int, int]) -> str:
    r, g, b, _ = color
    return f"#{r:02x}{g:02x}{b:02x}"


def color_distance(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    return math.sqrt(sum((a[index] - b[index]) ** 2 for index in range(3)))


def estimate_radius(img: Image.Image, rect: Rect) -> dict[str, Any]:
    rgba = img.convert("RGBA")
    left, top, right, bottom = clamp_box(rect.x, rect.y, rect.width, rect.height, rgba.width, rgba.height)
    crop = rgba.crop((left, top, right, bottom))
    width, height = crop.size

    if width < 6 or height < 6:
        return {"image_px": None, "confidence": "unknown", "notes": "box is too small for radius probing"}

    center_box = (
        max(0, int(width * 0.4)),
        max(0, int(height * 0.4)),
        min(width, int(width * 0.6) + 1),
        min(height, int(height * 0.6) + 1),
    )
    fill = average_color(crop, center_box)
    corner_colors = [
        crop.getpixel((0, 0)),
        crop.getpixel((width - 1, 0)),
        crop.getpixel((0, height - 1)),
        crop.getpixel((width - 1, height - 1)),
    ]
    background_delta = median(color_distance(fill, color) for color in corner_colors)
    max_probe = max(1, min(width, height) // 2)
    threshold = max(8, min(36, background_delta * 0.55))

    def is_fill(pixel: tuple[int, int, int, int]) -> bool:
        return pixel[3] > 8 and color_distance(pixel, fill) <= threshold

    pixels = crop.load()
    probes: list[int] = []

    for x in range(max_probe):
        if is_fill(pixels[x, 0]):
            probes.append(x)
            break

    for y in range(max_probe):
        if is_fill(pixels[0, y]):
            probes.append(y)
            break

    for x in range(width - 1, width - max_probe - 1, -1):
        if is_fill(pixels[x, 0]):
            probes.append(width - 1 - x)
            break

    for y in range(max_probe):
        if is_fill(pixels[width - 1, y]):
            probes.append(y)
            break

    if not probes:
        return {
            "image_px": None,
            "confidence": "unknown",
            "notes": "could not find a rounded corner transition; use --manual-radius",
        }

    return {
        "image_px": rounded(median(probes)),
        "confidence": "estimated",
        "notes": "probed top corners against center fill; shadows/borders can affect this",
    }


def estimate_text(text: TextBox, scale: Scale) -> dict[str, Any]:
    line_box = css_y(text.height, scale) / text.lines
    line_height = nearest(line_box, [14, 16, 18, 20, 22, 24, 28, 32, 36, 40, 44])
    font_size = nearest(line_height / 1.22, [10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32])
    return {
        "name": text.name,
        "box_css": {
            "x": rounded(css_x(text.x, scale)),
            "y": rounded(css_y(text.y, scale)),
            "width": rounded(css_x(text.width, scale)),
            "height": rounded(css_y(text.height, scale)),
        },
        "lines": text.lines,
        "estimated_size_px": font_size,
        "estimated_line_height_px": line_height,
        "confidence": "estimated",
        "notes": "estimated from text bounding-box height; verify against source design when exact typography matters",
    }


def nearest(value: float, candidates: list[int]) -> int:
    return min(candidates, key=lambda candidate: abs(candidate - value))


def common_tokens(values: list[float], candidates: list[int], limit: int = 12) -> list[int]:
    snapped = [nearest(value, candidates) for value in values if value > 0]
    result: list[int] = []
    for value in snapped:
        if value not in result:
            result.append(value)
    return result[:limit]


def add_token_candidate(values: list[float], value: float, max_value: int = 128) -> None:
    if 0 < value <= max_value:
        values.append(value)


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def adapt_value(value: int, factor: float, candidates: list[int]) -> int:
    return nearest(value * factor, candidates)


def unique(values: list[int]) -> list[int]:
    result: list[int] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def build_adaptations(source_viewport: Viewport, targets: list[NamedViewport], tokens: dict[str, list[int]]) -> list[dict[str, Any]]:
    adaptations = []
    spacing_candidates = [2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64]
    radius_candidates = [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]
    type_candidates = [10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 36]

    for target in targets:
        width_ratio = target.viewport.width / source_viewport.width
        spacing_factor = clamp(width_ratio**0.35, 0.88, 1.22)
        radius_factor = clamp(width_ratio**0.18, 0.95, 1.12)
        type_factor = clamp(width_ratio**0.22, 0.95, 1.14)
        page_padding_min = 16 if target.viewport.width < 768 else 24
        page_padding_max = 24 if target.viewport.width < 768 else 40

        adaptations.append(
            {
                "name": target.name,
                "viewport_css_px": {
                    "width": rounded(target.viewport.width),
                    "height": rounded(target.viewport.height),
                },
                "scale_strategy": {
                    "spacing_factor": rounded(spacing_factor),
                    "radius_factor": rounded(radius_factor),
                    "typography_factor": rounded(type_factor),
                    "notes": "gentle token scaling, not proportional screenshot scaling",
                },
                "tokens": {
                    "spacing_px": unique([adapt_value(value, spacing_factor, spacing_candidates) for value in tokens["spacing_px"]]),
                    "radius_px": unique([adapt_value(value, radius_factor, radius_candidates) for value in tokens["radius_px"]]),
                    "typography_px": unique([adapt_value(value, type_factor, type_candidates) for value in tokens["typography_px"]]),
                },
                "layout_guidance": {
                    "page_padding": f"clamp({page_padding_min}px, 4vw, {page_padding_max}px)",
                    "content_width": "use fluid width with max-width; do not lock to the reference screenshot width",
                },
            }
        )

    return adaptations


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    img = Image.open(args.image).convert("RGBA")
    source_viewport = args.source_viewport or args.viewport or Viewport(width=img.width, height=img.height)
    scale = Scale(x=img.width / source_viewport.width, y=img.height / source_viewport.height)

    rects = []
    spacing_candidates: list[float] = []
    radius_candidates: list[float] = []

    for rect in args.rect:
        rects.append(
            {
                "name": rect.name,
                "image_px": {
                    "x": rounded(rect.x),
                    "y": rounded(rect.y),
                    "width": rounded(rect.width),
                    "height": rounded(rect.height),
                },
                "css_px": {
                    "x": rounded(css_x(rect.x, scale)),
                    "y": rounded(css_y(rect.y, scale)),
                    "width": rounded(css_x(rect.width, scale)),
                    "height": rounded(css_y(rect.height, scale)),
                },
                "confidence": "measured",
            }
        )
        add_token_candidate(spacing_candidates, css_x(rect.x, scale), max_value=96)
        add_token_candidate(spacing_candidates, css_y(rect.y, scale), max_value=96)
        add_token_candidate(spacing_candidates, css_x(rect.width, scale), max_value=128)
        add_token_candidate(spacing_candidates, css_y(rect.height, scale), max_value=128)

    distances = []
    for distance in args.distance:
        dx = abs(distance.x2 - distance.x1)
        dy = abs(distance.y2 - distance.y1)
        diagonal = math.hypot(dx, dy)
        distances.append(
            {
                "name": distance.name,
                "image_px": {
                    "dx": rounded(dx),
                    "dy": rounded(dy),
                    "distance": rounded(diagonal),
                },
                "css_px": {
                    "dx": rounded(css_x(dx, scale)),
                    "dy": rounded(css_y(dy, scale)),
                    "distance": rounded(css_len(diagonal, scale)),
                },
                "confidence": "measured",
            }
        )
        add_token_candidate(spacing_candidates, css_x(dx, scale), max_value=128)
        add_token_candidate(spacing_candidates, css_y(dy, scale), max_value=128)
        add_token_candidate(spacing_candidates, css_len(diagonal, scale), max_value=128)

    colors = []
    for point in args.sample:
        box = clamp_box(point.x, point.y, 1, 1, img.width, img.height)
        color = average_color(img, box)
        colors.append(
            {
                "name": point.name,
                "point_css": {"x": rounded(css_x(point.x, scale)), "y": rounded(css_y(point.y, scale))},
                "hex": color_to_hex(color),
                "rgba": color,
                "confidence": "measured",
            }
        )

    for rect in args.sample_box:
        box = clamp_box(rect.x, rect.y, rect.width, rect.height, img.width, img.height)
        color = average_color(img, box)
        colors.append(
            {
                "name": rect.name,
                "box_css": {
                    "x": rounded(css_x(rect.x, scale)),
                    "y": rounded(css_y(rect.y, scale)),
                    "width": rounded(css_x(rect.width, scale)),
                    "height": rounded(css_y(rect.height, scale)),
                },
                "hex": color_to_hex(color),
                "rgba": color,
                "confidence": "measured",
            }
        )

    radii = []
    for rect in args.radius_probe:
        radius = estimate_radius(img, rect)
        css_value = None if radius["image_px"] is None else rounded(css_len(float(radius["image_px"]), scale))
        if css_value is not None:
            radius_candidates.append(float(css_value))
        radii.append(
            {
                "name": rect.name,
                "css_px": css_value,
                "image_px": radius["image_px"],
                "confidence": radius["confidence"],
                "notes": radius["notes"],
            }
        )

    for radius in args.manual_radius:
        css_value = rounded(css_len(radius.value, scale))
        radius_candidates.append(float(css_value))
        radii.append(
            {
                "name": radius.name,
                "css_px": css_value,
                "image_px": rounded(radius.value),
                "confidence": "measured",
                "notes": "manual image-pixel radius converted using viewport scale",
            }
        )

    text = [estimate_text(text_box, scale) for text_box in args.text]

    tokens = {
        "spacing_px": common_tokens(spacing_candidates, [2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64]),
        "radius_px": common_tokens(radius_candidates, [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]),
        "typography_px": common_tokens(
            [item["estimated_size_px"] for item in text],
            [10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32],
        ),
    }

    return {
        "source_image": str(args.image),
        "calibration": {
            "image_px": {"width": img.width, "height": img.height},
            "source_viewport_css_px": {"width": rounded(source_viewport.width), "height": rounded(source_viewport.height)},
            "scale": {
                "x_image_px_per_css_px": rounded(scale.x),
                "y_image_px_per_css_px": rounded(scale.y),
                "uniform": scale.is_uniform,
            },
            "accuracy_notes": "Values are measured in the reference design coordinate system. Adaptation targets use token scaling, not screenshot proportional scaling.",
        },
        "rects": rects,
        "distances": distances,
        "colors": colors,
        "radii": radii,
        "typography": text,
        "tokens_to_consider": tokens,
        "adaptations": build_adaptations(source_viewport, args.target_viewport, tokens),
    }


def render_markdown(report: dict[str, Any]) -> str:
    calibration = report["calibration"]
    lines = [
        "## Design Measurements",
        "",
        "### Calibration",
        f"- source image: `{report['source_image']}`",
        f"- image pixels: {calibration['image_px']['width']}x{calibration['image_px']['height']}",
        f"- source viewport: {calibration['source_viewport_css_px']['width']}x{calibration['source_viewport_css_px']['height']} CSS px",
        (
            "- scale: "
            f"{calibration['scale']['x_image_px_per_css_px']}x / "
            f"{calibration['scale']['y_image_px_per_css_px']}y image px per CSS px"
        ),
        f"- accuracy notes: {calibration['accuracy_notes']}",
        "",
    ]

    if report["rects"]:
        lines.extend(
            [
                "### Rectangles",
                "| item | x | y | width | height | confidence |",
                "|---|---:|---:|---:|---:|---|",
            ]
        )
        for item in report["rects"]:
            css = item["css_px"]
            lines.append(f"| {item['name']} | {css['x']}px | {css['y']}px | {css['width']}px | {css['height']}px | {item['confidence']} |")
        lines.append("")

    if report["distances"]:
        lines.extend(
            [
                "### Distances",
                "| item | dx | dy | distance | confidence |",
                "|---|---:|---:|---:|---|",
            ]
        )
        for item in report["distances"]:
            css = item["css_px"]
            lines.append(f"| {item['name']} | {css['dx']}px | {css['dy']}px | {css['distance']}px | {item['confidence']} |")
        lines.append("")

    if report["colors"]:
        lines.extend(
            [
                "### Colors",
                "| item | color | confidence |",
                "|---|---|---|",
            ]
        )
        for item in report["colors"]:
            lines.append(f"| {item['name']} | `{item['hex']}` | {item['confidence']} |")
        lines.append("")

    if report["radii"]:
        lines.extend(
            [
                "### Radius",
                "| item | radius | confidence | notes |",
                "|---|---:|---|---|",
            ]
        )
        for item in report["radii"]:
            value = "unknown" if item["css_px"] is None else f"{item['css_px']}px"
            lines.append(f"| {item['name']} | {value} | {item['confidence']} | {item['notes']} |")
        lines.append("")

    if report["typography"]:
        lines.extend(
            [
                "### Typography",
                "| role | size | line-height | confidence | notes |",
                "|---|---:|---:|---|---|",
            ]
        )
        for item in report["typography"]:
            lines.append(
                f"| {item['name']} | {item['estimated_size_px']}px | "
                f"{item['estimated_line_height_px']}px | {item['confidence']} | {item['notes']} |"
            )
        lines.append("")

    tokens = report["tokens_to_consider"]
    lines.extend(
        [
            "### Tokens To Consider",
            f"- spacing: {', '.join(str(value) for value in tokens['spacing_px']) or 'unknown'}",
            f"- radius: {', '.join(str(value) for value in tokens['radius_px']) or 'unknown'}",
            f"- typography: {', '.join(str(value) for value in tokens['typography_px']) or 'unknown'}",
            "",
        ]
    )

    if report["adaptations"]:
        lines.extend(
            [
                "### Adaptation Targets",
                "| target | viewport | spacing | radius | typography | layout guidance |",
                "|---|---:|---|---|---|---|",
            ]
        )
        for item in report["adaptations"]:
            viewport = item["viewport_css_px"]
            tokens = item["tokens"]
            spacing = ", ".join(str(value) for value in tokens["spacing_px"]) or "unknown"
            radius = ", ".join(str(value) for value in tokens["radius_px"]) or "unknown"
            typography = ", ".join(str(value) for value in tokens["typography_px"]) or "unknown"
            guidance = f"{item['layout_guidance']['page_padding']}; {item['layout_guidance']['content_width']}"
            lines.append(f"| {item['name']} | {viewport['width']}x{viewport['height']} | {spacing} | {radius} | {typography} | {guidance} |")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure UI screenshots into CSS-pixel design tokens from explicit coordinates."
    )
    parser.add_argument("image", type=Path, help="Screenshot or mockup image to measure.")
    parser.add_argument("--source-viewport", type=parse_viewport, help="Reference design CSS viewport, for example 390x844.")
    parser.add_argument("--viewport", type=parse_viewport, help="Alias for --source-viewport, kept for compatibility.")
    parser.add_argument("--target-viewport", type=parse_named_viewport, action="append", default=[], help="Implementation target viewport for adapted token suggestions: name:WIDTHxHEIGHT or WIDTHxHEIGHT. Can be repeated.")
    parser.add_argument("--rect", type=parse_rect, action="append", default=[], help="Measure an element box: name:x,y,w,h in image pixels.")
    parser.add_argument("--distance", type=parse_distance, action="append", default=[], help="Measure a gap/distance: name:x1,y1,x2,y2 in image pixels.")
    parser.add_argument("--sample", type=parse_point, action="append", default=[], help="Sample a single pixel color: name:x,y in image pixels.")
    parser.add_argument("--sample-box", type=parse_rect, action="append", default=[], help="Average a color region: name:x,y,w,h in image pixels.")
    parser.add_argument("--radius-probe", type=parse_rect, action="append", default=[], help="Estimate rounded-corner radius from an element box: name:x,y,w,h.")
    parser.add_argument("--manual-radius", type=parse_manual_value, action="append", default=[], help="Convert a manually measured image-pixel radius: name:px.")
    parser.add_argument("--text", type=parse_text_box, action="append", default=[], help="Estimate type from text bounds: role:x,y,w,h or role:x,y,w,h,lines.")
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
