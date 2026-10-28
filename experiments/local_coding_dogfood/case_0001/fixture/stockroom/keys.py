"""Canonical resource keys; event IDs deliberately have no normalization."""


def stock_key(warehouse: str, sku: str) -> tuple[str, str]:
    return warehouse.strip().casefold(), sku.strip().upper()
