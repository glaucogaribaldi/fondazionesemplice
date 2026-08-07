import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "drawdown_repair", ROOT / "scripts" / "repair_v13_smoke_drawdown.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
repair_database = MODULE.repair_database


class DrawdownRepairTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.database = Path(self.tempdir.name) / "arena.db"
        connection = sqlite3.connect(self.database)
        connection.executescript(
            """
            CREATE TABLE portfolios (
                lane_id TEXT PRIMARY KEY,
                cash REAL,
                equity REAL,
                peak_equity REAL,
                max_drawdown_pct REAL
            );
            CREATE TABLE positions (lane_id TEXT, quantity REAL);
            CREATE TABLE arena_events (
                id INTEGER PRIMARY KEY,
                lane_id TEXT,
                symbol TEXT,
                action TEXT,
                quantity REAL,
                reason_codes TEXT
            );
            """
        )
        for number in range(1, 6):
            lane_id = f"lane_{number}"
            cash = 306.8814
            quantity = 0.00004787265400743346
            equity = cash + quantity * 64_891.56
            synthetic_equity = cash + quantity * MODULE.SYNTHETIC_SMOKE_PRICE
            corrupted_drawdown = (310 - synthetic_equity) / 310 * 100
            connection.execute(
                "INSERT INTO portfolios VALUES (?, ?, ?, ?, ?)",
                (lane_id, cash, equity, 310, corrupted_drawdown),
            )
            connection.execute("INSERT INTO positions VALUES (?, ?)", (lane_id, quantity))
            connection.execute(
                "INSERT INTO arena_events VALUES (?, ?, ?, ?, ?, ?)",
                (
                    number,
                    lane_id,
                    "BTC/USDT",
                    "BUY",
                    quantity,
                    json.dumps(["BOOTSTRAP_PROBE"]),
                ),
            )
        connection.commit()
        connection.close()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_dry_run_does_not_change_database(self):
        repairs = repair_database(str(self.database))
        self.assertEqual(len(repairs), 5)
        connection = sqlite3.connect(self.database)
        stored = connection.execute(
            "SELECT max_drawdown_pct FROM portfolios WHERE lane_id = 'lane_1'"
        ).fetchone()[0]
        connection.close()
        self.assertAlmostEqual(stored, repairs[0].stored_drawdown_pct)

    def test_apply_repairs_only_max_drawdown(self):
        repairs = repair_database(str(self.database), apply=True)
        connection = sqlite3.connect(self.database)
        row = connection.execute(
            "SELECT cash, equity, max_drawdown_pct FROM portfolios WHERE lane_id = 'lane_1'"
        ).fetchone()
        trade_count = connection.execute("SELECT COUNT(*) FROM arena_events").fetchone()[0]
        connection.close()
        self.assertEqual(row[0], 306.8814)
        self.assertAlmostEqual(row[1], 309.987931, places=5)
        self.assertAlmostEqual(row[2], repairs[0].corrected_drawdown_pct)
        self.assertEqual(trade_count, 5)

    def test_refuses_non_bootstrap_history(self):
        connection = sqlite3.connect(self.database)
        connection.execute(
            "INSERT INTO arena_events VALUES (?, ?, ?, ?, ?, ?)",
            (10, "lane_1", "BTC/USDT", "BUY", 0.1, json.dumps(["KRONOS_UP"])),
        )
        connection.commit()
        connection.close()
        with self.assertRaisesRegex(ValueError, "exactly one filled trade"):
            repair_database(str(self.database), apply=True)


if __name__ == "__main__":
    unittest.main()
