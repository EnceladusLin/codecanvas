#!/usr/bin/env python3
"""Generate sample SVG outputs without external dependencies."""
from pathlib import Path
from datetime import datetime, timedelta


def minimal_heatmap():
    """Generate a simple heatmap SVG."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 200">
  <rect width="100%" height="100%" fill="#0d1117"/>
  <text x="20" y="25" fill="#c9d1d9" font-family="sans-serif" font-size="16" font-weight="bold">Coding Activity (example)</text>
  <rect x="30" y="50" width="12" height="12" fill="#161b22" rx="2"/>
  <rect x="46" y="50" width="12" height="12" fill="#0e4429" rx="2"/>
  <rect x="62" y="50" width="12" height="12" fill="#006d32" rx="2"/>
  <rect x="78" y="50" width="12" height="12" fill="#26a641" rx="2"/>
  <rect x="94" y="50" width="12" height="12" fill="#39d353" rx="2"/>
  <text x="30" y="85" fill="#8b949e" font-family="monospace" font-size="10">Less</text>
  <text x="110" y="85" fill="#8b949e" font-family="monospace" font-size="10">More</text>
  <text x="30" y="120" fill="#58a6ff" font-family="sans-serif" font-size="12">Run: codecanvas --repo . --output ./output</text>
  <text x="30" y="145" fill="#8b949e" font-family="sans-serif" font-size="11">to generate real visualizations from your git history</text>
</svg>'''
    return svg


def minimal_card():
    """Generate a stats card SVG."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120">
  <rect width="100%" height="100%" fill="#0d1117" rx="12"/>
  <circle cx="50" cy="60" r="28" fill="#58a6ff" opacity="0.3"/>
  <text x="50" y="66" fill="#58a6ff" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle">EN</text>
  <text x="100" y="50" fill="#c9d1d9" font-family="sans-serif" font-size="22" font-weight="bold">1,284</text>
  <text x="100" y="70" fill="#8b949e" font-family="sans-serif" font-size="10">commits this year</text>
  <rect x="0" y="116" width="400" height="4" fill="#58a6ff"/>
</svg>'''
    return svg


if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parent
    out = ROOT / 'output'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'heatmap.svg').write_text(minimal_heatmap())
    (out / 'card.svg').write_text(minimal_card())
    print('Generated sample SVGs in examples/output/')
