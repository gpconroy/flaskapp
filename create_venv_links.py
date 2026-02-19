#!/usr/bin/env python3
"""Create junction points for .venv in each worktree"""
import os
import subprocess
from pathlib import Path

def create_venv_junctions():
    repo_path = Path(__file__).parent
    venv_path = repo_path / ".venv"
    trees_path = repo_path / ".trees"
    
    if not venv_path.exists():
        print(f"❌ .venv not found at {venv_path}")
        return False
    
    worktrees = [
        "issue-1-5day-forecast",
        "issue-2-search-history",
        "issue-3-celsius-fahrenheit"
    ]
    
    for worktree_name in worktrees:
        worktree_path = trees_path / worktree_name
        venv_link_path = worktree_path / ".venv"
        
        if venv_link_path.exists() or venv_link_path.is_symlink():
            print(f"⚠️  .venv already exists at {venv_link_path}")
            continue
        
        try:
            # Use Windows mklink through cmd.exe
            cmd = f'mklink /J "{venv_link_path}" "{venv_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Created junction: {venv_link_path} -> {venv_path}")
            else:
                print(f"❌ Failed to create junction for {worktree_name}")
                print(f"   Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Exception creating junction: {e}")
    
    return True

if __name__ == "__main__":
    create_venv_junctions()
