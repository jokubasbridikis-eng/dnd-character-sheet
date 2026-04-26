"""Character classes - abstract base and concrete implementations."""

from abc import ABC, abstractmethod


class CharacterClass(ABC):
    """Abstract base class for all character classes."""

    def __init__(self, name, hit_die, primary_stat):
        self._name = name
        self._hit_die = hit_die
        self._primary_stat = primary_stat

    @property
    def name(self):
        return self._name

    @property
    def hit_die(self):
        return self._hit_die

    @property
    def primary_stat(self):
        return self._primary_stat

    @abstractmethod
    def special_ability(self):
        pass

    @abstractmethod
    def get_proficiencies(self):
        pass

    def calculate_hit_points(self, level, con_modifier):
        base_hp = self._hit_die
        level_hp = (level - 1) * (self._hit_die // 2 + 1)
        con_bonus = level * con_modifier
        return max(1, base_hp + level_hp + con_bonus)

    def __str__(self):
        return f"{self._name} (Hit Die: d{self._hit_die}, Primary: {self._primary_stat})"


class Warrior(CharacterClass):

    def __init__(self):
        super().__init__(name="Warrior", hit_die=10, primary_stat="STR")

    def special_ability(self):
        return "Second Wind: Recover 1d10 + level hit points as a bonus action."

    def get_proficiencies(self):
        return ["All armor", "Shields", "Simple weapons", "Martial weapons"]

    def calculate_hit_points(self, level, con_modifier):
        # Warriors get +2 bonus HP per level
        base = super().calculate_hit_points(level, con_modifier)
        return base + (level * 2)


class Mage(CharacterClass):

    def __init__(self):
        super().__init__(name="Mage", hit_die=6, primary_stat="INT")

    def special_ability(self):
        return "Arcane Recovery: Recover spell slots during a short rest."

    def get_proficiencies(self):
        return ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"]


class Rogue(CharacterClass):

    def __init__(self):
        super().__init__(name="Rogue", hit_die=8, primary_stat="DEX")

    def special_ability(self):
        return "Sneak Attack: Deal extra 1d6 damage when you have advantage."

    def get_proficiencies(self):
        return ["Light armor", "Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"]


class Cleric(CharacterClass):

    def __init__(self):
        super().__init__(name="Cleric", hit_die=8, primary_stat="WIS")

    def special_ability(self):
        return "Divine Intervention: Call upon your deity for miraculous aid."

    def get_proficiencies(self):
        return ["Light armor", "Medium armor", "Shields", "Simple weapons"]


CLASS_MAP = {
    "warrior": Warrior,
    "mage": Mage,
    "rogue": Rogue,
    "cleric": Cleric,
}
