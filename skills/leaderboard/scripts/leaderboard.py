#!/usr/bin/env python3
"""Thin wrapper -- delegates to the main leaderboard script."""
import sys
import os
import importlib.util

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
sys.argv[0] = 'leaderboard.py'
sys.path.insert(0, WORKSPACE)

spec = importlib.util.spec_from_file_location(
    "leaderboard", os.path.join(WORKSPACE, "leaderboard.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
