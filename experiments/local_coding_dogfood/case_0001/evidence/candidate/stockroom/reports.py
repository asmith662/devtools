"""Human-facing reporting, independently maintained from delivery projection."""


def format_stock_rows(balances):
    return [
        f"{warehouse}/{sku}: {count:+d}"
        for (warehouse, sku), count in sorted(balances.items())
    ]
