#!/usr/bin/env python3
"""
Entry point for jira-generator.

Usage:
    python run.py --help
    python run.py --all
    python run.py --projects --hierarchy
"""
import sys
from jira_generator.main import main

if __name__ == "__main__":
    sys.exit(main())
