#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
raise SystemExit(subprocess.call([sys.executable, "-m", "unittest", "-v", "test_scoring.py"], cwd=HERE))
