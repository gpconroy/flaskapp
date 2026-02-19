#!/usr/bin/env python3
"""Clean up git worktrees"""
import subprocess
import shutil
from pathlib import Path

def remove_worktree(repo_path, worktree_name):
    """Remove a worktree"""
    try:
        # Remove worktree using git
        result = subprocess.run(['git', 'worktree', 'remove', '-f', worktree_name], 
                              cwd=repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Removed worktree: {worktree_name}")
            return True
        else:
            print(f"⚠️  Could not remove worktree {worktree_name}: {result.stderr}")
            # Try manual removal
            return remove_worktree_manual(worktree_name)
    except Exception as e:
        print(f"❌ Error removing worktree {worktree_name}: {e}")
        return False

def remove_worktree_manual(worktree_path):
    """Manually remove worktree directory"""
    try:
        if Path(worktree_path).exists():
            shutil.rmtree(worktree_path)
            print(f"✅ Manually removed directory: {worktree_path}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error manually removing {worktree_path}: {e}")
        return False

def main():
    repo_path = Path(__file__).parent
    trees_path = repo_path / ".trees"
    
    worktrees = [
        "issue-1-5day-forecast",
        "issue-2-search-history",
        "issue-3-celsius-fahrenheit"
    ]
    
    print("🧹 Cleaning up worktrees...\n")
    
    for worktree_name in worktrees:
        worktree_full_path = trees_path / worktree_name
        remove_worktree(repo_path, str(worktree_full_path))
    
    # Remove .trees directory if empty
    if trees_path.exists() and not any(trees_path.iterdir()):
        shutil.rmtree(trees_path)
        print(f"✅ Removed empty .trees directory")
    
    print("\n✅ Cleanup complete!")

if __name__ == "__main__":
    main()
