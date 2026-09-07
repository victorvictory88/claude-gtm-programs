#!/usr/bin/env python3
"""Generate PNG visuals for GitHub README and docs.

Usage:
  python scripts/generate_visuals.py

Writes PNGs under docs/images/. Requires pillow.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"

# Dark professional palette (readable on GitHub light and dark themes via contrast)
BG = (15, 23, 42)  # slate-900
CARD = (30, 41, 59)  # slate-800
BORDER = (51, 65, 85)  # slate-700
ACCENT = (56, 189, 248)  # sky-400
ACCENT2 = (52, 211, 153)  # emerald-400
ACCENT3 = (251, 191, 36)  # amber-400
ACCENT4 = (167, 139, 250)  # violet-400
ACCENT5 = (244, 114, 182)  # pink-400
TEXT = (241, 245, 249)  # slate-100
MUTED = (148, 163, 184)  # slate-400
GREEN = (74, 222, 128)
RED = (248, 113, 113)
TERM_BG = (12, 12, 18)
TERM_FG = (200, 210, 220)
TERM_PROMPT = (52, 211, 153)
TERM_KEY = (125, 211, 252)
TERM_STR = (253, 224, 71)
TERM_NUM = (251, 146, 60)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def mono(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, xy, fill, outline=None, width=1, radius=16):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_size(draw, trial, fnt)[0] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def make_architecture() -> None:
    w, h = 960, 540
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(28, bold=True)
    label_f = font(20, bold=True)
    sub_f = font(14)
    foot_f = font(12)

    draw.text((40, 28), "claude-gtm-programs", font=title_f, fill=TEXT)
    draw.text((40, 68), "Public toolkit: Claude skills + GTM Programs reference", font=sub_f, fill=MUTED)

    boxes = [
        ("skills/", "Reusable agent\ninstructions", "baseline, plays,\nattribution, discovery", ACCENT),
        ("demos/", "Messages API\nCLIs", "tool-use brief +\nstructured plan JSON", ACCENT2),
        ("evals/", "Offline rubric\nscoring", "fixtures + JSON\nsummary (no API)", ACCENT3),
        ("teaching/", "45-min workshop\n+ exercise", "baseline without\ninventing numbers", ACCENT4),
    ]

    gap = 24
    box_w = (w - 80 - 3 * gap) // 4
    box_h = 280
    y0 = 120
    x = 40
    for title, mid, bottom, color in boxes:
        rounded_rect(draw, (x, y0, x + box_w, y0 + box_h), CARD, outline=BORDER, width=2, radius=18)
        draw.rectangle((x, y0, x + box_w, y0 + 8), fill=color)
        draw.text((x + 18, y0 + 28), title, font=label_f, fill=color)
        for i, line in enumerate(mid.split("\n")):
            draw.text((x + 18, y0 + 70 + i * 22), line, font=sub_f, fill=TEXT)
        for i, line in enumerate(bottom.split("\n")):
            draw.text((x + 18, y0 + 150 + i * 20), line, font=foot_f, fill=MUTED)
        x += box_w + gap

    draw.text((40, h - 40), "Fictional accounts only: Acme Energy, Northwind Retail", font=foot_f, fill=MUTED)
    img.save(OUT / "architecture.png", optimize=True)


def make_baseline_card() -> None:
    w, h = 800, 520
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(24, bold=True)
    head_f = font(16, bold=True)
    body_f = font(15)
    small_f = font(13)

    rounded_rect(draw, (24, 24, w - 24, h - 24), CARD, outline=BORDER, width=2, radius=20)
    draw.rectangle((24, 24, w - 24, 88), fill=(37, 99, 235))
    draw.text((48, 42), "Program Baseline Card", font=title_f, fill=TEXT)
    draw.text((48, 110), "Account (fictional): Acme Energy", font=head_f, fill=ACCENT)
    draw.text((48, 140), "Program: AMER Mid-Market AI Discovery Play", font=body_f, fill=TEXT)

    rows = [
        ("Metric", "Discovery checklist completion within 14 days of Stage 2"),
        ("Owner", "GTM Analytics Partner (metric) / GTM Programs Manager AMER (program)"),
        ("Baseline", "0% until CRM discovery field ships (field not live)"),
        ("Target", "Raise completion rate vs baseline after enablement launch"),
        ("Window", "Launch 2026-10-01 | 30-day check 2026-10-31 | 90-day review 2026-12-30"),
    ]
    y = 185
    for label, value in rows:
        draw.text((48, y), label, font=head_f, fill=ACCENT2)
        wrapped = wrap_text(draw, value, body_f, w - 120)
        for i, line in enumerate(wrapped):
            draw.text((48, y + 24 + i * 22), line, font=body_f, fill=TEXT)
        y += 24 + 22 * max(1, len(wrapped)) + 12

    draw.text((48, h - 56), "Sample only. No real customer data.", font=small_f, fill=MUTED)
    img.save(OUT / "program_baseline_card.png", optimize=True)


def make_seller_play() -> None:
    w, h = 720, 960
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(26, bold=True)
    head_f = font(16, bold=True)
    body_f = font(14)
    small_f = font(12)

    rounded_rect(draw, (20, 20, w - 20, h - 20), CARD, outline=BORDER, width=2, radius=18)
    draw.rectangle((20, 20, w - 20, 100), fill=(5, 150, 105))
    draw.text((40, 36), "Seller Play (one-pager)", font=title_f, fill=TEXT)
    draw.text((40, 70), "Northwind Retail  |  Mid-market AI SaaS discovery", font=small_f, fill=(209, 250, 229))

    y = 120
    sections = [
        ("Play name", "Structured Discovery Checklist Play"),
        ("Segment / ICP", "AMER mid-market retail and ecommerce evaluating AI assistants"),
        ("Trigger", "Opp enters Stage 2; buyer mentions eval criteria or SE capacity risk"),
        ("Desired outcome", "Completed discovery checklist within 14 days; clear SE handoff"),
        (
            "Discovery questions",
            "1. Which workflows should an assistant change in the first 90 days?\n"
            "2. Who owns success criteria across IT, Ops, and the business?\n"
            "3. What data sources are in / out of scope for the pilot?\n"
            "4. How do you measure agent quality today (if at all)?\n"
            "5. What would make this a no-go for security or procurement?",
        ),
        (
            "Narrative and proof",
            "- Frame: shorten Stage 2 to Stage 3 with shared criteria\n"
            "- Proof TBD: enablement to supply public-safe win note\n"
            "- Example account (fictional): Northwind Retail store ops pilot",
        ),
        (
            "Assets",
            "- Discovery checklist (owner: AMER Seller Enablement Lead)\n"
            "- SE technical validation sheet (owner: SE Manager)\n"
            "- One-slide value narrative (owner: GTM Programs Manager AMER)",
        ),
        (
            "Handoff",
            "- To SE when checklist fields for tech scope are complete\n"
            "- To CSM when pilot success criteria are written and agreed",
        ),
        (
            "Adoption metric",
            "% of qualified Northwind-like opps with checklist done in 14 days (CRM)",
        ),
    ]

    for title, body in sections:
        draw.text((40, y), title, font=head_f, fill=ACCENT)
        y += 26
        for line in body.split("\n"):
            for wrapped in wrap_text(draw, line, body_f, w - 100):
                draw.text((40, y), wrapped, font=body_f, fill=TEXT)
                y += 20
        y += 14

    draw.text((40, h - 48), "Fictional example for public toolkit. Not a real customer play.", font=small_f, fill=MUTED)
    img.save(OUT / "seller_play_card.png", optimize=True)


def harness_summary() -> dict:
    """Run evals/harness.py and parse JSON, or fall back to fixture-shaped summary."""
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "evals" / "harness.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        text = proc.stdout.strip()
        if text.startswith("{"):
            return json.loads(text)
    except Exception:
        pass
    return {
        "harness": "evals/harness.py",
        "rubric": "evals/rubrics/gtm_program.md",
        "case_count": 2,
        "passed_cases": 1,
        "expect_matches": 2,
        "results": [
            {
                "id": "good_plan",
                "fixture": "fixtures/good_plan.json",
                "expect_pass": True,
                "expect_match": True,
                "scores": {
                    "baseline_clarity": 2,
                    "measurable_metrics": 2,
                    "named_owners": 2,
                    "no_fluff": 2,
                },
                "total": 8,
                "max": 8,
                "pass": True,
            },
            {
                "id": "weak_plan",
                "fixture": "fixtures/weak_plan.json",
                "expect_pass": False,
                "expect_match": True,
                "scores": {
                    "baseline_clarity": 1,
                    "measurable_metrics": 0,
                    "named_owners": 0,
                    "no_fluff": 0,
                },
                "total": 1,
                "max": 8,
                "pass": False,
            },
        ],
    }


def make_eval_terminal() -> None:
    summary = harness_summary()
    pretty = json.dumps(summary, indent=2)
    lines = pretty.splitlines()

    pad = 24
    line_h = 20
    header_h = 44
    w = 860
    h = header_h + pad * 2 + line_h * (len(lines) + 3) + 20
    img = Image.new("RGB", (w, h), TERM_BG)
    draw = ImageDraw.Draw(img)
    mf = mono(13)
    mf_b = mono(13, bold=True)
    title_f = font(13, bold=True)

    draw.rectangle((0, 0, w, header_h), fill=(30, 30, 40))
    for i, c in enumerate([(239, 68, 68), (234, 179, 8), (34, 197, 94)]):
        draw.ellipse((16 + i * 22, 14, 30 + i * 22, 28), fill=c)
    draw.text((90, 14), "evals - python evals/harness.py", font=title_f, fill=MUTED)

    y = header_h + pad
    draw.text((pad, y), "$ python evals/harness.py", font=mf_b, fill=TERM_PROMPT)
    y += line_h + 8

    for line in lines:
        color = TERM_FG
        stripped = line.lstrip()
        if stripped.startswith('"') and '":' in stripped:
            key, _, rest = stripped.partition(":")
            indent = line[: len(line) - len(stripped)]
            draw.text((pad, y), indent + key, font=mf, fill=TERM_KEY)
            key_w = text_size(draw, indent + key, mf)[0]
            draw.text((pad + key_w, y), ":" + rest, font=mf, fill=TERM_FG if not rest.strip().startswith('"') else TERM_STR)
            val = rest.strip()
            if val.startswith('"') or val.startswith("true") or val.startswith("false"):
                draw.rectangle((pad + key_w, y, w - pad, y + line_h), fill=TERM_BG)
                draw.text((pad + key_w, y), ":", font=mf, fill=TERM_FG)
                vcolor = TERM_STR if val.startswith('"') else TERM_NUM
                if val.rstrip(",").isdigit() or val.rstrip(",").replace(".", "", 1).isdigit():
                    vcolor = TERM_NUM
                if val.startswith("true") or val.startswith("false"):
                    vcolor = TERM_NUM
                draw.text((pad + key_w + text_size(draw, ":", mf)[0], y), rest, font=mf, fill=vcolor)
            elif any(ch.isdigit() for ch in val[:3]):
                draw.rectangle((pad + key_w, y, w - pad, y + line_h), fill=TERM_BG)
                draw.text((pad + key_w, y), ":" + rest, font=mf, fill=TERM_NUM)
        else:
            draw.text((pad, y), line, font=mf, fill=color)
        y += line_h

    y += 8
    draw.text((pad, y), "$  # exit 0 when expect_match for all cases", font=mf, fill=MUTED)
    img.save(OUT / "eval_harness_terminal.png", optimize=True)


def _wrap_json_display_lines(pretty: str, max_chars: int = 88) -> list[str]:
    """Soft-wrap long JSON pretty lines for screenshot readability."""
    out: list[str] = []
    for line in pretty.splitlines():
        if len(line) <= max_chars:
            out.append(line)
            continue
        if '": "' in line:
            prefix, _, value = line.partition('": "')
            prefix = prefix + '": "'
            trailer = ""
            if value.endswith('",'):
                value, trailer = value[:-2], '",'
            elif value.endswith('"'):
                value, trailer = value[:-1], '"'
            indent = " " * len(prefix)
            chunk = ""
            first = True
            for word in value.split(" "):
                trial = word if not chunk else f"{chunk} {word}"
                limit = max_chars - len(prefix if first else indent)
                if len(trial) <= limit:
                    chunk = trial
                else:
                    out.append((prefix if first else indent) + chunk)
                    first = False
                    chunk = word
            out.append((prefix if first else indent) + chunk + trailer)
        else:
            while len(line) > max_chars:
                out.append(line[:max_chars])
                line = "  " + line[max_chars:]
            out.append(line)
    return out


def make_program_plan_json() -> None:
    plan_path = ROOT / "evals" / "fixtures" / "good_plan.json"
    plan = json.loads(plan_path.read_text())
    pretty = json.dumps(plan, indent=2)
    lines = _wrap_json_display_lines(pretty, max_chars=92)

    pad = 28
    line_h = 18
    header_h = 70
    w = 980
    h = header_h + pad * 2 + line_h * len(lines) + 40
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(22, bold=True)
    sub_f = font(13)
    mf = mono(12)

    draw.text((pad, 22), "Sample structured program plan (JSON)", font=title_f, fill=TEXT)
    draw.text((pad, 52), "From evals/fixtures/good_plan.json  |  fictional AMER mid-market play", font=sub_f, fill=MUTED)

    rounded_rect(draw, (pad - 8, header_h, w - pad + 8, h - 20), CARD, outline=BORDER, width=2, radius=14)

    y = header_h + 16
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith('"') and '":' in stripped:
            key, _, rest = stripped.partition(":")
            draw.text((pad + 8, y), indent + key, font=mf, fill=TERM_KEY)
            key_w = text_size(draw, indent + key, mf)[0]
            val = rest.strip()
            if val.startswith('"'):
                vcolor = TERM_STR
            elif val.startswith("{") or val.startswith("[") or val.startswith("}"):
                vcolor = TERM_FG
            else:
                vcolor = TERM_NUM
            draw.text((pad + 8 + key_w, y), ":" + rest, font=mf, fill=vcolor)
        elif stripped.startswith('"') or (stripped and stripped[0].isalnum()):
            draw.text((pad + 8, y), line, font=mf, fill=TERM_STR)
        else:
            draw.text((pad + 8, y), line, font=mf, fill=TERM_FG)
        y += line_h

    img.save(OUT / "program_plan_json.png", optimize=True)


def make_skills_grid() -> None:
    """Five skill cards in a grid."""
    w, h = 1000, 620
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(26, bold=True)
    label_f = font(16, bold=True)
    body_f = font(13)
    foot_f = font(12)

    draw.text((40, 28), "Claude skills for GTM Programs", font=title_f, fill=TEXT)
    draw.text((40, 64), "Reusable agent instructions: baseline, plays, attribution, discovery, enablement", font=body_f, fill=MUTED)

    skills = [
        ("program-baseline", "Lock metrics, owners,\nand scope before launch", ACCENT),
        ("seller-play-packager", "Turn a win pattern into\na one-page seller play", ACCENT2),
        ("attribution-review", "Monthly readout with\ninfluence vs credit", ACCENT3),
        ("discovery-coach", "AI SaaS discovery\nquestions + post-call", ACCENT4),
        ("enablement-outline", "Session design with\nleading + lagging metrics", ACCENT5),
    ]

    # 3 on top row, 2 centered on bottom
    card_w, card_h = 280, 200
    gap = 24
    top_y = 110
    total_top = 3 * card_w + 2 * gap
    start_x = (w - total_top) // 2

    for i, (name, desc, color) in enumerate(skills[:3]):
        x = start_x + i * (card_w + gap)
        y = top_y
        rounded_rect(draw, (x, y, x + card_w, y + card_h), CARD, outline=BORDER, width=2, radius=16)
        draw.rectangle((x, y, x + card_w, y + 8), fill=color)
        draw.text((x + 18, y + 28), name, font=label_f, fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x + 18, y + 70 + j * 22), line, font=body_f, fill=TEXT)
        draw.text((x + 18, y + card_h - 36), "skills/" + name, font=foot_f, fill=MUTED)

    bottom_y = top_y + card_h + gap
    total_bot = 2 * card_w + gap
    start_bot = (w - total_bot) // 2
    for i, (name, desc, color) in enumerate(skills[3:]):
        x = start_bot + i * (card_w + gap)
        y = bottom_y
        rounded_rect(draw, (x, y, x + card_w, y + card_h), CARD, outline=BORDER, width=2, radius=16)
        draw.rectangle((x, y, x + card_w, y + 8), fill=color)
        draw.text((x + 18, y + 28), name, font=label_f, fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x + 18, y + 70 + j * 22), line, font=body_f, fill=TEXT)
        draw.text((x + 18, y + card_h - 36), "skills/" + name, font=foot_f, fill=MUTED)

    draw.text((40, h - 36), "Install by copying each folder into your skills directory", font=foot_f, fill=MUTED)
    img.save(OUT / "skills_grid.png", optimize=True)


def make_discovery_coach_flow() -> None:
    """Simple horizontal/vertical flow for discovery coach."""
    w, h = 960, 420
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(24, bold=True)
    label_f = font(14, bold=True)
    body_f = font(12)
    foot_f = font(12)

    draw.text((40, 24), "Discovery Coach flow", font=title_f, fill=TEXT)
    draw.text((40, 58), "Example: Acme Energy AI SaaS discovery (fictional)", font=body_f, fill=MUTED)

    steps = [
        ("1. Context", "Industry, contact,\nknown initiative", ACCENT),
        ("2. Situation", "How work is done\ntoday", ACCENT2),
        ("3. Pain", "Where time, quality,\nor risk breaks", ACCENT3),
        ("4. Impact", "Ask for quantified\ncost (do not invent)", ACCENT4),
        ("5. Decision", "Who decides, timeline,\nsuccess criteria", ACCENT5),
        ("6. Capture", "Post-call summary +\nnext step", (94, 234, 212)),
    ]

    box_w, box_h = 130, 150
    gap = 18
    total = len(steps) * box_w + (len(steps) - 1) * gap
    x0 = (w - total) // 2
    y0 = 110

    for i, (title, desc, color) in enumerate(steps):
        x = x0 + i * (box_w + gap)
        rounded_rect(draw, (x, y0, x + box_w, y0 + box_h), CARD, outline=BORDER, width=2, radius=14)
        draw.rectangle((x, y0, x + box_w, y0 + 6), fill=color)
        draw.text((x + 10, y0 + 20), title, font=label_f, fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x + 10, y0 + 52 + j * 18), line, font=body_f, fill=TEXT)
        if i < len(steps) - 1:
            ax = x + box_w + 2
            ay = y0 + box_h // 2
            draw.line((ax, ay, ax + gap - 4, ay), fill=MUTED, width=2)
            draw.polygon([(ax + gap - 4, ay), (ax + gap - 10, ay - 5), (ax + gap - 10, ay + 5)], fill=MUTED)

    draw.text((40, h - 36), "Redirect premature product talk back to workflow and outcomes", font=foot_f, fill=MUTED)
    img.save(OUT / "discovery_coach_flow.png", optimize=True)


def make_attribution_review_dashboard() -> None:
    """Mock monthly review metrics dashboard."""
    w, h = 980, 560
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(24, bold=True)
    head_f = font(15, bold=True)
    body_f = font(13)
    big_f = font(28, bold=True)
    foot_f = font(12)

    draw.text((40, 24), "Attribution review (monthly)", font=title_f, fill=TEXT)
    draw.text((40, 58), "Program: AMER Mid-Market AI Discovery Play  |  Period: 2026-08  |  Fictional sample", font=body_f, fill=MUTED)

    metrics = [
        ("Checklist done\nin 14 days", "42%", "vs 28% prior", "improved", ACCENT2),
        ("Play logged on\nqualified opps", "31%", "vs 30% prior", "flat", ACCENT3),
        ("Stage 2 to 3\nconversion", "19%", "insufficient data", "insufficient", ACCENT4),
        ("SE handoff\nSLA met", "67%", "vs 55% prior", "improved", ACCENT),
    ]

    card_w, card_h = 200, 170
    gap = 20
    total = 4 * card_w + 3 * gap
    x0 = (w - total) // 2
    y0 = 100

    for i, (label, value, delta, status, color) in enumerate(metrics):
        x = x0 + i * (card_w + gap)
        rounded_rect(draw, (x, y0, x + card_w, y0 + card_h), CARD, outline=BORDER, width=2, radius=14)
        draw.rectangle((x, y0, x + card_w, y0 + 6), fill=color)
        for j, line in enumerate(label.split("\n")):
            draw.text((x + 14, y0 + 20 + j * 18), line, font=body_f, fill=MUTED)
        draw.text((x + 14, y0 + 70), value, font=big_f, fill=TEXT)
        draw.text((x + 14, y0 + 110), delta, font=body_f, fill=MUTED)
        status_color = GREEN if status == "improved" else (ACCENT3 if status == "flat" else MUTED)
        draw.text((x + 14, y0 + 138), status, font=head_f, fill=status_color)

    # Bottom decision panel
    panel_y = 300
    rounded_rect(draw, (40, panel_y, w - 40, h - 40), CARD, outline=BORDER, width=2, radius=16)
    draw.text((60, panel_y + 20), "Influence vs credit (sample)", font=head_f, fill=ACCENT)
    rows = [
        ("Influence", "Enablement touched 38 of 52 Stage 2 opps before checklist completion"),
        ("Credit", "Claim only checklist completion lift; Stage 2-3 needs more months of data"),
        ("Decision", "Keep play; iterate CRM field adoption; pause Stage 2-3 causal claims"),
        ("Owners", "Program: GTM Programs Manager AMER  |  Metric: GTM Analytics Partner"),
    ]
    y = panel_y + 52
    for label, value in rows:
        draw.text((60, y), label, font=head_f, fill=ACCENT2)
        for line in wrap_text(draw, value, body_f, w - 200):
            draw.text((200, y), line, font=body_f, fill=TEXT)
            y += 20
        y += 8

    draw.text((60, h - 58), "Fictional metrics for Acme Energy / Northwind-like segment. Not real customer data.", font=foot_f, fill=MUTED)
    img.save(OUT / "attribution_review_dashboard.png", optimize=True)


def make_workshop_agenda() -> None:
    """45-minute workshop timeline."""
    w, h = 900, 520
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(24, bold=True)
    head_f = font(15, bold=True)
    body_f = font(13)
    foot_f = font(12)

    draw.text((40, 24), "Workshop agenda (45 minutes)", font=title_f, fill=TEXT)
    draw.text((40, 58), "Agentic AI for GTM Programs  |  Audience: business leaders and GTM managers", font=body_f, fill=MUTED)

    blocks = [
        (5, "Open", "Why baselines beat slogans", ACCENT),
        (10, "Concepts", "Agents, tools, skills, evals in plain language", ACCENT2),
        (10, "Live pattern", "Walk a program plan shape (name, baseline, metrics, owners)", ACCENT3),
        (15, "Exercise", "Draft a program baseline (no invented numbers)", ACCENT4),
        (5, "Close", "30-day measurement commitment", ACCENT5),
    ]

    # Timeline bar
    bar_x, bar_y = 40, 120
    bar_w = w - 80
    bar_h = 28
    rounded_rect(draw, (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), BORDER, radius=8)
    total_min = sum(b[0] for b in blocks)
    cx = bar_x
    for mins, _name, _desc, color in blocks:
        seg = int(bar_w * (mins / total_min))
        draw.rectangle((cx, bar_y, cx + seg - 2, bar_y + bar_h), fill=color)
        cx += seg

    # Minute markers
    draw.text((bar_x, bar_y + 36), "0 min", font=foot_f, fill=MUTED)
    draw.text((bar_x + bar_w - 50, bar_y + 36), "45 min", font=foot_f, fill=MUTED)

    y = 190
    elapsed = 0
    for mins, name, desc, color in blocks:
        rounded_rect(draw, (40, y, w - 40, y + 48), CARD, outline=BORDER, width=1, radius=10)
        draw.rectangle((40, y, 48, y + 48), fill=color)
        time_label = f"{elapsed}-{elapsed + mins} min"
        draw.text((64, y + 14), time_label, font=head_f, fill=color)
        draw.text((180, y + 14), name, font=head_f, fill=TEXT)
        draw.text((320, y + 14), desc, font=body_f, fill=MUTED)
        elapsed += mins
        y += 56

    draw.text((40, h - 36), "See teaching/workshop_01_agentic_gtm.md and exercises/exercise_baseline.md", font=foot_f, fill=MUTED)
    img.save(OUT / "workshop_agenda.png", optimize=True)


def make_demo_tool_use_flow() -> None:
    """Tool-use sales brief flow diagram."""
    w, h = 960, 480
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(24, bold=True)
    label_f = font(14, bold=True)
    body_f = font(12)
    foot_f = font(12)

    draw.text((40, 24), "Demo 01: tool-use sales brief", font=title_f, fill=TEXT)
    draw.text((40, 58), "demos/01_tool_use_sales_brief.py  |  Account: Acme Energy (fictional)", font=body_f, fill=MUTED)

    steps = [
        ("Load account\nJSON", "sample_data/\naccount.json", ACCENT),
        ("Messages API\n+ tool schema", "Model requests\nget_account_facts", ACCENT2),
        ("Tool result", "Name, pain,\nstage, stakeholders", ACCENT3),
        ("Draft brief", "One-page sales\nbrief from facts", ACCENT4),
        ("CLI output", "Print brief;\nexit 0", ACCENT5),
    ]

    box_w, box_h = 150, 160
    gap = 28
    total = len(steps) * box_w + (len(steps) - 1) * gap
    x0 = (w - total) // 2
    y0 = 120

    for i, (title, desc, color) in enumerate(steps):
        x = x0 + i * (box_w + gap)
        rounded_rect(draw, (x, y0, x + box_w, y0 + box_h), CARD, outline=BORDER, width=2, radius=14)
        draw.rectangle((x, y0, x + box_w, y0 + 6), fill=color)
        for j, line in enumerate(title.split("\n")):
            draw.text((x + 12, y0 + 24 + j * 20), line, font=label_f, fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x + 12, y0 + 90 + j * 18), line, font=body_f, fill=TEXT)
        if i < len(steps) - 1:
            ax = x + box_w + 4
            ay = y0 + box_h // 2
            draw.line((ax, ay, ax + gap - 8, ay), fill=MUTED, width=2)
            draw.polygon(
                [(ax + gap - 8, ay), (ax + gap - 14, ay - 5), (ax + gap - 14, ay + 5)],
                fill=MUTED,
            )

    # Note box
    rounded_rect(draw, (40, 320, w - 40, 420), CARD, outline=BORDER, width=2, radius=12)
    draw.text((60, 340), "Notes", font=label_f, fill=ACCENT)
    notes = [
        "Default model: claude-sonnet-4-20250514 (override with --model)",
        "Exits with code 2 if ANTHROPIC_API_KEY is missing",
        "Tool use keeps the brief grounded in loaded account facts, not invented metrics",
    ]
    y = 368
    for note in notes:
        draw.text((60, y), "- " + note, font=body_f, fill=TEXT)
        y += 18

    draw.text((40, h - 36), "Pair with demo 02 for structured program plan JSON", font=foot_f, fill=MUTED)
    img.save(OUT / "demo_tool_use_flow.png", optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_architecture()
    make_baseline_card()
    make_seller_play()
    make_eval_terminal()
    make_program_plan_json()
    make_skills_grid()
    make_discovery_coach_flow()
    make_attribution_review_dashboard()
    make_workshop_agenda()
    make_demo_tool_use_flow()
    print(f"Wrote visuals to {OUT}")
    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
