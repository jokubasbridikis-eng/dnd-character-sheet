"""Unit tests for the Inventory class."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.inventory import Inventory
from models.item import Item


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory(capacity=50.0)
        self.sword = Item("Iron Sword", "A basic sword", 5.0, "weapon")
        self.potion = Item("Health Potion", "Restores 10 HP", 0.5, "potion")
        self.shield = Item("Wooden Shield", "Basic shield", 8.0, "armor")

    def test_add_item(self):
        result = self.inventory.add_item(self.sword)
        self.assertTrue(result)
        self.assertEqual(self.inventory.item_count, 1)

    def test_add_item_exceeds_capacity(self):
        heavy = Item("Boulder", "Very heavy", 100.0, "misc")
        result = self.inventory.add_item(heavy)
        self.assertFalse(result)
        self.assertEqual(self.inventory.item_count, 0)

    def test_add_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            self.inventory.add_item("not an item")

    def test_remove_item(self):
        self.inventory.add_item(self.sword)
        removed = self.inventory.remove_item("Iron Sword")
        self.assertIsNotNone(removed)
        self.assertEqual(removed.name, "Iron Sword")
        self.assertEqual(self.inventory.item_count, 0)

    def test_remove_nonexistent_item(self):
        result = self.inventory.remove_item("Nonexistent")
        self.assertIsNone(result)

    def test_find_item(self):
        self.inventory.add_item(self.sword)
        found = self.inventory.find_item("Iron Sword")
        self.assertIsNotNone(found)
        self.assertEqual(self.inventory.item_count, 1)

    def test_find_item_case_insensitive(self):
        self.inventory.add_item(self.sword)
        found = self.inventory.find_item("iron sword")
        self.assertIsNotNone(found)

    def test_total_weight(self):
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.potion)
        self.assertAlmostEqual(self.inventory.total_weight, 5.5)

    def test_get_items_by_type(self):
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.potion)
        self.inventory.add_item(self.shield)
        weapons = self.inventory.get_items_by_type("weapon")
        self.assertEqual(len(weapons), 1)
        self.assertEqual(weapons[0].name, "Iron Sword")

    def test_clear_inventory(self):
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.potion)
        cleared = self.inventory.clear()
        self.assertEqual(len(cleared), 2)
        self.assertEqual(self.inventory.item_count, 0)

    def test_to_dict_and_from_dict(self):
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.potion)
        data = self.inventory.to_dict()
        restored = Inventory.from_dict(data)
        self.assertEqual(restored.item_count, 2)
        self.assertEqual(restored.capacity, 50.0)

    def test_len(self):
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.potion)
        self.assertEqual(len(self.inventory), 2)


if __name__ == "__main__":
    unittest.main()
