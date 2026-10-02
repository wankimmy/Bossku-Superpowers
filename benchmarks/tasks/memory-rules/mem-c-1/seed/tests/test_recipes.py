import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import recipes


class RecipesModuleTests(unittest.TestCase):
    def test_module_imports(self):
        self.assertTrue(hasattr(recipes, "__doc__"))


if __name__ == "__main__":
    unittest.main()
