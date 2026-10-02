#!/usr/bin/env python3
"""One local entry point for reconciliation, delivery and browser acceptance.

Usage: python3 scripts/card_batch.py {reconcile|delivery|browser|context|workflow} [tool options]
Each command is read-only with respect to cards. There is no install/publish action.
"""
from pathlib import Path
import subprocess
import sys


def main():
    scripts = Path(__file__).resolve().parent
    commands = {
        'reconcile': [sys.executable, str(scripts/'reconcile_card_resume.py')],
        'delivery': [sys.executable, str(scripts/'check_card_delivery.py')],
        'browser': ['node', str(scripts/'check_card_browser.cjs')],
        'workflow': [sys.executable, str(scripts/'card_workflow.py')],
        'context': [sys.executable, str(scripts/'card_context.py')],
    }
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        return 2
    return subprocess.call(commands[sys.argv[1]] + sys.argv[2:], cwd=scripts.parent)


if __name__ == '__main__':
    raise SystemExit(main())
