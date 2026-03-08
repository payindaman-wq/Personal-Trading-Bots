#!/usr/bin/env python3
"""Thin wrapper -- delegates to the main leaderboard script."""
import sys
import os
sys.argv[0] = 'leaderboard.py'
sys.path.insert(0, '/root/.openclaw/workspace')
# Re-execute the main script in workspace
exec(open('/root/.openclaw/workspace/leaderboard.py').read())
