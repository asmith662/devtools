"""Fold delivery events into an independently owned stock projection."""

from collections.abc import Iterable, Mapping

from stockroom.events import StockEvent
from stockroom.keys import stock_key


def project_stock(
    initial: Mapping[tuple[str, str], int], events: Iterable[StockEvent]
) -> dict[tuple[str, str], int]:
    """Return stock after processing this delivery batch.

    A delivery identity is (canonical warehouse, exact opaque event_id).
    An identical repeated delivery contributes its delta only once.
    The same identity with a different canonical SKU or delta conflicts.
    """
    result = dict(initial)
    seen: dict[tuple[str, str], tuple[tuple[str, str], int]] = {}
    for event in events:
        key = stock_key(event.warehouse, event.sku)
        identity = (key[0], event.event_id)
        if identity in seen:
            prior_key, prior_delta = seen[identity]
            if key != prior_key or event.delta != prior_delta:
                raise ValueError(
                    "conflicting delivery for event_id "
                    f"{event.event_id!r} in warehouse {key[0]!r}"
                )
        else:
            seen[identity] = (key, event.delta)
            result[key] = result.get(key, 0) + event.delta
    return result
