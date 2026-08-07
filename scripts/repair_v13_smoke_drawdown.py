#!/usr/bin/env python3
import argparse
import json
import math
import sqlite3
from dataclasses import dataclass
from pathlib import Path


SYNTHETIC_SMOKE_PRICE = 51_595.0
EXPECTED_LANES = {f"lane_{number}" for number in range(1, 6)}


@dataclass(frozen=True)
class Repair:
    lane_id: str
    stored_drawdown_pct: float
    synthetic_drawdown_pct: float
    corrected_drawdown_pct: float


def inspect_repairs(connection: sqlite3.Connection) -> list[Repair]:
    connection.row_factory = sqlite3.Row
    portfolios = connection.execute(
        "SELECT lane_id, cash, equity, peak_equity, max_drawdown_pct FROM portfolios"
    ).fetchall()
    if {row["lane_id"] for row in portfolios} != EXPECTED_LANES:
        raise ValueError("expected exactly lane_1 through lane_5")

    repairs = []
    for portfolio in portfolios:
        lane_id = portfolio["lane_id"]
        trades = connection.execute(
            """
            SELECT symbol, action, quantity, reason_codes
            FROM arena_events
            WHERE lane_id = ? AND quantity > 0
            ORDER BY id
            """,
            (lane_id,),
        ).fetchall()
        if len(trades) != 1:
            raise ValueError(f"{lane_id} must have exactly one filled trade")
        trade = trades[0]
        reasons = json.loads(trade["reason_codes"])
        if (
            trade["symbol"] != "BTC/USDT"
            or trade["action"] != "BUY"
            or reasons != ["BOOTSTRAP_PROBE"]
        ):
            raise ValueError(f"{lane_id} trade does not match the bootstrap signature")

        positions = connection.execute(
            "SELECT quantity FROM positions WHERE lane_id = ? AND quantity > 0",
            (lane_id,),
        ).fetchall()
        if len(positions) != 1:
            raise ValueError(f"{lane_id} must have exactly one open position")

        peak = float(portfolio["peak_equity"])
        synthetic_equity = float(portfolio["cash"]) + float(
            positions[0]["quantity"]
        ) * SYNTHETIC_SMOKE_PRICE
        synthetic_drawdown = (peak - synthetic_equity) / peak * 100 if peak else 0
        stored_drawdown = float(portfolio["max_drawdown_pct"])
        corrected_drawdown = (
            (peak - float(portfolio["equity"])) / peak * 100 if peak else 0
        )
        if not math.isclose(stored_drawdown, synthetic_drawdown, abs_tol=0.00001):
            raise ValueError(
                f"{lane_id} max drawdown does not match the v1.3 smoke signature"
            )
        if corrected_drawdown >= stored_drawdown:
            raise ValueError(f"{lane_id} current drawdown is not lower than the corrupted value")
        repairs.append(
            Repair(
                lane_id=lane_id,
                stored_drawdown_pct=stored_drawdown,
                synthetic_drawdown_pct=synthetic_drawdown,
                corrected_drawdown_pct=max(0.0, corrected_drawdown),
            )
        )
    return repairs


def repair_database(path: str, *, apply: bool = False) -> list[Repair]:
    connection = sqlite3.connect(path)
    try:
        repairs = inspect_repairs(connection)
        if apply:
            with connection:
                for repair in repairs:
                    connection.execute(
                        "UPDATE portfolios SET max_drawdown_pct = ? WHERE lane_id = ?",
                        (repair.corrected_drawdown_pct, repair.lane_id),
                    )
        return repairs
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair the exact max-drawdown signature left by the v1.3 smoke price."
    )
    parser.add_argument("--database", default="/data/arena.db")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not Path(args.database).is_file():
        parser.error(f"database not found: {args.database}")
    repairs = repair_database(args.database, apply=args.apply)
    mode = "APPLIED" if args.apply else "DRY-RUN"
    for repair in repairs:
        print(
            f"{mode} {repair.lane_id}: "
            f"{repair.stored_drawdown_pct:.9f}% -> "
            f"{repair.corrected_drawdown_pct:.9f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
