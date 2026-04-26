"""Unit tests for CharacterBuilder and CharacterDirector."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from builder.character_builder import CharacterBuilder, CharacterDirector
from models.character_class import Warrior, Mage
from models.stats import Stats


class TestCharacterBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = CharacterBuilder()

    def test_build_complete_character(self):
        character = (
            self.builder
            .set_name("Gandalf")
            .set_race("Human")
            .set_class(Mage())
            .set_stats(Stats(intelligence=18))
            .set_level(5)
            .set_history("A wise wizard.")
            .build()
        )
        self.assertEqual(character.name, "Gandalf")
        self.assertEqual(character.race, "Human")
        self.assertEqual(character.level, 5)
        self.assertEqual(character.character_class.name, "Mage")

    def test_build_missing_name_raises(self):
        self.builder.set_race("Elf").set_class(Mage()).set_stats(Stats())
        with self.assertRaises(ValueError) as ctx:
            self.builder.build()
        self.assertIn("name", str(ctx.exception))

    def test_build_missing_class_raises(self):
        self.builder.set_name("Test").set_race("Elf").set_stats(Stats())
        with self.assertRaises(ValueError) as ctx:
            self.builder.build()
        self.assertIn("character class", str(ctx.exception))

    def test_build_missing_stats_raises(self):
        self.builder.set_name("Test").set_race("Elf").set_class(Warrior())
        with self.assertRaises(ValueError) as ctx:
            self.builder.build()
        self.assertIn("stats", str(ctx.exception))

    def test_set_class_by_name(self):
        character = (
            self.builder
            .set_name("Test")
            .set_race("Human")
            .set_class_by_name("warrior")
            .set_stats(Stats())
            .build()
        )
        self.assertEqual(character.character_class.name, "Warrior")

    def test_set_class_by_invalid_name_raises(self):
        with self.assertRaises(ValueError):
            self.builder.set_class_by_name("bard")

    def test_builder_resets_after_build(self):
        self.builder.set_name("A").set_race("B").set_class(Warrior()).set_stats(Stats())
        self.builder.build()
        with self.assertRaises(ValueError):
            self.builder.build()

    def test_method_chaining(self):
        result = self.builder.set_name("Test")
        self.assertIs(result, self.builder)
        result = self.builder.set_race("Elf")
        self.assertIs(result, self.builder)

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.builder.set_name("")

    def test_set_stats_from_values(self):
        character = (
            self.builder
            .set_name("Test")
            .set_race("Human")
            .set_class(Warrior())
            .set_stats_from_values(strength=18, dexterity=14)
            .build()
        )
        self.assertEqual(character.stats.get_stat("STR"), 18)
        self.assertEqual(character.stats.get_stat("DEX"), 14)
        self.assertEqual(character.stats.get_stat("INT"), 10)


class TestCharacterDirector(unittest.TestCase):

    def setUp(self):
        self.builder = CharacterBuilder()
        self.director = CharacterDirector(self.builder)

    def test_create_default_warrior(self):
        character = self.director.create_default_warrior()
        self.assertEqual(character.name, "Thorin")
        self.assertEqual(character.race, "Dwarf")
        self.assertEqual(character.character_class.name, "Warrior")
        self.assertEqual(character.stats.get_stat("STR"), 16)

    def test_create_default_mage(self):
        character = self.director.create_default_mage()
        self.assertEqual(character.name, "Elara")
        self.assertEqual(character.character_class.name, "Mage")
        self.assertEqual(character.stats.get_stat("INT"), 16)

    def test_create_default_rogue(self):
        character = self.director.create_default_rogue()
        self.assertEqual(character.name, "Shadow")
        self.assertEqual(character.character_class.name, "Rogue")
        self.assertEqual(character.stats.get_stat("DEX"), 16)

    def test_custom_name_on_preset(self):
        character = self.director.create_default_warrior("Gimli")
        self.assertEqual(character.name, "Gimli")


if __name__ == "__main__":
    unittest.main()
