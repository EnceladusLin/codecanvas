# CodeCanvas

Generate beautiful SVG coding activity summaries from git history.

## What it does

CodeCanvas turns raw git commits into shareable developer visuals:
- weekly activity charts
- repo heatmaps
- contributor streak cards
- SVG summaries for README profiles

## Why this has star potential

Most git analytics tools stop at numbers. CodeCanvas focuses on **presentation**: images you can actually embed in a README, post on X, or drop into a personal site.

That makes it naturally more shareable than a plain terminal report.

## Example outputs

Generated example assets live in `examples/output/`.

- `heatmap.svg`
- `card.svg`

## CLI

```bash
codecanvas --repo . --output ./codecanvas-output
```

This generates:
- `heatmap.svg`
- `weekly.svg`
- `hourly.svg`
- `card.svg`

## MVP

- parse git log
- aggregate commits by day/week/hour
- export SVG dashboard
- export PNG later via optional renderer
- CLI + config file

## Stack

- Python
- click
- svgwrite
- gitpython

## Launch positioning

**Your git history, turned into beautiful SVG dashboards.**

## Next build targets

- contributor comparison cards
- repository language bands
- profile-ready dark/light themes
- markdown embed snippets
- screenshot assets for launch posts
