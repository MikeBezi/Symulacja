import random
import json
from datetime import datetime
from itertools import combinations
import character_creator
import os

class Combat:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.combat_log = []
        self.winner = None
        self.loser = None
    
    def reset_fighters(self):

        # Zapisujemy oryginalne HP (z ekwipunkiem)
        self.fighter1.max_hp = self.fighter1.hp
        self.fighter2.max_hp = self.fighter2.hp

        # Resetujemy current_hp na maksymalne
        self.fighter1.current_hp = self.fighter1.hp
        self.fighter2.current_hp = self.fighter2.hp
    
    def determine_turn_order(self):
        if self.fighter1.speed >= self.fighter2.speed:
            return self.fighter1, self.fighter2
        else:
            return self.fighter2, self.fighter1
    
    def attempt_hit(self, attacker, defender):
        # Sprawdzanie czy atak trafia na podstawie dexterity
        hit_roll = random.randint(1, 10)
        hit_success = hit_roll <= attacker.dexterity
        
        if not hit_success:
            message = f"{attacker.name} chybił! (potrzebował {attacker.dexterity} lub mniej, wyrzucił {hit_roll})"
            self.combat_log.append(message)
            return False
        
        # Sprawdzenie uniku obrońcy
        dodge_roll = random.randint(1, 10)
        dodge_success = dodge_roll <= defender.dodge
        
        if dodge_success:
            message = f"{defender.name} uniknął ataku {attacker.name}! (potrzebował {defender.dodge} lub mniej, wyrzucił {dodge_roll})"
            self.combat_log.append(message)
            return False
        
        return True
    
    def deal_damage(self, attacker, defender):
        damage = attacker.strength
        defender.current_hp -= damage
        
        message = f"{attacker.name} zadaje {damage} obrażeń {defender.name}! HP: {defender.current_hp}/{defender.max_hp}"
        self.combat_log.append(message)
        
        return damage
    
    def is_fighter_alive(self, fighter):
        return fighter.current_hp > 0
    
    def single_turn(self, attacker, defender):
        if self.attempt_hit(attacker, defender):
            self.deal_damage(attacker, defender)
            
            if not self.is_fighter_alive(defender):
                self.winner = attacker
                self.loser = defender
                message = f"{defender.name} został pokonany! {attacker.name} wygrywa!"
                self.combat_log.append(message)
                return True  # Walka zakończona
        
        return False  # Walka trwa
    
    def fight(self):
        self.reset_fighters()
        
        first_attacker, second_attacker = self.determine_turn_order()
        
        self.combat_log.append(f"WALKA: {self.fighter1.name} vs {self.fighter2.name}")
        self.combat_log.append(f"Kolejność: {first_attacker.name} (SPD:{first_attacker.speed}) -> {second_attacker.name} (SPD:{second_attacker.speed})")
        
        turn_count = 0
        
        while turn_count:
            turn_count += 1
            self.combat_log.append(f"\n--- TURA {turn_count} ---")
            
            # Atak pierwszego wojownika
            if self.single_turn(first_attacker, second_attacker):
                break
            
            # Atak drugiego wojownika (jeśli pierwszy nie zakończył walki)
            if self.single_turn(second_attacker, first_attacker):
                break
        

            if self.fighter1.current_hp > self.fighter2.current_hp:
                self.winner = self.fighter1
                self.loser = self.fighter2
            else:
                self.winner = self.fighter2
                self.loser = self.fighter1

        
        return {
            "fighter1": self.fighter1.name,
            "fighter2": self.fighter2.name,
            "winner": self.winner.name,
            "loser": self.loser.name,
            "turns": turn_count,
            "final_hp": {
                self.fighter1.name: self.fighter1.current_hp,
                self.fighter2.name: self.fighter2.current_hp
            },
            "combat_log": self.combat_log.copy()
        }

def generate_fight_pairs(characters):
    return list(combinations(characters, 2))

def run_tournament(characters):
    fight_pairs = generate_fight_pairs(characters)
    results = []
    
    print(f"Rozpoczynam turniej! Liczba walk: {len(fight_pairs)}")
    
    for i, (fighter1, fighter2) in enumerate(fight_pairs, 1):
        print(f"Walka {i}/{len(fight_pairs)}: {fighter1.name} vs {fighter2.name}")
        
        combat = Combat(fighter1, fighter2)
        result = combat.fight()
        results.append(result)
    
    return results

def calculate_statistics(results):
    # Oblicza statystyki turnieu
    fighter_stats = {}
    
    for result in results:
        fighter1 = result["fighter1"]
        fighter2 = result["fighter2"]
        winner = result["winner"]
        
        # Inicjalizacja statystyk
        for fighter in [fighter1, fighter2]:
            if fighter not in fighter_stats:
                fighter_stats[fighter] = {
                    "fights": 0,
                    "wins": 0,
                    "losses": 0,
                }
        
        # Aktualizacja statystyk
        fighter_stats[fighter1]["fights"] += 1
        fighter_stats[fighter2]["fights"] += 1
        
        if winner == fighter1:
            fighter_stats[fighter1]["wins"] += 1
            fighter_stats[fighter2]["losses"] += 1
        elif winner == fighter2:
            fighter_stats[fighter2]["wins"] += 1
            fighter_stats[fighter1]["losses"] += 1
    
    # Oblicz współczynnik wygranych
    for fighter, stats in fighter_stats.items():
        if stats["fights"] > 0:
            stats["win_rate"] = round(stats["wins"] / stats["fights"] * 100, 2)
        else:
            stats["win_rate"] = 0
    
    return fighter_stats

def save_tournament_results(results, statistics, filename="tournament_results.json"):
      
    json_folder = "json"
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_fights": len(results),
        "statistics": statistics,
        "detailed_results": results
    }
    
    filepath = os.path.join(json_folder, filename)
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False) + "\n\n")

