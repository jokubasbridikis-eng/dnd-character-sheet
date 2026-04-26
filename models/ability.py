"""Ability model for character skills."""


class Ability:
    """A character ability or skill with a level requirement."""

    def __init__(self, name, description="", level_requirement=1, associated_stat="STR"):
        self._name = name
        self._description = description
        self._level_requirement = max(1, level_requirement)
        self._associated_stat = associated_stat.upper()

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def level_requirement(self):
        return self._level_requirement

    @property
    def associated_stat(self):
        return self._associated_stat

    def is_available_at_level(self, level):
        return level >= self._level_requirement

    def to_dict(self):
        return {
            "name": self._name,
            "description": self._description,
            "level_requirement": self._level_requirement,
            "associated_stat": self._associated_stat,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            level_requirement=data.get("level_requirement", 1),
            associated_stat=data.get("associated_stat", "STR"),
        )

    def __str__(self):
        return f"{self._name} (Lvl {self._level_requirement}, {self._associated_stat}): {self._description}"
