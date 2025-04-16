import random
from rpg_mechanics.models.character import Character
from rpg_mechanics.models.equipment import create_weapon, create_armor
from rpg_mechanics.models.combat import CombatSystem

class Simulator:
    def __init__(self, num_characters=20, verbose=False):
        self.num_characters = num_characters
        self.characters = []
        self.combat_system = CombatSystem(verbose=verbose)
        self.results = {}
        self.verbose = verbose
    
    def generate_characters(self):
        """Generuje bohaterów z losowymi atrybutami i ekwipunkiem."""
        names = [
            "Aragorn", "Geralt", "Legolas", "Gimli", "Gandalf",
            "Xena", "Conan", "Achilles", "Spartakus", "Thorgal",
            "Merlin", "Arya", "Drizzt", "Galadriel", "Boromir",
            "Zoltan", "Triss", "Yennefer", "Ciri", "Jaskier",
            "Guts", "Griffith", "Casca", "Thrall", "Jaina",
            "Arthas", "Illidan", "Tyrande", "Neria", "Zevran"
        ]
        
        weapon_types = [
            "miecz", "topór", "sztylet", "łuk", "włócznia",
            "młot", "kostur", "katana", "dwuręczny miecz", "rapier"
        ]
        
        armor_types = [
            "lekka", "średnia", "ciężka", "tarcza", "magiczna",
            "wzmocniona", "legendarna", "mistrzowska", "lekka płytowa", "smocza"
        ]
        
        # Wylosuj unikalne imiona dla postaci
        selected_names = random.sample(names, self.num_characters)
        
        # Generuj postacie
        for i in range(self.num_characters):
            name = selected_names[i]
            
            # Losuj atrybuty (5-15)
            strength = random.randint(5, 15)
            dexterity = random.randint(5, 15)
            intelligence = random.randint(5, 15)
            endurance = random.randint(5, 15)
            
            # Utwórz postać
            character = Character(name, strength, dexterity, intelligence, endurance)
            
            # Wyposażenie postaci
            weapon_type = random.choice(weapon_types)
            armor_type = random.choice(armor_types)
            
            character.weapon = create_weapon(weapon_type)
            character.armor = create_armor(armor_type)
            
            self.characters.append(character)
            
        if self.verbose:
            print(f"Wygenerowano {self.num_characters} bohaterów.")
            for i, character in enumerate(self.characters):
                print(f"{i+1}. {character}")
                print(f"   Broń: {character.weapon}")
                print(f"   Zbroja: {character.armor}")
    
    def run_all_vs_all_tournament(self):
        """Przeprowadza turniej każdy z każdym."""
        if len(self.characters) < 2:
            print("Za mało bohaterów do przeprowadzenia symulacji!")
            return
        
        if self.verbose:
            print("\n=== ROZPOCZYNAMY TURNIEJ (KAŻDY Z KAŻDYM) ===\n")
        
        # Licznik walk
        total_fights = 0
        expected_fights = (self.num_characters * (self.num_characters - 1)) // 2
        
        # Przeprowadzamy walki każdy z każdym
        for i in range(len(self.characters)):
            for j in range(i + 1, len(self.characters)):
                char1 = self.characters[i]
                char2 = self.characters[j]
                
                # Przeprowadź walkę
                result = self.combat_system.simulate_combat(char1, char2)
                
                # Zapisz wynik walki
                fight_id = f"{char1.name}_vs_{char2.name}"
                self.results[fight_id] = result
                
                total_fights += 1
                if self.verbose:
                    print(f"Postęp: {total_fights}/{expected_fights} walk")
        
        if self.verbose:
            print(f"\nPrzeprowadzono {total_fights} walk.")
    
    def calculate_win_probabilities(self):
        """Oblicza prawdopodobieństwo zwycięstwa dla każdej postaci."""
        win_probabilities = {}
        
        for character in self.characters:
            win_prob = character.get_win_probability()
            win_probabilities[character.name] = win_prob
        
        return win_probabilities
    
    def get_character_rankings(self):
        """Zwraca ranking postaci wg. liczby zwycięstw."""
        # Sortowanie postaci wg liczby zwycięstw (malejąco)
        ranked_characters = sorted(
            self.characters,
            key=lambda c: (c.wins, c.current_health),
            reverse=True
        )
        
        return ranked_characters
    
    def print_tournament_results(self):
        """Wyświetla wyniki turnieju."""
        if not self.results:
            print("Brak wyników do wyświetlenia.")
            return
        
        print("\n=== WYNIKI TURNIEJU ===\n")
        
        # Ranking postaci
        ranked_characters = self.get_character_rankings()
        
        print("RANKING BOHATERÓW:")
        for i, char in enumerate(ranked_characters):
            win_rate = char.wins / char.total_fights if char.total_fights > 0 else 0
            print(f"{i+1}. {char.name} - Zwycięstwa: {char.wins}/{char.total_fights} ({win_rate:.2%})")
            print(f"   {char}")
            print(f"   Broń: {char.weapon}")
            print(f"   Zbroja: {char.armor}")
        
        # Oblicz prawdopodobieństwa zwycięstw
        win_probabilities = self.calculate_win_probabilities()
        
        print("\nPRAWDOPODOBIEŃSTWO ZWYCIĘSTWA:")
        sorted_probabilities = sorted(
            win_probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for name, probability in sorted_probabilities:
            print(f"{name}: {probability:.2%}")
        
        print("\nANALIZA ATRYBUTÓW ZWYCIĘZCÓW:")
        
        # Obliczanie średnich atrybutów dla najlepszych i najgorszych bohaterów
        top_half = ranked_characters[:len(ranked_characters)//2]
        bottom_half = ranked_characters[len(ranked_characters)//2:]
        
        avg_str_top = sum(c.strength for c in top_half) / len(top_half)
        avg_dex_top = sum(c.dexterity for c in top_half) / len(top_half)
        avg_int_top = sum(c.intelligence for c in top_half) / len(top_half)
        avg_end_top = sum(c.endurance for c in top_half) / len(top_half)
        
        avg_str_bottom = sum(c.strength for c in bottom_half) / len(bottom_half)
        avg_dex_bottom = sum(c.dexterity for c in bottom_half) / len(bottom_half)
        avg_int_bottom = sum(c.intelligence for c in bottom_half) / len(bottom_half)
        avg_end_bottom = sum(c.endurance for c in bottom_half) / len(bottom_half)
        
        print(f"Średnie atrybuty najlepszych bohaterów:")
        print(f"Siła: {avg_str_top:.2f}, Zręczność: {avg_dex_top:.2f}, Inteligencja: {avg_int_top:.2f}, Wytrzymałość: {avg_end_top:.2f}")
        
        print(f"Średnie atrybuty najgorszych bohaterów:")
        print(f"Siła: {avg_str_bottom:.2f}, Zręczność: {avg_dex_bottom:.2f}, Inteligencja: {avg_int_bottom:.2f}, Wytrzymałość: {avg_end_bottom:.2f}")
        
        # Analiza korelacji
        print("\nWNIOSKI:")
        
        attributes = ["siły", "zręczności", "inteligencji", "wytrzymałości"]
        avg_top = [avg_str_top, avg_dex_top, avg_int_top, avg_end_top]
        avg_bottom = [avg_str_bottom, avg_dex_bottom, avg_int_bottom, avg_end_bottom]
        
        # Znajdujemy atrybuty z największą różnicą między najlepszymi i najgorszymi
        diffs = [top - bottom for top, bottom in zip(avg_top, avg_bottom)]
        max_diff_index = diffs.index(max(diffs))
        
        print(f"Największy wpływ na wynik walk ma wartość {attributes[max_diff_index]}.")
        print(f"Analiza pokazuje, że bohaterowie z wyższymi wartościami {attributes[max_diff_index]} mają znacznie większe szanse na zwycięstwo.") 