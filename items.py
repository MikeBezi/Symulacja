import random
import json
from datetime import datetime

class Item:
    def __init__(self, name, tier=1):
        self.name = name # nazwa przedmiotu
        self.tier = tier  # tier przedmiotu
        self.stats = {}  # statystyki przedmiotu
        self._generate_stats() # generuje statystyki na podstawie tieru
    
    def _generate_stats(self):
        """Generuje statystyki na podstawie tieru przedmiotu"""
        # Lista możliwych statystyk
        available_stats = ["strength", "dexterity", "hp", "speed", "dodge"]
        
        # Liczba statystyk na podstawie tieru
        num_stats = self.tier
        
        # Wybierz losowe statystyki - random.sample losuje 1 rzecz z listy
        selected_stats = random.sample(available_stats, num_stats)
        
        # Generuj wartości dla statystyk
        for stat in selected_stats:
            max_value = 2 if self.tier == 1 else 3
            # Tier 1: losuje statystyki z zakresu 1-2
            # Tier 2 i 3: losuje statystyki z zakresu 1-3
            
            self.stats[stat] = random.randint(1, max_value)
            #do statystyk dodaje losową wartość z zakresu 1-max_value
    
    def to_dict(self):
        """Konwertuje obiekt do słownika do zapisu w JSON"""
        return {
            "name": self.name,
            "tier": self.tier,
            "stats": self.stats
        }

class Weapon(Item):
    def __init__(self, name, tier=1):
        super().__init__(name, tier)


    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "weapon",
        })
        return data
    
class Armor(Item):
    def __init__(self, name, tier=1):
        super().__init__(name, tier)

    
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "armor",

        })
        return data

def generate_random_items(weapon_counts, armor_counts):
    items = []
    
    # Typy broni i zbroi do losowania
    weapon_types = [
        {"name": "Miecz", },
        {"name": "Topór", },
        {"name": "Łuk",  }
    ]
    
    armor_types = [
        {"name": "Zbroja skórzana", },
        {"name": "Kolczuga", },
        {"name": "Zbroja płytowa", }
    ]
    
    # Generowanie broni
    for tier, count in weapon_counts.items():
        for _ in range(count):
            weapon_base = random.choice(weapon_types)
            weapon = Weapon(
                name=f"{weapon_base['name']} (T{tier})",
                tier=tier
            )
            items.append(weapon)
    
    # Generowanie zbroi
    for tier, count in armor_counts.items():
        for _ in range(count):
            armor_base = random.choice(armor_types)
            armor = Armor(
                name=f"{armor_base['name']} (T{tier})",
                tier=tier
            )
            items.append(armor)
    
    return items

def save_items_to_file(items, filename="item_history.json"):
    # Konwersja obiektów do formatu słownika
    items_data = [item.to_dict() for item in items]
    
    # Dodanie znacznika czasu
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": items_data
    }
    
    # Zapis do pliku z formatowaniem i kodowaniem UTF-8
    with open(filename, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False) + "\n\n")

# Przykład użycia:
if __name__ == "__main__":
    # Określenie ile przedmiotów danego tieru wygenerować
    weapon_counts = {1: 10, 2: 7, 3: 3}  # 10 broni tier 1, 7 broni tier 2, 3 broni tier 3
    armor_counts = {1: 10, 2: 7, 3: 3}   # 10 zbroi tier 1, 7 zbroi tier 2, 3 zbroje tier 3
    
    # Generowanie przedmiotów
    generated_items = generate_random_items(weapon_counts, armor_counts)
    
    # Wyświetlanie wygenerowanych przedmiotów
    for item in generated_items:
        if isinstance(item, Weapon):
            print(f"{item.name}: Statystyki: {item.stats}")
        else:
            print(f"{item.name}: Statystyki: {item.stats}")
    
    # Zapisywanie do pliku
    save_items_to_file(generated_items)
    print(f"Zapisano {len(generated_items)} przedmiotów do pliku item_history.json")