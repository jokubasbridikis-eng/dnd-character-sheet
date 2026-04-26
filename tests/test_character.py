"""Unit tests for the Character class and class polymorphism."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.character import Character
from models.character_class import Warrior, Mage, Rogue, Cleric
from models.stats import Stats
from models.ability import Ability


class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character(
            name="TestHero",
            race="Human",
            character_class=Warrior(),
            stats=Stats(strength=16, constitution=14),
            level=1,
            history="A brave warrior.",
        )

    def test_character_creation(self):
        self.assertEqual(self.character.name, "TestHero")
        self.assertEqual(self.character.race, "Human")
        self.assertEqual(self.character.level, 1)

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.character.name = "   "

    def test_level_up(self):
        result = self.character.level_up()
        self.assertTrue(result)
        self.assertEqual(self.character.level, 2)

    def test_level_up_at_max(self):
        self.character.level = 20
        result = self.character.level_up()
        self.assertFalse(result)

    def test_add_ability(self):
        ability = Ability("Slash", "A basic attack", 1, "STR")
        result = self.character.add_ability(ability)
        self.assertTrue(result)
        self.assertEqual(len(self.character.get_abilities()), 1)

    def test_add_ability_level_too_low(self):
        ability = Ability("Epic Strike", "Very powerful", 10, "STR")
        result = self.character.add_ability(ability)
        self.assertFalse(result)

    def test_remove_ability(self):
        ability = Ability("Slash", "A basic attack", 1, "STR")
        self.character.add_ability(ability)
        removed = self.character.remove_ability("Slash")
        self.assertIsNotNone(removed)
        self.assertEqual(len(self.character.get_abilities()), 0)

    def test_display_sheet(self):
        sheet = self.character.display_sheet()
        self.assertIn("TestHero", sheet)
        self.assertIn("Warrior", sheet)
        self.assertIn("Human", sheet)

    def test_to_dict(self):
        data = self.character.to_dict()
        self.assertEqual(data["name"], "TestHero")
        self.assertEqual(data["class"], "warrior")
        self.assertEqual(data["level"], 1)


class TestPolymorphism(unittest.TestCase):
    """Verifies that the same method call produces different results per class."""

    def test_different_hit_points(self):
        stats = Stats(constitution=14)
        level = 5

        warrior_hp = Warrior().calculate_hit_points(level, stats.get_modifier("CON"))
        mage_hp = Mage().calculate_hit_points(level, stats.get_modifier("CON"))
        rogue_hp = Rogue().calculate_hit_points(level, stats.get_modifier("CON"))

        self.assertGreater(warrior_hp, rogue_hp)
        self.assertGreater(rogue_hp, mage_hp)

    def test_different_special_abilities(self):
        classes = [Warrior(), Mage(), Rogue(), Cleric()]
        abilities = [c.special_ability() for c in classes]
        self.assertEqual(len(set(abilities)), len(abilities))

    def test_different_proficiencies(self):
        warrior = Warrior()
        mage = Mage()
        self.assertIn("All armor", warrior.get_proficiencies())
        self.assertNotIn("All armor", mage.get_proficiencies())

    def test_warrior_bonus_hp(self):
        warrior = Warrior()
        mage = Mage()
        # At level 1 with 0 CON modifier:
        # Warrior: 10 (hit die) + 1*2 (bonus) = 12
        # Mage: 6 (hit die) = 6
        self.assertEqual(warrior.calculate_hit_points(1, 0), 12)
        self.assertEqual(mage.calculate_hit_points(1, 0), 6)


if __name__ == "__main__":
    unittest.main()
