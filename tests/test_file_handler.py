"""Unit tests for the FileHandler class."""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.file_handler import FileHandler
from builder.character_builder import CharacterBuilder
from models.character_class import Warrior
from models.stats import Stats
from models.item import Item
from models.ability import Ability


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.handler = FileHandler(data_directory=self.test_dir)

        builder = CharacterBuilder()
        self.character = (
            builder
            .set_name("TestHero")
            .set_race("Human")
            .set_class(Warrior())
            .set_stats(Stats(strength=16, constitution=14))
            .set_level(3)
            .set_history("A test character.")
            .build()
        )
        self.character.inventory.add_item(Item("Test Sword", "A sword", 5.0, "weapon"))
        self.character.add_ability(Ability("Power Strike", "Deal extra damage", 1, "STR"))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_character(self):
        filepath = self.handler.save_character(self.character)
        self.assertTrue(os.path.exists(filepath))

    def test_load_character(self):
        self.handler.save_character(self.character)
        loaded = self.handler.load_character("TestHero")
        self.assertEqual(loaded.name, "TestHero")
        self.assertEqual(loaded.race, "Human")
        self.assertEqual(loaded.level, 3)
        self.assertEqual(loaded.character_class.name, "Warrior")

    def test_save_load_roundtrip_stats(self):
        self.handler.save_character(self.character)
        loaded = self.handler.load_character("TestHero")
        self.assertEqual(loaded.stats.get_stat("STR"), 16)
        self.assertEqual(loaded.stats.get_stat("CON"), 14)
        self.assertEqual(loaded.stats.get_stat("INT"), 10)

    def test_save_load_roundtrip_inventory(self):
        self.handler.save_character(self.character)
        loaded = self.handler.load_character("TestHero")
        self.assertEqual(loaded.inventory.item_count, 1)
        found = loaded.inventory.find_item("Test Sword")
        self.assertIsNotNone(found)
        self.assertEqual(found.item_type, "weapon")

    def test_save_load_roundtrip_abilities(self):
        self.handler.save_character(self.character)
        loaded = self.handler.load_character("TestHero")
        abilities = loaded.get_abilities()
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].name, "Power Strike")

    def test_load_nonexistent_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.handler.load_character("DoesNotExist")

    def test_list_saved_characters(self):
        self.handler.save_character(self.character)
        saved = self.handler.list_saved_characters()
        self.assertIn("TestHero", saved)

    def test_delete_character(self):
        self.handler.save_character(self.character)
        result = self.handler.delete_character("TestHero")
        self.assertTrue(result)
        saved = self.handler.list_saved_characters()
        self.assertNotIn("TestHero", saved)

    def test_delete_nonexistent_returns_false(self):
        result = self.handler.delete_character("DoesNotExist")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
