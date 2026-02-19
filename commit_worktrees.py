#!/usr/bin/env python3
"""Commit changes in each worktree"""
import subprocess
from pathlib import Path

def commit_worktree_changes(worktree_path, issue_number, description):
    """Commit changes in a worktree"""
    try:
        # Add all changes
        subprocess.run(['git', 'add', '-A'], cwd=worktree_path, capture_output=True, check=True)
        
        # Commit with message
        commit_msg = f"feat: Issue #{issue_number} - {description}"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], cwd=worktree_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Committed Issue #{issue_number}: {description}")
            return True
        else:
            print(f"⚠️  Issue #{issue_number}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error committing Issue #{issue_number}: {e}")
        return False

def main():
    repo_path = Path(__file__).parent
    trees_path = repo_path / ".trees"
    
    issues = [
        (1, "issue-1-5day-forecast", "Add 5-Day Weather Forecast view"),
        (2, "issue-2-search-history", "Add Search History for recent cities"),
        (3, "issue-3-celsius-fahrenheit", "Add Celsius/Fahrenheit toggle with persistence")
    ]
    
    print("📦 Committing changes in all worktrees...\n")
    
    for issue_num, worktree_name, description in issues:
        worktree_path = trees_path / worktree_name
        if worktree_path.exists():
            commit_worktree_changes(worktree_path, issue_num, description)
        else:
            print(f"⚠️  Worktree not found: {worktree_path}")

if __name__ == "__main__":
    main()
