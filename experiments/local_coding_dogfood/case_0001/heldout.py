"""Independent frozen grading: never sent to or callable by the coding model."""

import sys
import unittest

sys.path.insert(0, sys.argv.pop(1))
from stockroom.events import StockEvent as E
from stockroom.projection import project_stock


class Heldout(unittest.TestCase):
    def test_interleaved_replays(self):
        events = [
            E(" A ", "x", "1", 4),
            E("B", "x", "1", 7),
            E("a", "X", "2", -1),
            E("a", "x", "1", 4),
            E("b", " X ", "1", 7),
        ]
        self.assertEqual(
            project_stock({("other", "KEEP"): 9}, events),
            {("other", "KEEP"): 9, ("a", "X"): 3, ("b", "X"): 7},
        )

    def test_opaque_case_sensitive_ids(self):
        self.assertEqual(
            project_stock({}, [E("A", "x", "Token", 2), E("A", "x", "token", 3)]),
            {("a", "X"): 5},
        )

    def test_opaque_space_ids(self):
        self.assertEqual(
            project_stock({}, [E("A", "x", "id", 2), E("A", "x", " id ", 3)]),
            {("a", "X"): 5},
        )

    def test_unicode_canonical_duplicates(self):
        self.assertEqual(
            project_stock(
                {}, [E(" Straße ", "é", "x", -3), E("STRASSE", " É ", "x", -3)]
            ),
            {("strasse", "É"): -3},
        )

    def test_conflict_after_other_effects_does_not_mutate_input(self):
        initial = {("a", "X"): 10}
        with self.assertRaises(ValueError):
            project_stock(
                initial,
                iter(
                    [
                        E("A", "x", "first", 4),
                        E("A", "y", "ok", 7),
                        E("a", "z", "first", 4),
                    ]
                ),
            )
        self.assertEqual(initial, {("a", "X"): 10})

    def test_empty_returns_independent_mapping(self):
        initial = {("a", "X"): 0}
        result = project_stock(initial, iter(()))
        self.assertEqual(result, initial)
        self.assertIsNot(result, initial)

    def test_separate_calls_do_not_share_replay_state(self):
        events = [E("A", "x", "id", 2), E("a", "X", "id", 2)]
        self.assertEqual(project_stock({}, events), {("a", "X"): 2})
        self.assertEqual(project_stock({}, events), {("a", "X"): 2})

    def test_zero_delta_replay_conflict(self):
        with self.assertRaises(ValueError):
            project_stock({}, [E("A", "x", "id", 0), E("a", "X", "id", 1)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
