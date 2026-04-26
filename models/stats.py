"""Character ability scores."""

STAT_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
MIN_STAT = 1
MAX_STAT = 20
DEFAULT_STAT = 10


class Stats:
    """Stores and validates the six DND ability scores."""

    def __init__(self, strength=DEFAULT_STAT, dexterity=DEFAULT_STAT,
                 constitution=DEFAULT_STAT, intelligence=DEFAULT_STAT,
                 wisdom=DEFAULT_STAT, charisma=DEFAULT_STAT):
        self._stats = {}
        self.set_stat("STR", strength)
        self.set_stat("DEX", dexterity)
        self.set_stat("CON", constitution)
        self.set_stat("INT", intelligence)
        self.set_stat("WIS", wisdom)
        self.set_stat("CHA", charisma)

    def _validate_stat_name(self, name):
        name = name.upper().strip()
        if name not in STAT_NAMES:
            raise ValueError(f"Invalid stat name '{name}'. Must be one of: {STAT_NAMES}")
        return name

    def _validate_stat_value(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Stat value must be an integer, got {type(value).__name__}")
        if value < MIN_STAT or value > MAX_STAT:
            raise ValueError(f"Stat value must be between {MIN_STAT} and {MAX_STAT}, got {value}")
        return value

    def get_stat(self, name):
        name = self._validate_stat_name(name)
        return self._stats[name]

    def set_stat(self, name, value):
        name = self._validate_stat_name(name)
        value = self._validate_stat_value(value)
        self._stats[name] = value

    def get_modifier(self, name):
        """Calculate DND ability modifier: (stat - 10) // 2."""
        value = self.get_stat(name)
        return (value - 10) // 2

    def get_all_stats(self):
        return dict(self._stats)

    def to_dict(self):
        return dict(self._stats)

    @classmethod
    def from_dict(cls, data):
        return cls(
            strength=data.get("STR", DEFAULT_STAT),
            dexterity=data.get("DEX", DEFAULT_STAT),
            constitution=data.get("CON", DEFAULT_STAT),
            intelligence=data.get("INT", DEFAULT_STAT),
            wisdom=data.get("WIS", DEFAULT_STAT),
            charisma=data.get("CHA", DEFAULT_STAT),
        )

    def __str__(self):
        lines = []
        for name in STAT_NAMES:
            value = self._stats[name]
            modifier = self.get_modifier(name)
            sign = "+" if modifier >= 0 else ""
            lines.append(f"  {name}: {value:2d} ({sign}{modifier})")
        return "\n".join(lines)
