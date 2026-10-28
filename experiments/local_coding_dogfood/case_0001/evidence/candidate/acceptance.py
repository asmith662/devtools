"""Frozen focused acceptance. This file is outside model read/edit scope."""

import unittest

from stockroom.events import StockEvent as E
from stockroom.projection import project_stock


class Acceptance(unittest.TestCase):
    def test_canonical_repeated_delivery(self):
        initial = {("north", "BOLT"): 5, ("south", "NUT"): 8}
        events = [E(" North ", "bolt", "r1", 3), E("NORTH", " BOLT ", "r1", 3)]
        self.assertEqual(
            project_stock(initial, events), {("north", "BOLT"): 8, ("south", "NUT"): 8}
        )
        self.assertEqual(initial, {("north", "BOLT"): 5, ("south", "NUT"): 8})

    def test_same_id_in_distinct_warehouses(self):
        self.assertEqual(
            project_stock({}, [E("N", "a", "r", 2), E("S", "a", "r", 4)]),
            {("n", "A"): 2, ("s", "A"): 4},
        )

    def test_quantity_conflict(self):
        initial = {("n", "A"): 4}
        with self.assertRaises(ValueError):
            project_stock(initial, [E("N", "a", "r", 2), E(" n ", "A", "r", 3)])
        self.assertEqual(initial, {("n", "A"): 4})

    def test_sku_conflict(self):
        with self.assertRaises(ValueError):
            project_stock({}, [E("N", "a", "r", 2), E("N", "b", "r", 2)])

    def test_generator_negative_and_zero(self):
        events = (e for e in [E("N", "a", "one", -2), E("N", "b", "zero", 0)])
        self.assertEqual(project_stock({}, events), {("n", "A"): -2, ("n", "B"): 0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
