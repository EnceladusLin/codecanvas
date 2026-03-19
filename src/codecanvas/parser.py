"""Git log parser."""
import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from typing import Optional

from git import Repo


def parse_git_log(
    repo_path: str = ".",
    days: int = 365,
    author: Optional[str] = None,
) -> dict:
    """Parse git log and aggregate commits."""
    try:
        repo = Repo(Path(repo_path).resolve(), search_parent_directories=True)
    except Exception as e:
        return {"error": str(e)}

    since = datetime.now() - timedelta(days=days)
    
    commits = []
    for commit in repo.iter_commits(max_count=5000):
        if commit.committed_datetime < since:
            break
        if author and author.lower() not in commit.author.name.lower():
            continue
        commits.append({
            "author": commit.author.name,
            "email": commit.author.email,
            "date": commit.committed_datetime,
            "message": commit.message.strip(),
            "hash": commit.hexsha[:7],
        })

    # Aggregate by day
    by_day = defaultdict(int)
    by_hour = defaultdict(int)
    by_weekday = defaultdict(int)
    files_touched = defaultdict(int)
    
    for c in commits:
        d = c["date"]
        key = d.strftime("%Y-%m-%d")
        by_day[key] += 1
        by_hour[d.hour] += 1
        by_weekday[d.weekday()] += 1
        
        # Count files changed (approximate)
        if commit.stats:
            files_touched[key] += sum(1 for _ in commit.stats.files)

    return {
        "commits": commits,
        "total": len(commits),
        "by_day": dict(by_day),
        "by_hour": dict(by_hour),
        "by_weekday": dict(by_weekday),
        "files_touched": dict(files_touched),
        "first_commit": commits[-1]["date"].isoformat() if commits else None,
        "last_commit": commits[0]["date"].isoformat() if commits else None,
    }
