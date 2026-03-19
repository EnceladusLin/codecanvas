# CodeCanvas

Generate beautiful SVG coding activity summaries from git history.

## What it does

CodeCanvas turns raw git commits into shareable developer visuals:
- weekly activity charts
- repo heatmaps
- contributor streak cards
- SVG summaries for README profiles

## Why it can get stars

- visual output spreads better than CLI-only tools
- useful for README/profile pages
- works with plain git history, no SaaS required
- easy to screenshot and post

## MVP

- parse git log
- aggregate commits by day/week/hour
- export SVG dashboard
- export PNG via optional browser render
- CLI + config file

## Stack

- Python
- click
- svgwrite
- gitpython

## Planned launch angle

"Your git history, turned into beautiful SVG dashboards."
