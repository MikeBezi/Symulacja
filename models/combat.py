import random
import time
from rpg_mechanics.models.character import Character

class CombatSystem:
    def __init__(self, verbose=True):
        self.verbose = verbose  # Czy wyświetlać szczegóły walki
    
    def simulate_combat(self, character1, character2, max_rounds=100):
        """Symuluje walkę między dwiema postaciami."""
        if self.verbose:
            print(f"\n=== WALKA: {character1.name} vs {character2.name} ===")
            print(f"{character1}")
            print(f"  Broń: {character1.weapon}")
            print(f"  Zbroja: {character1.armor}")
            print(f"{character2}")
            print(f"  Broń: {character2.weapon}")
            print(f"  Zbroja: {character2.armor}")
            print("\n--- Początek walki ---")
        
        # Przygotowanie postaci do walki
        character1.reset_for_combat()
        character2.reset_for_combat()
        
        # Statystyki walki
        rounds = 0
        combat_log = []
        
        # Główna pętla walki
        while character1.is_alive() and character2.is_alive() and rounds < max_rounds:
            rounds += 1
            
            # Losowe ustalenie kto atakuje pierwszy w tej rundzie (zależne od zręczności)
            initiative_c1 = random.random() * character1.dexterity
            initiative_c2 = random.random() * character2.dexterity
            
            # Ustalenie kolejności ataków
            if initiative_c1 >= initiative_c2:
                first, second = character1, character2
            else:
                first, second = character2, character1
            
            # Pierwsza postać atakuje
            attack_result = first.attack(second)
            if self.verbose:
                print(f"Runda {rounds}: {attack_result['message']}")
            combat_log.append(attack_result['message'])
            
            # Sprawdzenie czy druga postać żyje
            if not second.is_alive():
                if self.verbose:
                    print(f"{second.name} poległ!")
                break
            
            # Druga postać atakuje
            attack_result = second.attack(first)
            if self.verbose:
                print(f"Runda {rounds}: {attack_result['message']}")
            combat_log.append(attack_result['message'])
            
            # Sprawdzenie czy pierwsza postać żyje
            if not first.is_alive():
                if self.verbose:
                    print(f"{first.name} poległ!")
                break
            
            # Jeśli włączony tryb verbose, dodaj krótkie opóźnienie dla czytelności
            if self.verbose:
                time.sleep(0.05)
        
        # Określenie zwycięzcy
        if not character1.is_alive() and not character2.is_alive():
            winner = None
            if self.verbose:
                print("Obaj bohaterowie polegli!")
        elif not character1.is_alive():
            winner = character2
            if self.verbose:
                print(f"Zwycięzca: {character2.name}!")
        elif not character2.is_alive():
            winner = character1
            if self.verbose:
                print(f"Zwycięzca: {character1.name}!")
        else:
            # Limit rund - określenie zwycięzcy na podstawie pozostałych punktów życia
            if character1.current_health > character2.current_health:
                winner = character1
                if self.verbose:
                    print(f"Limit rund - zwycięzca na punkty: {character1.name}!")
            elif character2.current_health > character1.current_health:
                winner = character2
                if self.verbose:
                    print(f"Limit rund - zwycięzca na punkty: {character2.name}!")
            else:
                winner = None
                if self.verbose:
                    print("Remis!")
        
        # Aktualizacja statystyk postaci
        if winner == character1:
            character1.wins += 1
            character2.losses += 1
        elif winner == character2:
            character2.wins += 1
            character1.losses += 1
        
        character1.total_fights += 1
        character2.total_fights += 1
        
        # Przygotowanie wyniku walki
        result = {
            "winner": winner,
            "rounds": rounds,
            "character1_health": character1.current_health,
            "character2_health": character2.current_health,
            "combat_log": combat_log
        }
        
        return result 