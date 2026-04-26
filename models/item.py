"""Item model for inventory contents."""

VALID_ITEM_TYPES = ["weapon", "armor", "potion", "scroll", "tool", "misc"]


class Item:
    """Represents a single item that can be stored in an inventory."""

    def __init__(self, name, description="", weight=0.0, item_type="misc"):
        self._name = name
        self._description = description
        self._weight = max(0.0, weight)
        self._item_type = item_type if item_type in VALID_ITEM_TYPES else "misc"

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def weight(self):
        return self._weight

    @property
    def item_type(self):
        return self._item_type

    def to_dict(self):
        return {
            "name": self._name,
            "description": self._description,
            "weight": self._weight,
            "item_type": self._item_type,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            weight=data.get("weight", 0.0),
            item_type=data.get("item_type", "misc"),
        )

    def __str__(self):
        return f"{self._name} [{self._item_type}] - {self._weight}lb"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self._name == other._name and self._item_type == other._item_type

    def __repr__(self):
        return f"Item(name='{self._name}', type='{self._item_type}')"
