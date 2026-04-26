"""Inventory model - holds a collection of items."""

from models.item import Item


class Inventory:
    """Manages a collection of items with a weight capacity limit."""

    def __init__(self, capacity=150.0):
        self._items: list[Item] = []
        self._capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    @property
    def total_weight(self):
        return sum(item.weight for item in self._items)

    @property
    def item_count(self):
        return len(self._items)

    def add_item(self, item):
        """Add an item if there is enough weight capacity. Returns True on success."""
        if not isinstance(item, Item):
            raise TypeError("Can only add Item objects to inventory.")
        if self.total_weight + item.weight > self._capacity:
            return False
        self._items.append(item)
        return True

    def remove_item(self, item_name):
        """Remove and return an item by name, or None if not found."""
        for i, item in enumerate(self._items):
            if item.name.lower() == item_name.lower():
                return self._items.pop(i)
        return None

    def find_item(self, item_name):
        for item in self._items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def get_items_by_type(self, item_type):
        return [item for item in self._items if item.item_type == item_type]

    def get_all_items(self):
        return list(self._items)

    def clear(self):
        items = list(self._items)
        self._items.clear()
        return items

    def to_dict(self):
        return {
            "capacity": self._capacity,
            "items": [item.to_dict() for item in self._items],
        }

    @classmethod
    def from_dict(cls, data):
        inventory = cls(capacity=data.get("capacity", 150.0))
        for item_data in data.get("items", []):
            item = Item.from_dict(item_data)
            inventory.add_item(item)
        return inventory

    def __str__(self):
        if not self._items:
            return "  Inventory is empty."
        lines = [f"  Inventory ({self.total_weight:.1f}/{self._capacity:.1f} lb):"]
        for item in self._items:
            lines.append(f"    - {item}")
        return "\n".join(lines)

    def __len__(self):
        return len(self._items)
