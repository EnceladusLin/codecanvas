"""SVG generator for CodeCanvas."""
import svgwrite
from datetime import datetime, timedelta
from typing import Optional


# Color schemes
SCHEMES = {
    "github": {
        "bg": "#0d1117",
        "text": "#c9d1d9",
        "accent": "#58a6ff",
        "level0": "#161b22",
        "level1": "#0e4429",
        "level2": "#006d32",
        "level3": "#26a641",
        "level4": "#39d353",
    },
    "sunset": {
        "bg": "#1a0a2e",
        "text": "#f5e6ff",
        "accent": "#ff79c6",
        "level0": "#1a0a2e",
        "level1": "#4a1942",
        "level2": "#7b2d6e",
        "level3": "#a04595",
        "level4": "#ff79c6",
    },
    "ocean": {
        "bg": "#0a1628",
        "text": "#e0f2fe",
        "accent": "#38bdf8",
        "level0": "#0a1628",
        "level1": "#0c4a6e",
        "level2": "#0369a1",
        "level3": "#0ea5e9",
        "level4": "#7dd3fc",
    },
    "terminal": {
        "bg": "#000000",
        "text": "#00ff00",
        "accent": "#00ff00",
        "level0": "#0a0a0a",
        "level1": "#0d1a0d",
        "level2": "#1a331a",
        "level3": "#336633",
        "level4": "#00ff00",
    },
}


def _commits_to_level(commits: int, max_commits: int) -> int:
    """Convert commit count to contribution level (0-4)."""
    if commits == 0:
        return 0
    ratio = commits / max(max_commits, 1)
    if ratio < 0.2:
        return 1
    elif ratio < 0.4:
        return 2
    elif ratio < 0.7:
        return 3
    return 4


def render_heatmap(
    by_day: dict,
    days: int = 365,
    scheme: str = "github",
    title: str = "Coding Activity",
    cell_size: int = 12,
    gap: int = 3,
    width: int = 900,
) -> str:
    """Render contribution heatmap as SVG."""
    if scheme not in SCHEMES:
        scheme = "github"
    c = SCHEMES[scheme]

    weeks = days // 7 + 1
    cols = weeks
    rows = 7

    margin_top = 40
    margin_left = 30
    margin_right = 10
    margin_bottom = 10

    svg_width = margin_left + cols * (cell_size + gap) + margin_right
    svg_height = margin_top + rows * (cell_size + gap) + margin_bottom

    dwg = svgwrite.Drawing(size=(svg_width, svg_height))
    dwg.defs.add(dwg.style(f"""
        rect {{ stroke: none }}
        text {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif }}
    """))

    # Background
    dwg.add(dwg.rect((0, 0), (svg_width, svg_height), fill=c["bg"]))

    # Title
    dwg.add(dwg.text(
        title,
        insert=(margin_left, 20),
        fill=c["text"],
        font_size="14",
        font_weight="bold",
    ))

    # Month labels
    today = datetime.now()
    start = today - timedelta(days=days)
    current_month = -1
    for w in range(cols):
        date = start + timedelta(weeks=w)
        if date.month != current_month:
            month_name = date.strftime("%b")
            dwg.add(dwg.text(
                month_name,
                insert=(margin_left + w * (cell_size + gap), 34),
                fill=c["text"],
                font_size="9",
                opacity="0.6",
            ))
            current_month = date.month

    # Cells
    today = datetime.now()
    start = today - timedelta(days=days)
    max_c = max(by_day.values()) if by_day else 1

    for w in range(cols):
        for d in range(7):
            idx = w * 7 + d
            date = start + timedelta(days=idx)
            key = date.strftime("%Y-%m-%d")
            commits = by_day.get(key, 0)
            level = _commits_to_level(commits, max_c)
            color = c[f"level{level}"]

            x = margin_left + w * (cell_size + gap)
            y = margin_top + d * (cell_size + gap)

            rect = dwg.add(dwg.rect((x, y), (cell_size, cell_size), fill=color, rx=2))
            if commits > 0:
                rect.set_desc(f"{key}: {commits} commits")

    # Legend
    legend_x = svg_width - margin_right - 150
    legend_y = margin_top
    dwg.add(dwg.text("Less", insert=(legend_x, legend_y + 8), fill=c["text"], font_size="9", opacity="0.6"))
    for i in range(5):
        rect = dwg.add(dwg.rect(
            (legend_x + 30 + i * (cell_size + 2), legend_y),
            (cell_size, cell_size),
            fill=c[f"level{i}"],
            rx=2,
        ))
    dwg.add(dwg.text("More", insert=(legend_x + 30 + 5 * (cell_size + 2) + 4, legend_y + 8), fill=c["text"], font_size="9", opacity="0.6"))

    return dwg.tostring()


def render_weekly_bar(
    by_weekday: dict,
    scheme: str = "github",
    title: str = "Commits by Day",
    width: int = 400,
    height: int = 200,
) -> str:
    """Render weekly bar chart as SVG."""
    if scheme not in SCHEMES:
        scheme = "github"
    c = SCHEMES[scheme]

    margin = 40
    chart_w = width - margin * 2
    chart_h = height - margin * 2
    bar_w = chart_w / 7 - 8

    dwg = svgwrite.Drawing(size=(width, height))
    dwg.defs.add(dwg.style("""
        rect { stroke: none }
        text { font-family: -apple-system, BlinkMacSystemFont, sans-serif }
    """))

    dwg.add(dwg.rect((0, 0), (width, height), fill=c["bg"]))

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    max_v = max(by_weekday.values()) if by_weekday else 1

    for i, day in enumerate(days):
        v = by_weekday.get(i, 0)
        bar_h = (v / max_v) * chart_h if max_v > 0 else 0
        x = margin + i * (chart_w / 7) + 4
        y = margin + chart_h - bar_h

        dwg.add(dwg.rect((x, y), (bar_w, bar_h), fill=c["accent"], rx=3))
        dwg.add(dwg.text(
            str(v),
            insert=(x + bar_w / 2, y - 6),
            fill=c["text"],
            font_size="10",
            text_anchor="middle",
        ))
        dwg.add(dwg.text(
            day,
            insert=(x + bar_w / 2, height - 12),
            fill=c["text"],
            font_size="10",
            text_anchor="middle",
            opacity="0.6",
        ))

    dwg.add(dwg.text(
        title,
        insert=(width / 2, 20),
        fill=c["text"],
        font_size="12",
        text_anchor="middle",
        font_weight="bold",
    ))

    return dwg.tostring()


def render_hourly_heatmap(
    by_hour: dict,
    scheme: str = "github",
    title: str = "Commits by Hour",
    width: int = 400,
    height: int = 160,
) -> str:
    """Render hourly heatmap as SVG."""
    if scheme not in SCHEMES:
        scheme = "github"
    c = SCHEMES[scheme]

    margin = 40
    cell = 28
    gap = 4
    chart_w = 24 * (cell + gap)
    chart_h = cell + gap * 2

    svg_w = chart_w + margin * 2
    svg_h = chart_h + margin * 2 + 20

    dwg = svgwrite.Drawing(size=(svg_w, svg_h))
    dwg.defs.add(dwg.style("""
        rect { stroke: none }
        text { font-family: -apple-system, BlinkMacSystemFont, sans-serif }
    """))

    dwg.add(dwg.rect((0, 0), (svg_w, svg_h), fill=c["bg"]))

    max_v = max(by_hour.values()) if by_hour else 1

    for h in range(24):
        v = by_hour.get(h, 0)
        ratio = v / max_v
        level = 0 if v == 0 else int(ratio * 4) + 1
        level = min(level, 4)
        color = c[f"level{level}"]

        x = margin + h * (cell + gap)
        y = margin + gap

        dwg.add(dwg.rect((x, y), (cell, cell), fill=color, rx=4))
        dwg.add(dwg.text(
            f"{h:02d}",
            insert=(x + cell / 2, y + cell + 14),
            fill=c["text"],
            font_size="9",
            text_anchor="middle",
            opacity="0.5",
        ))
        if v > 0:
            dwg.add(dwg.text(
                str(v),
                insert=(x + cell / 2, y + cell / 2 + 3),
                fill="#fff",
                font_size="8",
                text_anchor="middle",
            ))

    dwg.add(dwg.text(
        title,
        insert=(svg_w / 2, 18),
        fill=c["text"],
        font_size="12",
        text_anchor="middle",
        font_weight="bold",
    ))

    return dwg.tostring()


def render_stats_card(
    total_commits: int,
    first_commit: str,
    last_commit: str,
    scheme: str = "github",
    username: str = "developer",
    width: int = 400,
    height: int = 120,
) -> str:
    """Render a simple stats card as SVG."""
    if scheme not in SCHEMES:
        scheme = "github"
    c = SCHEMES[scheme]

    dwg = svgwrite.Drawing(size=(width, height))
    dwg.defs.add(dwg.style("""
        rect { stroke: none }
        text { font-family: -apple-system, BlinkMacSystemFont, sans-serif }
    """))

    dwg.add(dwg.rect((0, 0), (width, height), fill=c["bg"], rx=12))

    # Avatar placeholder
    dwg.add(dwg.circle((50, height / 2), 28, fill=c["accent"], opacity="0.3"))
    dwg.add(dwg.text(
        username[:2].upper(),
        insert=(50, height / 2 + 6),
        fill=c["accent"],
        font_size="16",
        text_anchor="middle",
        font_weight="bold",
    ))

    # Stats
    dwg.add(dwg.text(
        f"{total_commits:,}",
        insert=(100, height / 2 - 8),
        fill=c["text"],
        font_size="22",
        font_weight="bold",
    ))
    dwg.add(dwg.text(
        "commits this year",
        insert=(100, height / 2 + 12),
        fill=c["text"],
        font_size="10",
        opacity="0.6",
    ))

    # Accent line
    dwg.add(dwg.rect((0, height - 4), (width, 4), fill=c["accent"]))

    return dwg.tostring()
