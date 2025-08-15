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

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'      # Purple
    OKBLUE = '\033[94m'      # Blue
    OKCYAN = '\033[96m'      # Cyan
    OKGREEN = '\033[92m'     # Green
    WARNING = '\033[93m'     # Yellow
    FAIL = '\033[91m'        # Red
    ENDC = '\033[0m'         # Reset
    BOLD = '\033[1m'         # Bold
    UNDERLINE = '\033[4m'    # Underline

def colorize(text, color):
    """Apply color to text."""
    return f"{color}{text}{Colors.ENDC}"

def print_header(text):
    """Print header text in purple."""
    print(colorize(f"\n{text}", Colors.HEADER))
    print(colorize("=" * len(text), Colors.HEADER))

def print_success(text):
    """Print success text in green."""
    print(colorize(f"✓ {text}", Colors.OKGREEN))

def print_error(text):
    """Print error text in red."""
    print(colorize(f"✗ {text}", Colors.FAIL))

def print_warning(text):
    """Print warning text in yellow."""
    print(colorize(f"⚠ {text}", Colors.WARNING))

def print_info(text):
    """Print info text in cyan."""
    print(colorize(f"{text}", Colors.OKCYAN))

def print_prompt(text):
    """Print prompt text in blue."""
    print(colorize(text, Colors.OKBLUE))


def load_environment():
    """Load environment variables from .env file."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print_error(".env file not found!")
        print_info("Please copy .env.example to .env and set a valid BASE_DIR path.")
        sys.exit(1)
    
    config = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    # Remove quotes if present
                    value = value.strip().strip('"\'')
                    config[key] = value
        
        # Check required variables
        if 'BASE_DIR' not in config or not config['BASE_DIR']:
            print_error("BASE_DIR not found or empty in .env file!")
            print_info("Please set a valid BASE_DIR path in your .env file.")
            sys.exit(1)
            
        if 'FIRST_NAME' not in config or not config['FIRST_NAME']:
            print_error("FIRST_NAME not found or empty in .env file!")
            print_info("Please set your first name in your .env file.")
            sys.exit(1)
            
        if 'LAST_NAME' not in config or not config['LAST_NAME']:
            print_error("LAST_NAME not found or empty in .env file!")
            print_info("Please set your last name in your .env file.")
            sys.exit(1)
        
        return Path(config['BASE_DIR']), config['FIRST_NAME'], config['LAST_NAME']
        
    except Exception as e:
        print_error(f"Error reading .env file: {e}")
        print_info("Please ensure your .env file is properly formatted.")
        sys.exit(1)


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
        print_error("Compiled resume (resume.pdf) not found!")
        print_info("Please compile your resume first.")
        return False
    return True


def create_directory(base_path, dir_name):
    """Create the target directory."""
    target_path = base_path / dir_name
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {target_path}")
        return target_path
    except Exception as e:
        print_error(f"Error creating directory: {e}")
        return None


def copy_resume(target_dir, first_name, last_name):
    """Copy the resume to the target directory with the new name."""
    source_file = Path("resume.pdf")
    target_file = target_dir / f"{first_name}_{last_name}_resume.pdf"
    
    try:
        shutil.copy2(source_file, target_file)
        print_success(f"Resume copied to: {target_file}")
        return True
    except Exception as e:
        print_error(f"Error copying resume: {e}")
        return False


def main():
    """Main function to handle resume export."""
    print_header("Resume Export Script")
    
    # Check if compiled resume exists
    if not check_resume_exists():
        sys.exit(1)
    
    # Load environment configuration
    try:
        OUTPUT_BASE, FIRST_NAME, LAST_NAME = load_environment()
    except Exception as e:
        print_error(f"Error loading environment: {e}")
        print_info("Please ensure .env file exists and contains valid BASE_DIR, FIRST_NAME, and LAST_NAME.")
        sys.exit(1)
    
    # Check if base directory exists
    if not OUTPUT_BASE.exists():
        print_error(f"Base directory does not exist: {OUTPUT_BASE}")
        print_info("Please check the BASE_DIR path in your .env file and ensure it exists.")
        sys.exit(1)
    
    # Prompt for directory name
    print_info(f"Base output directory: {OUTPUT_BASE}")
    default_name = get_default_directory_name()
    print_prompt(f"Enter a subdirectory name (press Enter for '{default_name}'): ")
    user_input = input().strip()
    
    if not user_input:
        dir_name = get_default_directory_name()
        print_info(f"Using default directory name: {dir_name}")
    else:
        dir_name = user_input
    
    # Create the target directory
    target_dir = create_directory(OUTPUT_BASE, dir_name)
    if not target_dir:
        sys.exit(1)
    
    # Copy the resume
    if copy_resume(target_dir, FIRST_NAME, LAST_NAME):
        print_success(f"\nResume successfully exported to: {target_dir}")
    else:
        print_error("\nFailed to export resume.")
        sys.exit(1)


if __name__ == "__main__":
    main()
