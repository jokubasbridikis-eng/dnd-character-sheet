"""Save and load characters as JSON files."""

import json
import os

from models.character import Character
from models.stats import Stats
from models.item import Item
from models.ability import Ability
from models.character_class import CLASS_MAP


class FileHandler:
    """Reads and writes character data to JSON files."""

    def __init__(self, data_directory="data/characters"):
        self._data_directory = data_directory
        os.makedirs(self._data_directory, exist_ok=True)

    @property
    def data_directory(self):
        return self._data_directory

    def _get_filepath(self, character_name):
        # Replace any unsafe characters with underscores
        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "_"
            for c in character_name
        )
        return os.path.join(self._data_directory, f"{safe_name}.json")

    def save_character(self, character):
        filepath = self._get_filepath(character.name)
        data = character.to_dict()
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return filepath

    def load_character(self, character_name):
        filepath = self._get_filepath(character_name)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No saved character found at: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        return self._dict_to_character(data)

    def load_from_filepath(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        return self._dict_to_character(data)

    def _dict_to_character(self, data):
        class_name = data.get("class", "warrior").lower()
        if class_name not in CLASS_MAP:
            raise ValueError(f"Unknown class: {class_name}")
        character_class = CLASS_MAP[class_name]()

        stats = Stats.from_dict(data.get("stats", {}))

        character = Character(
            name=data["name"],
            race=data.get("race", "Human"),
            character_class=character_class,
            stats=stats,
            level=data.get("level", 1),
            history=data.get("history", ""),
        )

        inventory_data = data.get("inventory", {})
        for item_data in inventory_data.get("items", []):
            item = Item.from_dict(item_data)
            character.inventory.add_item(item)

        for ability_data in data.get("abilities", []):
            ability = Ability.from_dict(ability_data)
            character.add_ability(ability)

        return character

    def list_saved_characters(self):
        if not os.path.exists(self._data_directory):
            return []
        files = [
            f.replace(".json", "")
            for f in os.listdir(self._data_directory)
            if f.endswith(".json")
        ]
        return sorted(files)

    def delete_character(self, character_name):
        filepath = self._get_filepath(character_name)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
