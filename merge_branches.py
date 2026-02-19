#!/usr/bin/env python3
"""Merge all feature branches into master"""
import subprocess
from pathlib import Path

def merge_branch(repo_path, branch_name, issue_num):
    """Merge a branch into master"""
    try:
        # Make sure we're on master
        subprocess.run(['git', 'checkout', 'master'], cwd=repo_path, capture_output=True, check=True)
        
        # Merge the branch
        result = subprocess.run(['git', 'merge', branch_name], cwd=repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Merged Issue #{issue_num} ({branch_name}) into master")
            return True
        else:
            # Check if it's a conflict error
            if 'conflict' in result.stdout.lower() or 'conflict' in result.stderr.lower():
                print(f"⚠️  Conflict detected while merging Issue #{issue_num}")
                print(f"   Output: {result.stderr}")
                return None  # Return None to indicate conflict
            else:
                print(f"❌ Failed to merge Issue #{issue_num}: {result.stderr}")
                return False
    except Exception as e:
        print(f"❌ Error merging Issue #{issue_num}: {e}")
        return False

def main():
    repo_path = Path(__file__).parent
    
    issues = [
        (1, "feature/issue-1-5day-forecast"),
        (2, "feature/issue-2-search-history"),
        (3, "feature/issue-3-celsius-fahrenheit")
    ]
    
    print("🔀 Merging all feature branches into master...\n")
    
    conflicts = []
    
    for issue_num, branch_name in issues:
        result = merge_branch(repo_path, branch_name, issue_num)
        if result is None:
            conflicts.append((issue_num, branch_name))
    
    if conflicts:
        print(f"\n⚠️  {len(conflicts)} branch(es) had conflicts:")
        for issue_num, branch_name in conflicts:
            print(f"   - Issue #{issue_num}: {branch_name}")
        print("\n🔧 Attempting to resolve conflicts with knowledge-based strategy...")
        resolve_conflicts(repo_path, conflicts)
    else:
        print("\n✅ All branches merged successfully!")

def resolve_conflicts(repo_path, conflicts):
    """Attempt to resolve conflicts using knowledge of changes"""
    try:
        # Get status to see what files have conflicts
        result = subprocess.run(['git', 'status'], cwd=repo_path, capture_output=True, text=True)
        print("\nCurrent git status:")
        print(result.stdout)
        
        # Attempt to resolve by accepting incoming changes one by one
        for issue_num, branch_name in conflicts:
            print(f"\nHandling conflicts for Issue #{issue_num}...")
            
            # Get conflicted files
            result = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=U'], cwd=repo_path, capture_output=True, text=True)
            conflicted_files = result.stdout.strip().split('\n')
            
            if conflicted_files and conflicted_files[0]:
                print(f"  Conflicted files: {', '.join(conflicted_files)}")
                
                # For this task, we'll use a merge strategy that prefers incoming changes
                for file in conflicted_files:
                    # Use their version (incoming from branch)
                    subprocess.run(['git', 'checkout', '--theirs', file], cwd=repo_path, capture_output=True)
                    subprocess.run(['git', 'add', file], cwd=repo_path, capture_output=True)
                
                # Complete the merge
                result = subprocess.run(['git', 'commit', '-m', f'Merge {branch_name} resolving conflicts'], 
                                      cwd=repo_path, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"  ✅ Resolved conflicts and completed merge for Issue #{issue_num}")
                else:
                    print(f"  ⚠️  Could not complete merge: {result.stderr}")
    except Exception as e:
        print(f"❌ Error resolving conflicts: {e}")

if __name__ == "__main__":
    main()
