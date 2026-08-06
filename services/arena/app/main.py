import asyncio
import os
from pathlib import Path

import httpx
import yaml
from fastapi import FastAPI, HTTPException
from prometheus_client import Gauge, make_asgi_app


app = FastAPI(title="Fondazione Arena", version="0.1.0")
app.mount("/metrics", make_asgi_app())
EQUITY = Gauge("foundation_lane_equity", "Paper equity", ["lane"])
INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "310"))
PORTFOLIOS: dict[str, dict[str, float]] = {}


def lane_ids() -> list[str]:
    with Path("/app/config/strategies.yml").open(encoding="utf-8") as handle:
        return list(yaml.safe_load(handle)["lanes"])


@app.on_event("startup")
async def initialize() -> None:
    for lane_id in lane_ids():
        PORTFOLIOS[lane_id] = {
            "initial_capital": INITIAL_CAPITAL,
            "cash": INITIAL_CAPITAL,
            "equity": INITIAL_CAPITAL,
            "realized_pnl": 0,
            "unrealized_pnl": 0,
            "fees": 0,
            "max_drawdown_pct": 0,
        }
        EQUITY.labels(lane_id).set(INITIAL_CAPITAL)


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok", "lanes": len(PORTFOLIOS)}


@app.get("/v1/ranking")
async def ranking() -> list[dict]:
    ordered = sorted(PORTFOLIOS.items(), key=lambda item: item[1]["equity"], reverse=True)
    return [
        {"rank": rank, "lane_id": lane_id, **portfolio}
        for rank, (lane_id, portfolio) in enumerate(ordered, start=1)
    ]


@app.post("/v1/evaluate")
async def evaluate(snapshot: dict) -> dict:
    required = {"request_id", "mode", "symbol", "timeframe", "market"}
    if missing := required - snapshot.keys():
        raise HTTPException(status_code=422, detail=f"missing fields: {sorted(missing)}")

    async def call_lane(client: httpx.AsyncClient, lane_id: str) -> dict:
        payload = dict(snapshot)
        payload["request_id"] = f"{snapshot['request_id']}-{lane_id}"
        payload["lane_id"] = lane_id
        payload["portfolio"] = {
            "equity": PORTFOLIOS[lane_id]["equity"],
            "cash": PORTFOLIOS[lane_id]["cash"],
            "daily_pnl_pct": 0,
            "open_positions": 0,
            "current_position_pct": 0,
            "last_trade_at": None,
        }
        response = await client.post(
            f"{os.environ['DECISION_URL']}/v1/decision",
            json=payload,
            headers={"X-API-Key": os.environ["DECISION_API_KEY"]},
        )
        response.raise_for_status()
        return response.json()

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            decisions = await asyncio.gather(*(call_lane(client, lane) for lane in PORTFOLIOS))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="decision service unavailable") from exc
    return {"request_id": snapshot["request_id"], "decisions": decisions}
