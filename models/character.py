import random

class Character:
    def __init__(self, name, strength, dexterity, intelligence, endurance):
        self.name = name
        self.strength = strength  # Wpływa na obrażenia w walce wręcz
        self.dexterity = dexterity  # Wpływa na celność i uniki
        self.intelligence = intelligence  # Wpływa na efektywność umiejętności
        self.endurance = endurance  # Wpływa na maksymalne punkty życia
        
        # Pochodne atrybuty
        self.max_health = 50 + (endurance * 10)
        self.current_health = self.max_health
        self.fatigue = 0  # Zmęczenie, zwiększa się podczas walki
        
        # Ekwipunek
        self.weapon = None
        self.armor = None
        
        # Statystyki walk
        self.wins = 0
        self.losses = 0
        self.total_fights = 0
    
    def reset_for_combat(self):
        """Resetuje postać przed walką."""
        self.current_health = self.max_health
        self.fatigue = 0
    
    def attack(self, target):
        """Wykonuje atak na cel."""
        # Sprawdzenie zmęczenia
        if self.fatigue >= 100:
            self.fatigue -= 5  # Odpoczywa trochę
            return {"hit": False, "damage": 0, "critical": False, "message": f"{self.name} jest zbyt zmęczony, aby atakować!"}
        
        # Obliczenie bazowych obrażeń
        base_damage = self.weapon.damage if self.weapon else self.strength / 2
        
        # Szansa na trafienie zależna od zręczności
        hit_chance = 0.5 + (self.dexterity * 0.03) - (target.dexterity * 0.01)
        hit_chance = min(0.95, max(0.10, hit_chance))  # Ograniczenie szansy od 10% do 95%
        
        # Sprawdzenie czy atak trafił
        hit = random.random() <= hit_chance
        if not hit:
            self.fatigue += 5  # Zwiększenie zmęczenia po chybionym ataku
            return {"hit": False, "damage": 0, "critical": False, "message": f"{self.name} chybił!"}
        
        # Obliczenie obrażeń
        damage_multiplier = 1.0
        
        # Wpływ siły na obrażenia
        strength_bonus = self.strength * 0.5
        
        # Wpływ zmęczenia na obrażenia
        fatigue_penalty = self.fatigue * 0.005  # 0.5% kary za każdy punkt zmęczenia
        
        # Szansa na trafienie krytyczne
        critical_chance = 0.05 + (self.dexterity * 0.01)
        critical = random.random() <= critical_chance
        if critical:
            damage_multiplier = 2.0
        
        # Ostateczne obrażenia
        raw_damage = (base_damage + strength_bonus) * damage_multiplier * (1 - fatigue_penalty)
        
        # Redukcja obrażeń przez zbroję celu
        if target.armor:
            armor_reduction = target.armor.protection
            damage = max(1, raw_damage - armor_reduction)  # Minimum 1 obrażenie
        else:
            damage = max(1, raw_damage)
        
        # Zaokrąglenie obrażeń
        damage = round(damage)
        
        # Zwiększenie zmęczenia po ataku
        self.fatigue += 10
        
        # Aplikacja obrażeń
        target.current_health -= damage
        
        # Przygotowanie odpowiedzi
        message = f"{self.name} trafia {target.name} za {damage} obrażeń"
        if critical:
            message += " (trafienie krytyczne!)"
        
        return {
            "hit": True,
            "damage": damage,
            "critical": critical,
            "message": message
        }
    
    def is_alive(self):
        """Sprawdza czy postać żyje."""
        return self.current_health > 0
    
    def get_win_probability(self):
        """Oblicza prawdopodobieństwo zwycięstwa na podstawie historii walk."""
        if self.total_fights == 0:
            return 0
        return self.wins / self.total_fights
    
    def __str__(self):
        """Reprezentacja tekstowa postaci."""
        return f"{self.name} (STR:{self.strength}, DEX:{self.dexterity}, INT:{self.intelligence}, END:{self.endurance})" 