#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
economy_trends — wrapper that delegates to daily_economy.main()
This lets the existing LaunchAgent keep calling economy_trends.py while
running the implemented daily_economy script.
"""

from pathlib import Path
import sys

# Ensure project dir is on sys.path
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

try:
    from daily_economy import main as daily_main
except Exception as e:
    print(f"Failed to import daily_economy: {e}")
    raise

if __name__ == '__main__':
    daily_main()
