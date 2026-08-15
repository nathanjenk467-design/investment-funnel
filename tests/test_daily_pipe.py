#!/usr/bin/env python3
"""Unittest wrapper around the daily pipe engine."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import daily_pipe  # noqa: E402


class DailyPipeSelfTest(unittest.TestCase):
    def test_self_test(self):
        self.assertEqual(daily_pipe.main(["self-test"]), 0)

    def test_run_now_pass(self):
        self.assertEqual(daily_pipe.main(["run-now", "--work", str(ROOT / "runs" / "test-run-now")]), 0)

    def test_run_now_frozen_is_a_correct_fail(self):
        self.assertEqual(
            daily_pipe.main(["run-now", "--frozen", "--work", str(ROOT / "runs" / "test-frozen")]),
            0,
        )


if __name__ == "__main__":
    unittest.main()
