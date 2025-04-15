class Weapon:
    def __init__(self, name, damage, attack_speed, strength_bonus=0, dexterity_bonus=0):
        self.name = name
        self.damage = damage  # Bazowe obrażenia
        self.attack_speed = attack_speed  # Wpływa na częstotliwość ataków (1-10)
        self.strength_bonus = strength_bonus  # Bonus do siły
        self.dexterity_bonus = dexterity_bonus  # Bonus do zręczności
    
    def __str__(self):
        """Reprezentacja tekstowa broni."""
        return f"{self.name} (DMG:{self.damage}, SPD:{self.attack_speed})"


class Armor:
    def __init__(self, name, protection, dexterity_penalty=0, endurance_bonus=0):
        self.name = name
        self.protection = protection  # Redukcja obrażeń
        self.dexterity_penalty = dexterity_penalty  # Kara do zręczności
        self.endurance_bonus = endurance_bonus  # Bonus do wytrzymałości
    
    def __str__(self):
        """Reprezentacja tekstowa zbroi."""
        return f"{self.name} (PROT:{self.protection})"


# Funkcje do tworzenia gotowych przedmiotów

def create_weapon(weapon_type):
    """Tworzy broń określonego typu."""
    weapons = {
        "miecz": Weapon("Stalowy miecz", damage=10, attack_speed=5, strength_bonus=2),
        "topór": Weapon("Ciężki topór", damage=15, attack_speed=3, strength_bonus=3),
        "sztylet": Weapon("Ostry sztylet", damage=6, attack_speed=8, dexterity_bonus=3),
        "łuk": Weapon("Długi łuk", damage=8, attack_speed=6, dexterity_bonus=4),
        "włócznia": Weapon("Długa włócznia", damage=12, attack_speed=4, strength_bonus=1, dexterity_bonus=1),
        "młot": Weapon("Bojowy młot", damage=18, attack_speed=2, strength_bonus=4),
        "kostur": Weapon("Magiczny kostur", damage=7, attack_speed=5, intelligence_bonus=5),
        "katana": Weapon("Ostra katana", damage=11, attack_speed=7, dexterity_bonus=2),
        "dwuręczny miecz": Weapon("Dwuręczny miecz", damage=20, attack_speed=2, strength_bonus=5),
        "rapier": Weapon("Elegancki rapier", damage=8, attack_speed=9, dexterity_bonus=5)
    }
    
    return weapons.get(weapon_type, Weapon("Pięści", damage=3, attack_speed=6))


def create_armor(armor_type):
    """Tworzy zbroję określonego typu."""
    armors = {
        "lekka": Armor("Skórzana zbroja", protection=3, dexterity_penalty=0, endurance_bonus=1),
        "średnia": Armor("Kolczuga", protection=5, dexterity_penalty=1, endurance_bonus=2),
        "ciężka": Armor("Pełna płytowa", protection=10, dexterity_penalty=3, endurance_bonus=3),
        "tarcza": Armor("Wielka tarcza", protection=4, dexterity_penalty=1, endurance_bonus=1),
        "magiczna": Armor("Magiczna szata", protection=4, dexterity_penalty=0, endurance_bonus=2),
        "wzmocniona": Armor("Wzmocniona skóra", protection=4, dexterity_penalty=0, endurance_bonus=1),
        "legendarna": Armor("Legendarna zbroja", protection=12, dexterity_penalty=1, endurance_bonus=4),
        "mistrzowska": Armor("Mistrzowska kolczuga", protection=7, dexterity_penalty=0, endurance_bonus=2),
        "lekka płytowa": Armor("Lekka płytowa", protection=6, dexterity_penalty=1, endurance_bonus=2),
        "smocza": Armor("Smocza skóra", protection=8, dexterity_penalty=0, endurance_bonus=3)
    }
    
    return armors.get(armor_type, Armor("Ubranie", protection=1)) 