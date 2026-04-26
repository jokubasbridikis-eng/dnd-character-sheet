"""Unit tests for the Stats class."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.stats import Stats, STAT_NAMES, MIN_STAT, MAX_STAT


class TestStats(unittest.TestCase):

    def setUp(self):
        self.stats = Stats(strength=15, dexterity=12, constitution=14,
                           intelligence=10, wisdom=8, charisma=13)

    def test_default_stats(self):
        default = Stats()
        for name in STAT_NAMES:
            self.assertEqual(default.get_stat(name), 10)

    def test_custom_stats(self):
        self.assertEqual(self.stats.get_stat("STR"), 15)
        self.assertEqual(self.stats.get_stat("DEX"), 12)
        self.assertEqual(self.stats.get_stat("CON"), 14)
        self.assertEqual(self.stats.get_stat("INT"), 10)
        self.assertEqual(self.stats.get_stat("WIS"), 8)
        self.assertEqual(self.stats.get_stat("CHA"), 13)

    def test_set_stat_valid(self):
        self.stats.set_stat("STR", 18)
        self.assertEqual(self.stats.get_stat("STR"), 18)

    def test_set_stat_min_boundary(self):
        self.stats.set_stat("STR", MIN_STAT)
        self.assertEqual(self.stats.get_stat("STR"), MIN_STAT)

    def test_set_stat_max_boundary(self):
        self.stats.set_stat("STR", MAX_STAT)
        self.assertEqual(self.stats.get_stat("STR"), MAX_STAT)

    def test_set_stat_below_min_raises(self):
        with self.assertRaises(ValueError):
            self.stats.set_stat("STR", 0)

    def test_set_stat_above_max_raises(self):
        with self.assertRaises(ValueError):
            self.stats.set_stat("STR", 21)

    def test_invalid_stat_name_raises(self):
        with self.assertRaises(ValueError):
            self.stats.get_stat("INVALID")

    def test_non_integer_raises(self):
        with self.assertRaises(TypeError):
            self.stats.set_stat("STR", "ten")

    def test_modifier_positive(self):
        self.stats.set_stat("STR", 16)
        self.assertEqual(self.stats.get_modifier("STR"), 3)

    def test_modifier_zero(self):
        self.stats.set_stat("STR", 10)
        self.assertEqual(self.stats.get_modifier("STR"), 0)
        self.stats.set_stat("STR", 11)
        self.assertEqual(self.stats.get_modifier("STR"), 0)

    def test_modifier_negative(self):
        self.stats.set_stat("STR", 8)
        self.assertEqual(self.stats.get_modifier("STR"), -1)

    def test_get_all_stats_returns_copy(self):
        all_stats = self.stats.get_all_stats()
        all_stats["STR"] = 99
        self.assertEqual(self.stats.get_stat("STR"), 15)

    def test_to_dict_and_from_dict(self):
        data = self.stats.to_dict()
        restored = Stats.from_dict(data)
        for name in STAT_NAMES:
            self.assertEqual(self.stats.get_stat(name), restored.get_stat(name))

    def test_case_insensitive_stat_name(self):
        self.assertEqual(self.stats.get_stat("str"), 15)
        self.assertEqual(self.stats.get_stat("Str"), 15)


if __name__ == "__main__":
    unittest.main()
