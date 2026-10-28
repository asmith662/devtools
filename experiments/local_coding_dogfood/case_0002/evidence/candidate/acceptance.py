"""Host-fixed focused tests; this entry point is read-only to the model."""

import unittest

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.discover("tests")
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
