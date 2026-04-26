# DND Character Sheet Creator

## 1. Introduction

### 1.1 What is this application?

The **DND Character Sheet Creator** is a command-line Python application that allows users to create, edit, save, and load digital character sheets for Dungeons and Dragons. It serves as a practical demonstration of Object-Oriented Programming (OOP) principles, implementing all four OOP pillars, the Builder design pattern, composition and aggregation relationships, file I/O operations, and unit testing.

### 1.2 How to run the program

**Prerequisites:** Python 3.10 or higher.

1. Clone the repository from GitHub:
   ```bash
   git clone <repository-url>
   cd dnd_helper
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Run the unit tests:
   ```bash
   python -m unittest discover -s tests -v
   ```

No external libraries are required the project uses only Python's standard library.

### 1.3 How to use the program

When the application starts, a menu is displayed with the following options:

1. **Create new character (custom)**: build a character step by step, choosing name, race, class, stats, level, and backstory.
2. **Create new character (preset)**: quickly generate a pre-configured Warrior, Mage, or Rogue.
3. **Load character from file**: load a previously saved character from a JSON file.
4. **View character sheet**: display the full character sheet with stats, abilities, inventory, and more.
5. **Edit character**: modify the character's name, stats, level, or backstory.
6. **Manage inventory**: add or remove items from the character's inventory.
7. **Manage abilities**: add or remove abilities and skills.
8. **Save character to file**: save the current character to a JSON file in `data/characters/`.
9. **List saved characters**: view all previously saved characters.
10. **Exit**: close the application.

The user navigates through the menu by entering the number of the desired option. Character data is persisted as JSON files, allowing characters to be saved and loaded across sessions.

---

## 2. Body / Analysis

This section explains how the program implements each functional requirement, with code snippets and explanations.

### 2.1 The Four OOP Pillars

#### 2.1.1 Encapsulation

**What it is:** Encapsulation is the practice of bundling data and the methods that operate on that data within a single class, while restricting direct access to the internal state. This is achieved through private attributes and controlled access via getters and setters.

**How it is used in code:**

The `Stats` class is the clearest example of encapsulation. The six ability scores are stored in a private dictionary `_stats` that cannot be accessed directly from outside the class. All access goes through `get_stat()` and `set_stat()` methods, which enforce validation rules:

```python
class Stats:
    def __init__(self, strength=10, dexterity=10, ...):
        self._stats = {}  # Private attribute
        self.set_stat("STR", strength)
        ...

    def set_stat(self, name: str, value: int) -> None:
        name = self._validate_stat_name(name)
        value = self._validate_stat_value(value)
        self._stats[name] = value

    def _validate_stat_value(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError(...)
        if value < MIN_STAT or value > MAX_STAT:
            raise ValueError(...)
        return value
```

This ensures that stat values can never be set outside the valid range of 1–20, and that invalid data types are rejected. The `get_all_stats()` method returns a **copy** of the internal dictionary rather than a reference, preventing external code from modifying the internal state:

```python
def get_all_stats(self) -> dict:
    return dict(self._stats)  # Returns a copy
```

Encapsulation is also present throughout other classes — `Item`, `Ability`, `Inventory`, and `Character` all use private attributes with property decorators for controlled access.

#### 2.1.2 Abstraction

**What it is:** Abstraction means defining a simplified interface that hides complex implementation details. In Python, this is commonly achieved using abstract base classes (ABC) with abstract methods that subclasses must implement.

**How it is used in code:**

The `CharacterClass` is an abstract base class that defines the interface all character classes must follow:

```python
from abc import ABC, abstractmethod

class CharacterClass(ABC):
    @abstractmethod
    def special_ability(self) -> str:
        pass

    @abstractmethod
    def get_proficiencies(self) -> list:
        pass

    def calculate_hit_points(self, level: int, con_modifier: int) -> int:
        base_hp = self._hit_die
        level_hp = (level - 1) * (self._hit_die // 2 + 1)
        con_bonus = level * con_modifier
        return max(1, base_hp + level_hp + con_bonus)
```

You cannot create an instance of `CharacterClass` directly — Python will raise a `TypeError`. Every subclass (Warrior, Mage, Rogue, Cleric) **must** implement `special_ability()` and `get_proficiencies()`. The rest of the program can work with any `CharacterClass` without knowing which specific subclass it is dealing with — it only needs to know the abstract interface.

#### 2.1.3 Inheritance

**What it is:** Inheritance allows a class to inherit attributes and methods from a parent class, enabling code reuse and establishing an "is-a" relationship between classes.

**How it is used in code:**

Four character classes inherit from the abstract `CharacterClass`:

```python
class Warrior(CharacterClass):
    def __init__(self):
        super().__init__(name="Warrior", hit_die=10, primary_stat="STR")

    def special_ability(self) -> str:
        return "Second Wind: Recover 1d10 + level hit points as a bonus action."

    def get_proficiencies(self) -> list:
        return ["All armor", "Shields", "Simple weapons", "Martial weapons"]

class Mage(CharacterClass):
    def __init__(self):
        super().__init__(name="Mage", hit_die=6, primary_stat="INT")

    def special_ability(self) -> str:
        return "Arcane Recovery: Recover spell slots during a short rest."

    def get_proficiencies(self) -> list:
        return ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"]
```

Each subclass calls `super().__init__()` to reuse the parent's constructor, inheriting the `name`, `hit_die`, and `primary_stat` properties along with the `calculate_hit_points()` method. This avoids code duplication — the base HP formula is written once and shared.

#### 2.1.4 Polymorphism

**What it is:** Polymorphism means "many forms" — the same method call can behave differently depending on which class the object belongs to. This allows code to work with objects of different types through a common interface.

**How it is used in code:**

The `calculate_hit_points()` method demonstrates polymorphism. The base class provides a default implementation, but `Warrior` overrides it to add bonus HP:

```python
# In CharacterClass (base):
def calculate_hit_points(self, level: int, con_modifier: int) -> int:
    base_hp = self._hit_die
    level_hp = (level - 1) * (self._hit_die // 2 + 1)
    con_bonus = level * con_modifier
    return max(1, base_hp + level_hp + con_bonus)

# In Warrior (override):
def calculate_hit_points(self, level: int, con_modifier: int) -> int:
    base = super().calculate_hit_points(level, con_modifier)
    return base + (level * 2)  # Warriors get +2 HP per level
```

When the `Character` class calls `self._character_class.calculate_hit_points(...)`, it does not need to know whether the class is a Warrior, Mage, or Rogue — Python automatically calls the correct version. The unit tests verify this behavior:

```python
def test_different_hit_points(self):
    stats = Stats(constitution=14)
    warrior_hp = Warrior().calculate_hit_points(5, stats.get_modifier("CON"))
    mage_hp = Mage().calculate_hit_points(5, stats.get_modifier("CON"))
    self.assertGreater(warrior_hp, mage_hp)
```

Similarly, `special_ability()` and `get_proficiencies()` return different results for each class — same method name, different behavior.

### 2.2 Design Pattern: Builder

**What it is:** The Builder pattern separates the construction of a complex object from its representation. Instead of a single constructor with many parameters, the object is built step by step.

**Why Builder was chosen over other patterns:**

- **Singleton** is not suitable because we need to create **multiple** characters, not restrict to one instance.
- **Factory Method** could help create different `CharacterClass` objects, but it does not solve the problem of assembling a full `Character` with stats, inventory, abilities, etc.
- **Builder** is the best fit because a `Character` has many components (name, race, class, stats, level, history) that are set independently and validated before the final object is created.

**How it is used in code:**

The `CharacterBuilder` class provides setter methods that return `self` for method chaining:

```python
class CharacterBuilder:
    def set_name(self, name: str) -> "CharacterBuilder":
        self._name = name.strip()
        return self

    def set_race(self, race: str) -> "CharacterBuilder":
        self._race = race.strip()
        return self

    def build(self) -> Character:
        missing = []
        if self._name is None:
            missing.append("name")
        if self._character_class is None:
            missing.append("character class")
        ...
        if missing:
            raise ValueError(f"Cannot build character. Missing: {', '.join(missing)}")

        character = Character(name=self._name, race=self._race, ...)
        self._reset()
        return character
```

Usage with method chaining:

```python
character = (
    builder
    .set_name("Gandalf")
    .set_race("Human")
    .set_class(Mage())
    .set_stats(Stats(intelligence=18))
    .build()
)
```

The `CharacterDirector` uses the builder to create preset configurations:

```python
class CharacterDirector:
    def create_default_warrior(self, name="Thorin") -> Character:
        return (
            self._builder
            .set_name(name)
            .set_race("Dwarf")
            .set_class_by_name("warrior")
            .set_stats_from_values(strength=16, dexterity=12, ...)
            .build()
        )
```

The `build()` method validates that all required fields are present before constructing the object, and resets the builder afterwards so it can be reused.

### 2.3 Composition and Aggregation

**Composition** is a "strong ownership" relationship — the contained object cannot meaningfully exist without the owner. If the owner is destroyed, so are its components.

**Aggregation** is a "weak ownership" relationship — the contained objects can exist independently of the container.

**Composition in code:**

The `Character` class **composes** `Stats` and `Inventory`:

```python
class Character:
    def __init__(self, name, race, character_class, stats, ...):
        self._stats = stats              # Composition: stats belong to this character
        self._inventory = Inventory()    # Composition: created internally
```

The `CharacterSheetApp` composes `FileHandler` and `CharacterBuilder`:

```python
class CharacterSheetApp:
    def __init__(self):
        self._builder = CharacterBuilder()      # Composition
        self._file_handler = FileHandler()      # Composition
```

These components are created by and belong to the owning class. The `FileHandler` has no purpose outside of the application.

**Aggregation in code:**

The `Inventory` class **aggregates** `Item` objects:

```python
class Inventory:
    def __init__(self):
        self._items: list[Item] = []  # Aggregation: items exist independently
```

Items can exist without an inventory — they are created externally and added via `add_item()`. If the inventory is cleared, the items are returned (not destroyed):

```python
def clear(self) -> list[Item]:
    items = list(self._items)
    self._items.clear()
    return items  # Items still exist after being removed
```

### 2.4 Reading from File and Writing to File

The `FileHandler` class implements JSON-based file I/O for character persistence:

```python
def save_character(self, character: Character) -> str:
    filepath = self._get_filepath(character.name)
    data = character.to_dict()
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return filepath

def load_character(self, character_name: str) -> Character:
    filepath = self._get_filepath(character_name)
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    return self._dict_to_character(data)
```

JSON was chosen because the character data is naturally nested (stats inside character, items inside inventory), which maps well to JSON's hierarchical structure. Each model class implements `to_dict()` and `from_dict()` methods for serialization and deserialization, ensuring a clean round-trip: save → load → identical object.

### 2.5 Testing

The project includes **63 unit tests** across 5 test files using Python's built-in `unittest` framework:

| Test File | Tests | What It Covers |
|---|---|---|
| `test_stats.py` | 17 | Stat validation, boundaries, modifiers, serialization |
| `test_inventory.py` | 12 | Add/remove items, weight limits, filtering, serialization |
| `test_builder.py` | 14 | Builder validation, method chaining, Director presets |
| `test_file_handler.py` | 9 | Save/load round-trips, listing, deletion |
| `test_character.py` | 11 | Character operations, polymorphism verification |

Example test demonstrating polymorphism verification:

```python
def test_different_hit_points(self):
    stats = Stats(constitution=14)
    warrior_hp = Warrior().calculate_hit_points(5, stats.get_modifier("CON"))
    mage_hp = Mage().calculate_hit_points(5, stats.get_modifier("CON"))
    rogue_hp = Rogue().calculate_hit_points(5, stats.get_modifier("CON"))
    self.assertGreater(warrior_hp, rogue_hp)
    self.assertGreater(rogue_hp, mage_hp)
```

All tests can be run with: `python -m unittest discover -s tests -v`

### 2.6 Code Style

The program follows PEP8 guidelines:

- **Naming:** `snake_case` for functions and variables, `PascalCase` for classes.
- **Docstrings:** Every class and public method has a descriptive docstring.
- **Type hints:** Parameters and return types are annotated throughout.
- **Line length:** Lines are kept under 100 characters.
- **Imports:** Organized by standard library, then project modules.
- **Project structure:** Code is organized into packages (`models/`, `builder/`, `utils/`, `tests/`) following Python application layout best practices.

---

## 3. Results and Summary

### 3.1 Results

- The application successfully creates, edits, saves, and loads DND character sheets through an interactive command-line interface.
- All four OOP pillars are implemented and demonstrated: encapsulation in `Stats`, abstraction in `CharacterClass`, inheritance in the four subclasses, and polymorphism in overridden methods like `calculate_hit_points()`.
- The Builder design pattern provides a clean, validated, step-by-step character creation process with method chaining and preset builds via the Director.
- File I/O with JSON allows full character persistence, including nested data like inventory items and abilities.
- All 63 unit tests pass, covering core functionality including edge cases and error handling.

### 3.2 Conclusions

This coursework resulted in a working DND Character Sheet Creator that covers the main OOP concepts in Python. The Builder pattern worked well for step-by-step character creation, and the character class hierarchy gave good examples of inheritance and polymorphism in action.

The hardest part was getting the serialization to work properly. Saving a character meant saving its stats, its inventory full of items, and its abilities — all nested inside each other. Loading it back had to rebuild everything in the right order. The Builder also took some thought, especially making sure it validated all required fields before building and resetting itself afterward, so it could be reused.

### 3.3 Future Prospects

The application could be extended in several ways:

- **Additional character classes**: adding Ranger, Paladin, Bard, etc. requires only creating new subclasses of `CharacterClass` and adding them to `CLASS_MAP`.
- **Graphical user interface**: replacing the CLI menu with a GUI using Tkinter or PyQt.
- **Dice rolling**: adding a dice roller for stat generation and combat simulation.
- **Party management**: managing a group of characters together with shared inventory.
- **Database storage**: replacing JSON files with SQLite for more robust data management.
- **Export formats**: exporting character sheets to PDF or HTML for printing.
