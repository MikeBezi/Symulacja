import items 
import characters
import random
import os
import json
from datetime import datetime

def equip_item(character, item):
    # Zwiększ statystyki postaci o wartości z przedmiotu
    for stat, value in item.stats.items():
        if hasattr(character, stat):
            current_value = getattr(character, stat)
            setattr(character, stat, current_value + value)
    
    # Dodaj atrybut z typem przedmiotu, jeśli go nie ma
    if isinstance(item, items.Weapon) and not hasattr(character, 'weapon'):
        character.weapon = item
    elif isinstance(item, items.Armor) and not hasattr(character, 'armor'):
        character.armor = item

# Przygotowanie danych do zapisu do pliku JSON
def character_to_dict(character):
    data = {
        "name": character.name,
        "class": character.__class__.__name__,
        "stats": {
            "strength": character.strength,
            "dexterity": character.dexterity,
            "hp": character.hp,
            "speed": character.speed,
            "dodge": character.dodge
        },
        "equipment": {
            "weapon": character.weapon.to_dict() if hasattr(character, 'weapon') else None,
            "armor": character.armor.to_dict() if hasattr(character, 'armor') else None
        }
    }
    return data

# Zapisanie postaci do pliku JSON
def save_characters(char_list, filename="character_data.json"):
    
    json_folder = "json"
    if not os.path.exists(json_folder):
       os.makedirs(json_folder)

    characters_data = [character_to_dict(character) for character in char_list]
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "characters": characters_data
    }
    
    filepath = os.path.join(json_folder, filename)
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False) + "\n\n")

def main():

    print("Rozpoczynam tworzenie postaci i przedmiotów...")
    
    # Generowanie postaci
    char_list = []
    character_classes = [characters.Warrior, characters.Hunter, characters.Rouge]
    names = ["Anna", "Bartek", "Cezary", "Dominika", "Eryk", "Filip", "Gosia", "Henryk", 
                "Irena", "Jakub", "Kamil", "Laura", "Marek", "Natalia", "Oliwia", "Piotr", 
                "Rafał", "Szymon", "Tomasz", "Wiktoria"]
    
    for i in range(20):
        # Wybierz klasę postaci
        char_class = character_classes[i % len(character_classes)]
        # Wybierz imię
        name = names[i]
        # Utwórz postać
        character = char_class(name)
        char_list.append(character)
    
    print(f"Utworzono {len(char_list)} postaci")
    
    # Generowanie przedmiotów (20 broni, 20 zbroi)
    all_weapons = items.generate_random_items({1: 10, 2: 7, 3: 3}, {})  # 10 broni tier 1, 7 broni tier 2, 3 broni tier 3
    all_armors = items.generate_random_items({}, {1: 10, 2: 7, 3: 3})   # 10 zbroi tier 1, 7 zbroi tier 2, 3 zbroje tier 3
    all_items = all_weapons + all_armors

    
    print(f"Wygenerowano {len(all_weapons)} broni i {len(all_armors)} zbroi")
    
    # Przypisywanie przedmiotów do postaci
    for i, character in enumerate(char_list):
        equip_item(character, all_weapons[i])
        equip_item(character, all_armors[i])
    
    # Wyświetlanie wyników
    for character in char_list:
        print(f"{character.name} ({character.__class__.__name__})")
        print(f"  Statystyki: STR={character.strength}, DEX={character.dexterity}, HP={character.hp}, SPD={character.speed}, DODGE={character.dodge}")
        if hasattr(character, 'weapon'):
            print(f"  Broń: {character.weapon.name} (Statystyki: {character.weapon.stats})")
        if hasattr(character, 'armor'):
            print(f"  Zbroja: {character.armor.name} (Statystyki: {character.armor.stats})")
        print()
    
    # Zapisanie przedmiotów do pliku JSON
    items.save_items_to_file(all_items)
    print(f"Zapisano {len(all_items)} przedmiotów do pliku item_history.json")
    
    # Zapisanie postaci do pliku JSON
    save_characters(char_list)
    print(f"Zapisano {len(char_list)} postaci do pliku character_data.json")
    
    return char_list