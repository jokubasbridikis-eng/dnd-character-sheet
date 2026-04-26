"""Character model - the main character sheet."""

from models.stats import Stats
from models.inventory import Inventory
from models.ability import Ability
from models.character_class import CharacterClass


class Character:
    """A full DND character with stats, class, inventory, and abilities."""

    def __init__(self, name, race, character_class, stats, level=1, history=""):
        self._name = name
        self._race = race
        self._character_class = character_class
        self._stats = stats
        self._inventory = Inventory()
        self._abilities: list[Ability] = []
        self._level = max(1, min(20, level))
        self._history = history

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Character name cannot be empty.")
        self._name = value.strip()

    @property
    def race(self):
        return self._race

    @property
    def character_class(self):
        return self._character_class

    @property
    def stats(self):
        return self._stats

    @property
    def inventory(self):
        return self._inventory

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = max(1, min(20, value))

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def hit_points(self):
        con_mod = self._stats.get_modifier("CON")
        return self._character_class.calculate_hit_points(self._level, con_mod)

    def add_ability(self, ability):
        if not isinstance(ability, Ability):
            raise TypeError("Can only add Ability objects.")
        if not ability.is_available_at_level(self._level):
            return False
        self._abilities.append(ability)
        return True

    def remove_ability(self, ability_name):
        for i, ability in enumerate(self._abilities):
            if ability.name.lower() == ability_name.lower():
                return self._abilities.pop(i)
        return None

    def get_abilities(self):
        return list(self._abilities)

    def level_up(self):
        if self._level >= 20:
            return False
        self._level += 1
        return True

    def to_dict(self):
        return {
            "name": self._name,
            "race": self._race,
            "class": self._character_class.name.lower(),
            "stats": self._stats.to_dict(),
            "inventory": self._inventory.to_dict(),
            "abilities": [a.to_dict() for a in self._abilities],
            "level": self._level,
            "history": self._history,
        }

    def display_sheet(self):
        separator = "=" * 50
        lines = [
            separator,
            f"  CHARACTER SHEET: {self._name}",
            separator,
            f"  Race: {self._race}",
            f"  Class: {self._character_class}",
            f"  Level: {self._level}",
            f"  HP: {self.hit_points}",
            "",
            "  --- Stats ---",
            str(self._stats),
            "",
            "  --- Special Ability ---",
            f"  {self._character_class.special_ability()}",
            "",
            "  --- Proficiencies ---",
        ]
        for prof in self._character_class.get_proficiencies():
            lines.append(f"    - {prof}")
        lines.append("")
        lines.append("  --- Abilities ---")
        if self._abilities:
            for ability in self._abilities:
                lines.append(f"    - {ability}")
        else:
            lines.append("    No abilities added.")
        lines.append("")
        lines.append("  --- Inventory ---")
        lines.append(str(self._inventory))
        lines.append("")
        lines.append("  --- History ---")
        lines.append(f"  {self._history if self._history else 'No history recorded.'}")
        lines.append(separator)
        return "\n".join(lines)

    def __str__(self):
        return f"{self._name} - Level {self._level} {self._race} {self._character_class.name} (HP: {self.hit_points})"
