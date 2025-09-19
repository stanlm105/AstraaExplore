"""
Launcher for the Messier Log Book CLI tool.

Run this script from the project root for best results.
Provides command-line arguments for personalization and output file location.
"""

import sys
from pathlib import Path
import argparse

# Set project_root to the repo root directory
project_root = Path(__file__).resolve().parent

# Ensure the CLI tool is importable
sys.path.insert(0, str(project_root))

from tools.logbook_generator.cli_logbook_generator import main

def parse_args():
    """
    Parse command-line arguments for the logbook generator.

    Returns:
        argparse.Namespace: Parsed arguments with 'name' and 'output'.
    """
    parser = argparse.ArgumentParser(description="Messier Log Book CLI Launcher")
    parser.add_argument(
        "--name", type=str, default="Bob Smith",
        help="Name for personalization (default: Bob Smith)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output PDF file path (default: output/LogBook_<name>.pdf)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        main(project_root=project_root, name=args.name, output=args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)