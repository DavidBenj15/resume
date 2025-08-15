#!/usr/bin/env python3
"""
Resume Export Script
Prompts user for directory name and exports the compiled resume to the specified location.
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def get_git_branch():
    """Get the current git branch name."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_default_directory_name():
    """Generate default directory name: <branch> <mm-dd-yy>."""
    branch = get_git_branch()
    date_str = datetime.now().strftime("%m-%d-%y")
    return f"{branch} {date_str}"


def check_resume_exists():
    """Check if the compiled resume (resume.pdf) exists."""
    resume_path = Path("resume.pdf")
    if not resume_path.exists():
        print("❌ Error: Compiled resume (resume.pdf) not found!")
        print("Please compile your resume first.")
        return False
    return True


def create_directory(base_path, dir_name):
    """Create the target directory."""
    target_path = base_path / dir_name
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {target_path}")
        return target_path
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None


def copy_resume(target_dir):
    """Copy the resume to the target directory with the new name."""
    source_file = Path("resume.pdf")
    target_file = target_dir / "David_Benjamin_resume.pdf"
    
    try:
        shutil.copy2(source_file, target_file)
        print(f"✅ Resume copied to: {target_file}")
        return True
    except Exception as e:
        print(f"❌ Error copying resume: {e}")
        return False


def main():
    """Main function to handle resume export."""
    print("Resume Export Script")
    print("=" * 40)
    
    # Check if compiled resume exists
    if not check_resume_exists():
        sys.exit(1)
    
    # Set output base directory
    OUTPUT_BASE = Path("/mnt/c/Users/david/OneDrive/School/Junior/Application stuff")
    
    # Check if base directory exists
    if not OUTPUT_BASE.exists():
        print(f"❌ Error: Base directory does not exist: {OUTPUT_BASE}")
        print("Please check the path and ensure it exists.")
        sys.exit(1)
    
    # Prompt for directory name
    print(f"\nBase output directory: {OUTPUT_BASE}")
    default_name = get_default_directory_name()
    print(f"Enter a subdirectory name (or press Enter for default: {default_name}):")
    
    user_input = input("Directory name: ").strip()
    
    if not user_input:
        dir_name = get_default_directory_name()
        print(f"Using default directory name: {dir_name}")
    else:
        dir_name = user_input
    
    # Create the target directory
    target_dir = create_directory(OUTPUT_BASE, dir_name)
    if not target_dir:
        sys.exit(1)
    
    # Copy the resume
    if copy_resume(target_dir):
        print(f"\n🎉 Resume successfully exported to: {target_dir}")
    else:
        print("\n❌ Failed to export resume.")
        sys.exit(1)


if __name__ == "__main__":
    main()
