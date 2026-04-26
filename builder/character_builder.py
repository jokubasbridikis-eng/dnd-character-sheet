"""Builder for constructing Character objects step by step."""

from models.character import Character
from models.stats import Stats
from models.character_class import CharacterClass, CLASS_MAP


class CharacterBuilder:
    """Builds a Character object step by step with method chaining."""

    def __init__(self):
        self._reset()

    def _reset(self):
        self._name = None
        self._race = None
        self._character_class = None
        self._stats = None
        self._level = 1
        self._history = ""

    def set_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self._name = name.strip()
        return self

    def set_race(self, race):
        if not race.strip():
            raise ValueError("Race cannot be empty.")
        self._race = race.strip()
        return self

    def set_class(self, character_class):
        if not isinstance(character_class, CharacterClass):
            raise TypeError("Must provide a CharacterClass instance.")
        self._character_class = character_class
        return self

    def set_class_by_name(self, class_name):
        class_name = class_name.lower().strip()
        if class_name not in CLASS_MAP:
            raise ValueError(f"Unknown class '{class_name}'. Available: {list(CLASS_MAP.keys())}")
        self._character_class = CLASS_MAP[class_name]()
        return self

    def set_stats(self, stats):
        if not isinstance(stats, Stats):
            raise TypeError("Must provide a Stats instance.")
        self._stats = stats
        return self

    def set_stats_from_values(self, strength=10, dexterity=10, constitution=10,
                              intelligence=10, wisdom=10, charisma=10):
        self._stats = Stats(
            strength=strength, dexterity=dexterity,
            constitution=constitution, intelligence=intelligence,
            wisdom=wisdom, charisma=charisma,
        )
        return self

    def set_level(self, level):
        self._level = max(1, min(20, level))
        return self

    def set_history(self, history):
        self._history = history
        return self

    def build(self):
        """Validate and construct the final Character."""
        missing = []
        if self._name is None:
            missing.append("name")
        if self._race is None:
            missing.append("race")
        if self._character_class is None:
            missing.append("character class")
        if self._stats is None:
            missing.append("stats")

        if missing:
            raise ValueError(f"Cannot build character. Missing: {', '.join(missing)}")

        character = Character(
            name=self._name,
            race=self._race,
            character_class=self._character_class,
            stats=self._stats,
            level=self._level,
            history=self._history,
        )
        self._reset()
        return character


class CharacterDirector:
    """Creates preset character builds using a CharacterBuilder."""

    def __init__(self, builder):
        self._builder = builder

    def create_default_warrior(self, name="Thorin"):
        return (
            self._builder
            .set_name(name)
            .set_race("Dwarf")
            .set_class_by_name("warrior")
            .set_stats_from_values(strength=16, dexterity=12, constitution=14,
                                   intelligence=8, wisdom=10, charisma=10)
            .set_level(1)
            .set_history("A seasoned warrior from the mountain halls.")
            .build()
        )

    def create_default_mage(self, name="Elara"):
        return (
            self._builder
            .set_name(name)
            .set_race("Elf")
            .set_class_by_name("mage")
            .set_stats_from_values(strength=8, dexterity=14, constitution=10,
                                   intelligence=16, wisdom=12, charisma=12)
            .set_level(1)
            .set_history("A scholar of the arcane arts from the Elven Academy.")
            .build()
        )

    def create_default_rogue(self, name="Shadow"):
        return (
            self._builder
            .set_name(name)
            .set_race("Halfling")
            .set_class_by_name("rogue")
            .set_stats_from_values(strength=10, dexterity=16, constitution=12,
                                   intelligence=14, wisdom=10, charisma=12)
            .set_level(1)
            .set_history("A street-smart thief with a heart of gold.")
            .build()
        )
