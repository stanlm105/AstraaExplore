"""
Launcher for the Messier Log Book CLI tool.
Run this from the project root for best results.
"""

import sys
from pathlib import Path
import argparse

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from tools.logbook_generator.cli_logbook_generator import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Messier Log Book CLI Launcher")
    parser.add_argument("--name", type=str, default="Bob Smith", help="Name for personalization")
    parser.add_argument("--output", type=str, default=None, help="Output PDF file path")
    try:
        args = parser.parse_args()
    except SystemExit as e:
        print("Error: Invalid or missing arguments. Use --help for usage information.")
        sys.exit(e.code)
    main(project_root=project_root, name=args.name, output=args.output)