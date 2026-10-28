"""Fold delivery events into an independently owned stock projection."""

from collections.abc import Iterable, Mapping

from stockroom.events import StockEvent
from stockroom.keys import stock_key


def project_stock(
    initial: Mapping[tuple[str, str], int], events: Iterable[StockEvent]
) -> dict[tuple[str, str], int]:
    """Return stock after processing this delivery batch."""
    result = dict(initial)
    for event in events:
        key = stock_key(event.warehouse, event.sku)
        result[key] = result.get(key, 0) + event.delta
    return result
