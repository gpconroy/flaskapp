#!/usr/bin/env python3
"""Helper script to create git worktrees for issues"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running: {cmd}")
            print(f"stderr: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception running command: {e}")
        return False

def create_worktrees():
    """Create worktrees for each open issue"""
    repo_path = Path(__file__).parent
    trees_path = repo_path / ".trees"
    
    # Issue mapping: {issue_number: (branch_name, worktree_name)}
    issues = {
        1: ("feature/issue-1-5day-forecast", "issue-1-5day-forecast"),
        2: ("feature/issue-2-search-history", "issue-2-search-history"),
        3: ("feature/issue-3-celsius-fahrenheit", "issue-3-celsius-fahrenheit")
    }
    
    # Ensure .trees directory exists
    trees_path.mkdir(exist_ok=True)
    print(f"Using trees directory: {trees_path}")
    
    for issue_num, (branch_name, worktree_name) in issues.items():
        worktree_path = trees_path / worktree_name
        
        # Check if worktree already exists
        if worktree_path.exists():
            print(f"⚠️  Worktree {worktree_name} already exists at {worktree_path}")
            continue
        
        # Create branch for this issue
        print(f"\n🌿 Creating branch {branch_name}...")
        cmd = f'git branch {branch_name}'
        if not run_command(cmd, cwd=repo_path):
            print(f"Branch {branch_name} may already exist or failed to create")
        
        # Create worktree
        print(f"📦 Creating worktree for {worktree_name}...")
        cmd = f'git worktree add "{worktree_path}" {branch_name}'
        if not run_command(cmd, cwd=repo_path):
            print(f"Failed to create worktree for {worktree_name}")
            continue
        
        print(f"✅ Created worktree: {worktree_path}")

if __name__ == "__main__":
    create_worktrees()
