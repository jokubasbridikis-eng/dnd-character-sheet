"""DND Character Sheet Creator - main application entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.stats import STAT_NAMES
from models.item import Item, VALID_ITEM_TYPES
from models.ability import Ability
from models.character_class import CLASS_MAP
from builder.character_builder import CharacterBuilder, CharacterDirector
from utils.file_handler import FileHandler


class CharacterSheetApp:
    """Main application with a menu-driven interface."""

    def __init__(self):
        self._builder = CharacterBuilder()
        self._director = CharacterDirector(self._builder)
        self._file_handler = FileHandler()
        self._characters: list = []
        self._current_character = None

    def run(self):
        print("\n" + "=" * 50)
        print("  DND Character Sheet Creator")
        print("=" * 50)

        while True:
            self._show_main_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self._create_character()
            elif choice == "2":
                self._create_preset_character()
            elif choice == "3":
                self._load_character()
            elif choice == "4":
                self._view_character()
            elif choice == "5":
                self._edit_character()
            elif choice == "6":
                self._manage_inventory()
            elif choice == "7":
                self._manage_abilities()
            elif choice == "8":
                self._save_character()
            elif choice == "9":
                self._list_characters()
            elif choice == "0":
                print("\nFarewell, adventurer!")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def _show_main_menu(self):
        print("\n--- Main Menu ---")
        current = f" (Current: {self._current_character})" if self._current_character else ""
        print(f"  Active character:{current}")
        print("  1. Create new character (custom)")
        print("  2. Create new character (preset)")
        print("  3. Load character from file")
        print("  4. View character sheet")
        print("  5. Edit character")
        print("  6. Manage inventory")
        print("  7. Manage abilities")
        print("  8. Save character to file")
        print("  9. List saved characters")
        print("  0. Exit")

    def _create_character(self):
        print("\n--- Create New Character ---")

        try:
            name = input("Enter character name: ").strip()
            self._builder.set_name(name)

            race = input("Enter race (e.g., Human, Elf, Dwarf, Halfling): ").strip()
            self._builder.set_race(race)

            available = list(CLASS_MAP.keys())
            print(f"Available classes: {', '.join(available)}")
            class_name = input("Enter class: ").strip()
            self._builder.set_class_by_name(class_name)

            print(f"\nSet stats (values 1-20):")
            stats_values = {}
            for stat in STAT_NAMES:
                while True:
                    try:
                        value = int(input(f"  {stat}: "))
                        stats_values[stat.lower()[:3]] = value
                        break
                    except ValueError:
                        print("  Please enter a valid integer.")
            self._builder.set_stats_from_values(
                strength=stats_values.get("str", 10),
                dexterity=stats_values.get("dex", 10),
                constitution=stats_values.get("con", 10),
                intelligence=stats_values.get("int", 10),
                wisdom=stats_values.get("wis", 10),
                charisma=stats_values.get("cha", 10),
            )

            level_input = input("Enter starting level (1-20, default 1): ").strip()
            level = int(level_input) if level_input else 1
            self._builder.set_level(level)

            history = input("Enter character backstory (optional): ").strip()
            self._builder.set_history(history)

            character = self._builder.build()
            self._characters.append(character)
            self._current_character = character
            print(f"\nCharacter '{character.name}' created successfully!")

        except (ValueError, TypeError) as e:
            print(f"\nError creating character: {e}")

    def _create_preset_character(self):
        print("\n--- Preset Characters ---")
        print("  1. Default Warrior (Dwarf)")
        print("  2. Default Mage (Elf)")
        print("  3. Default Rogue (Halfling)")

        choice = input("Select preset: ").strip()
        name = input("Enter character name (or press Enter for default): ").strip()

        try:
            if choice == "1":
                character = self._director.create_default_warrior(name if name else "Thorin")
            elif choice == "2":
                character = self._director.create_default_mage(name if name else "Elara")
            elif choice == "3":
                character = self._director.create_default_rogue(name if name else "Shadow")
            else:
                print("Invalid choice.")
                return

            self._characters.append(character)
            self._current_character = character
            print(f"\nCharacter '{character.name}' created successfully!")
        except (ValueError, TypeError) as e:
            print(f"\nError: {e}")

    def _view_character(self):
        if not self._current_character:
            print("\nNo character selected. Create or load one first.")
            return
        print(self._current_character.display_sheet())

    def _edit_character(self):
        if not self._current_character:
            print("\nNo character selected.")
            return

        print("\n--- Edit Character ---")
        print("  1. Edit name")
        print("  2. Edit stats")
        print("  3. Level up")
        print("  4. Edit history")
        print("  5. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            new_name = input("New name: ").strip()
            if new_name:
                self._current_character.name = new_name
                print("Name updated.")
        elif choice == "2":
            self._edit_stats()
        elif choice == "3":
            if self._current_character.level_up():
                print(f"Leveled up to {self._current_character.level}! New HP: {self._current_character.hit_points}")
            else:
                print("Already at max level (20).")
        elif choice == "4":
            history = input("New backstory: ").strip()
            self._current_character.history = history
            print("History updated.")

    def _edit_stats(self):
        print(f"\nCurrent stats:\n{self._current_character.stats}")
        stat_name = input("Which stat to edit? (e.g., STR): ").strip().upper()
        try:
            current = self._current_character.stats.get_stat(stat_name)
            print(f"Current {stat_name}: {current}")
            new_value = int(input(f"New value for {stat_name}: "))
            self._current_character.stats.set_stat(stat_name, new_value)
            print(f"{stat_name} updated to {new_value}.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def _manage_inventory(self):
        if not self._current_character:
            print("\nNo character selected.")
            return

        print("\n--- Inventory Management ---")
        print("  1. Add item")
        print("  2. Remove item")
        print("  3. View inventory")
        print("  4. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            name = input("Item name: ").strip()
            description = input("Description: ").strip()
            print(f"Item types: {VALID_ITEM_TYPES}")
            item_type = input("Type: ").strip().lower()
            try:
                weight = float(input("Weight (lb): "))
            except ValueError:
                weight = 0.0

            item = Item(name, description, weight, item_type)
            if self._current_character.inventory.add_item(item):
                print(f"Added '{name}' to inventory.")
            else:
                print("Cannot add item - exceeds carry capacity!")
        elif choice == "2":
            name = input("Item name to remove: ").strip()
            removed = self._current_character.inventory.remove_item(name)
            if removed:
                print(f"Removed '{removed.name}'.")
            else:
                print("Item not found.")
        elif choice == "3":
            print(self._current_character.inventory)

    def _manage_abilities(self):
        if not self._current_character:
            print("\nNo character selected.")
            return

        print("\n--- Ability Management ---")
        print("  1. Add ability")
        print("  2. Remove ability")
        print("  3. View abilities")
        print("  4. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            name = input("Ability name: ").strip()
            description = input("Description: ").strip()
            try:
                level_req = int(input("Level requirement: "))
            except ValueError:
                level_req = 1
            stat = input("Associated stat (e.g., STR): ").strip()

            ability = Ability(name, description, level_req, stat)
            if self._current_character.add_ability(ability):
                print(f"Added ability '{name}'.")
            else:
                print(f"Character level ({self._current_character.level}) too low for this ability (requires {level_req}).")
        elif choice == "2":
            name = input("Ability name to remove: ").strip()
            removed = self._current_character.remove_ability(name)
            if removed:
                print(f"Removed '{removed.name}'.")
            else:
                print("Ability not found.")
        elif choice == "3":
            abilities = self._current_character.get_abilities()
            if abilities:
                for ability in abilities:
                    print(f"  - {ability}")
            else:
                print("  No abilities.")

    def _save_character(self):
        if not self._current_character:
            print("\nNo character selected.")
            return
        try:
            filepath = self._file_handler.save_character(self._current_character)
            print(f"Character saved to: {filepath}")
        except OSError as e:
            print(f"Error saving: {e}")

    def _load_character(self):
        saved = self._file_handler.list_saved_characters()
        if not saved:
            print("\nNo saved characters found.")
            return
        print("\n--- Saved Characters ---")
        for i, name in enumerate(saved, 1):
            print(f"  {i}. {name}")

        choice = input("Select character number: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(saved):
                character = self._file_handler.load_character(saved[index])
                self._characters.append(character)
                self._current_character = character
                print(f"Loaded '{character.name}'!")
            else:
                print("Invalid selection.")
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading: {e}")

    def _list_characters(self):
        saved = self._file_handler.list_saved_characters()
        if not saved:
            print("\nNo saved characters.")
            return
        print("\n--- Saved Characters ---")
        for name in saved:
            print(f"  - {name}")


if __name__ == "__main__":
    app = CharacterSheetApp()
    app.run()
