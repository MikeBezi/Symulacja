import matplotlib.pyplot as plt
import numpy as np

class StatisticsAnalyzer:
    def __init__(self, simulator):
        self.simulator = simulator
        self.characters = simulator.characters
        self.results = simulator.results
    
    def analyze_win_rates(self):
        """Analizuje współczynniki zwycięstw postaci."""
        win_rates = {}
        for character in self.characters:
            if character.total_fights > 0:
                win_rate = character.wins / character.total_fights
            else:
                win_rate = 0
            win_rates[character.name] = win_rate
        
        return win_rates
    
    def analyze_attribute_correlation(self):
        """Analizuje korelację między atrybutami a zwycięstwami."""
        strengths = [char.strength for char in self.characters]
        dexterities = [char.dexterity for char in self.characters]
        intelligences = [char.intelligence for char in self.characters]
        endurances = [char.endurance for char in self.characters]
        win_rates = [char.wins / char.total_fights if char.total_fights > 0 else 0 for char in self.characters]
        
        # Obliczamy korelację Pearsona
        strength_corr = np.corrcoef(strengths, win_rates)[0, 1]
        dexterity_corr = np.corrcoef(dexterities, win_rates)[0, 1]
        intelligence_corr = np.corrcoef(intelligences, win_rates)[0, 1]
        endurance_corr = np.corrcoef(endurances, win_rates)[0, 1]
        
        return {
            "siła": strength_corr,
            "zręczność": dexterity_corr,
            "inteligencja": intelligence_corr,
            "wytrzymałość": endurance_corr
        }
    
    def analyze_weapon_effectiveness(self):
        """Analizuje skuteczność różnych typów broni."""
        weapon_stats = {}
        
        for character in self.characters:
            weapon_name = character.weapon.name if character.weapon else "Brak broni"
            if weapon_name not in weapon_stats:
                weapon_stats[weapon_name] = {
                    "wins": 0,
                    "losses": 0,
                    "total": 0
                }
            
            weapon_stats[weapon_name]["wins"] += character.wins
            weapon_stats[weapon_name]["losses"] += character.losses
            weapon_stats[weapon_name]["total"] += character.total_fights
        
        # Obliczamy współczynnik zwycięstw dla każdej broni
        weapon_win_rates = {}
        for weapon_name, stats in weapon_stats.items():
            if stats["total"] > 0:
                win_rate = stats["wins"] / stats["total"]
            else:
                win_rate = 0
            weapon_win_rates[weapon_name] = win_rate
        
        return weapon_win_rates
    
    def analyze_armor_effectiveness(self):
        """Analizuje skuteczność różnych typów zbroi."""
        armor_stats = {}
        
        for character in self.characters:
            armor_name = character.armor.name if character.armor else "Brak zbroi"
            if armor_name not in armor_stats:
                armor_stats[armor_name] = {
                    "wins": 0,
                    "losses": 0,
                    "total": 0
                }
            
            armor_stats[armor_name]["wins"] += character.wins
            armor_stats[armor_name]["losses"] += character.losses
            armor_stats[armor_name]["total"] += character.total_fights
        
        # Obliczamy współczynnik zwycięstw dla każdej zbroi
        armor_win_rates = {}
        for armor_name, stats in armor_stats.items():
            if stats["total"] > 0:
                win_rate = stats["wins"] / stats["total"]
            else:
                win_rate = 0
            armor_win_rates[armor_name] = win_rate
        
        return armor_win_rates
    
    def plot_win_probabilities(self, save_path=None):
        """Generuje wykres prawdopodobieństw zwycięstwa dla każdej postaci."""
        win_rates = self.analyze_win_rates()
        
        # Sortowanie wg prawdopodobieństwa zwycięstwa
        sorted_win_rates = sorted(win_rates.items(), key=lambda x: x[1], reverse=True)
        names = [item[0] for item in sorted_win_rates]
        probabilities = [item[1] for item in sorted_win_rates]
        
        plt.figure(figsize=(12, 8))
        plt.bar(names, probabilities)
        plt.xlabel('Bohater')
        plt.ylabel('Prawdopodobieństwo zwycięstwa')
        plt.title('Prawdopodobieństwo zwycięstwa dla każdego bohatera')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"Wykres zapisany jako {save_path}")
        else:
            plt.show()
    
    def plot_attribute_correlation(self, save_path=None):
        """Generuje wykres korelacji atrybutów ze zwycięstwami."""
        correlations = self.analyze_attribute_correlation()
        
        attributes = list(correlations.keys())
        correlation_values = list(correlations.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(attributes, correlation_values)
        plt.xlabel('Atrybut')
        plt.ylabel('Korelacja z prawdopodobieństwem zwycięstwa')
        plt.title('Wpływ atrybutów na prawdopodobieństwo zwycięstwa')
        plt.axhline(y=0, color='r', linestyle='-')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"Wykres zapisany jako {save_path}")
        else:
            plt.show()
    
    def generate_comprehensive_report(self):
        """Generuje kompleksowy raport z analizy wyników."""
        print("\n=== RAPORT Z SYMULACJI WALK RPG ===\n")
        
        # Wyświetlenie informacji o postaciach
        print(f"Liczba bohaterów: {len(self.characters)}")
        print(f"Liczba przeprowadzonych walk: {len(self.results)}")
        
        # Analiza współczynników zwycięstw
        win_rates = self.analyze_win_rates()
        print("\nNAJLEPSI BOHATEROWIE:")
        sorted_win_rates = sorted(win_rates.items(), key=lambda x: x[1], reverse=True)
        for i, (name, win_rate) in enumerate(sorted_win_rates[:5], 1):
            character = next(c for c in self.characters if c.name == name)
            print(f"{i}. {name} - {win_rate:.2%} zwycięstw")
            print(f"   {character}")
            print(f"   Broń: {character.weapon}")
            print(f"   Zbroja: {character.armor}")
        
        # Korelacja atrybutów ze zwycięstwami
        correlations = self.analyze_attribute_correlation()
        print("\nKORELACJA ATRYBUTÓW ZE ZWYCIĘSTWAMI:")
        sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
        for attribute, correlation in sorted_correlations:
            print(f"{attribute}: {correlation:.3f}")
        
        # Wpływ najsilniejszego atrybutu
        strongest_attribute = sorted_correlations[0][0]
        correlation_value = sorted_correlations[0][1]
        if correlation_value > 0:
            print(f"\nNajwiększy wpływ na wyniki walk ma atrybut: {strongest_attribute} (korelacja: {correlation_value:.3f})")
            print(f"Wyższa wartość {strongest_attribute} znacząco zwiększa szanse na zwycięstwo.")
        else:
            print(f"\nNajwiększy wpływ na wyniki walk ma atrybut: {strongest_attribute} (korelacja: {correlation_value:.3f})")
            print(f"Niższa wartość {strongest_attribute} zwiększa szanse na zwycięstwo, co jest zaskakującym wynikiem.")
        
        # Analiza skuteczności broni
        weapon_effectiveness = self.analyze_weapon_effectiveness()
        print("\nSKUTECZNOŚĆ BRONI:")
        sorted_weapons = sorted(weapon_effectiveness.items(), key=lambda x: x[1], reverse=True)
        for weapon_name, win_rate in sorted_weapons:
            print(f"{weapon_name}: {win_rate:.2%}")
        
        # Analiza skuteczności zbroi
        armor_effectiveness = self.analyze_armor_effectiveness()
        print("\nSKUTECZNOŚĆ ZBROI:")
        sorted_armors = sorted(armor_effectiveness.items(), key=lambda x: x[1], reverse=True)
        for armor_name, win_rate in sorted_armors:
            print(f"{armor_name}: {win_rate:.2%}")
        
        # Sugestie balansu
        print("\nSUGESTIE DOTYCZĄCE BALANSU GRY:")
        
        # Najsilniejsza i najsłabsza broń
        strongest_weapon = sorted_weapons[0][0]
        weakest_weapon = sorted_weapons[-1][0]
        print(f"- Najsilniejsza broń: {strongest_weapon} (wsp. zwycięstw: {sorted_weapons[0][1]:.2%})")
        print(f"- Najsłabsza broń: {weakest_weapon} (wsp. zwycięstw: {sorted_weapons[-1][1]:.2%})")
        
        # Najsilniejsza i najsłabsza zbroja
        strongest_armor = sorted_armors[0][0]
        weakest_armor = sorted_armors[-1][0]
        print(f"- Najsilniejsza zbroja: {strongest_armor} (wsp. zwycięstw: {sorted_armors[0][1]:.2%})")
        print(f"- Najsłabsza zbroja: {weakest_armor} (wsp. zwycięstw: {sorted_armors[-1][1]:.2%})")
        
        # Wnioski końcowe
        print("\nWNIOSKI KOŃCOWE:")
        
        # Wnioski oparte na najważniejszym atrybucie
        print(f"1. Atrybut {strongest_attribute} ma największy wpływ na wynik walki.")
        
        # Wnioski dotyczące wyposażenia
        print(f"2. Kombinacja {strongest_weapon} i {strongest_armor} daje największe szanse na zwycięstwo.")
        
        # Sugestie dotyczące balansu
        if max(weapon_effectiveness.values()) - min(weapon_effectiveness.values()) > 0.3:
            print("3. System broni wymaga zbalansowania - różnice między najsilniejszą a najsłabszą bronią są zbyt duże.")
        else:
            print("3. System broni jest relatywnie dobrze zbalansowany.")
        
        if max(armor_effectiveness.values()) - min(armor_effectiveness.values()) > 0.3:
            print("4. System zbroi wymaga zbalansowania - różnice między najsilniejszą a najsłabszą zbroją są zbyt duże.")
        else:
            print("4. System zbroi jest relatywnie dobrze zbalansowany.") 