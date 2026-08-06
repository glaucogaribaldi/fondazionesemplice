from datetime import UTC, datetime


def normalize_candles(
    rows: list[list[float]], now: int, granularity: int, limit: int
) -> list[dict]:
    closed_before = now - (now % granularity)
    candles = []
    for timestamp, low, high, opening, close, volume in rows:
        if int(timestamp) >= closed_before:
            continue
        candles.append(
            {
                "timestamp": datetime.fromtimestamp(timestamp, UTC).isoformat(),
                "open": opening,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
            }
        )
    candles.sort(key=lambda item: item["timestamp"])
    return candles[-limit:]


def product_to_symbol(product: str) -> str:
    parts = product.split("-")
    if len(parts) != 2 or not all(parts):
        raise ValueError(f"invalid Coinbase product: {product}")
    return "/".join(parts)
