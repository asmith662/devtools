"""Domain inputs supplied by the ingestion boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StockEvent:
    warehouse: str
    sku: str
    event_id: str
    delta: int

    def __post_init__(self):
        if not self.warehouse.strip() or not self.sku.strip() or not self.event_id:
            raise ValueError("event identifiers cannot be empty")
        if type(self.delta) is not int:
            raise ValueError("delta must be an integer")
