"""CLI for CodeCanvas."""
from pathlib import Path
import click

from codecanvas.parser import parse_git_log
from codecanvas.svg_gen import (
    render_heatmap,
    render_weekly_bar,
    render_hourly_heatmap,
    render_stats_card,
)


@click.command()
@click.option("--repo", default=".", help="Path to git repository")
@click.option("--days", default=365, help="Days of history to analyze")
@click.option("--author", default=None, help="Filter by author name")
@click.option("--scheme", default="github", help="Color scheme")
@click.option("--output", default="./codecanvas-output", help="Output directory")
def main(repo, days, author, scheme, output):
    """Generate SVG coding activity summaries from git history."""
    stats = parse_git_log(repo_path=repo, days=days, author=author)
    if stats.get("error"):
        raise click.ClickException(stats["error"])

    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)

    heatmap = render_heatmap(stats["by_day"], days=days, scheme=scheme)
    weekly = render_weekly_bar(stats["by_weekday"], scheme=scheme)
    hourly = render_hourly_heatmap(stats["by_hour"], scheme=scheme)
    card = render_stats_card(
        total_commits=stats["total"],
        first_commit=stats["first_commit"],
        last_commit=stats["last_commit"],
        scheme=scheme,
        username=author or "developer",
    )

    (out / "heatmap.svg").write_text(heatmap, encoding="utf-8")
    (out / "weekly.svg").write_text(weekly, encoding="utf-8")
    (out / "hourly.svg").write_text(hourly, encoding="utf-8")
    (out / "card.svg").write_text(card, encoding="utf-8")

    click.echo(f"Generated 4 SVG files in {out}")


if __name__ == "__main__":
    main()
