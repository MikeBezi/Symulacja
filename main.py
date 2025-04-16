import os
import time
from rpg_mechanics.models.character import Character
from rpg_mechanics.models.equipment import create_weapon, create_armor
from rpg_mechanics.models.combat import CombatSystem
from rpg_mechanics.simulation.simulator import Simulator
from rpg_mechanics.simulation.statistics import StatisticsAnalyzer

def main():
    """Główna funkcja programu."""
    print("=" * 50)
    print("SYMULATOR MECHANIKI RPG")
    print("=" * 50)
    print("\nInicjalizacja systemu...")
    
    # Parametry symulacji
    num_characters = 20
    verbose_mode = False  # Czy wyświetlać szczegóły każdej walki
    
    # Inicjalizacja symulatora
    simulator = Simulator(num_characters=num_characters, verbose=verbose_mode)
    
    print(f"Generowanie {num_characters} bohaterów...")
    simulator.generate_characters()
    
    print("\nRozpoczynanie turnieju (każdy z każdym)...")
    start_time = time.time()
    simulator.run_all_vs_all_tournament()
    end_time = time.time()
    
    print(f"Symulacja zakończona w {end_time - start_time:.2f} sekund!")
    
    # Wyświetlenie wyników
    simulator.print_tournament_results()
    
    # Szczegółowa analiza statystyczna
    print("\nGenerowanie statystyk i wykresów...")
    stats_analyzer = StatisticsAnalyzer(simulator)
    
    # Sprawdzenie czy jest możliwość tworzenia wykresów
    try:
        # Tworzenie katalogu na wykresy jeśli nie istnieje
        os.makedirs("rpg_mechanics/results", exist_ok=True)
        
        # Generowanie wykresów
        stats_analyzer.plot_win_probabilities("rpg_mechanics/results/win_probabilities.png")
        stats_analyzer.plot_attribute_correlation("rpg_mechanics/results/attribute_correlation.png")
        print("Wykresy zostały zapisane w katalogu 'rpg_mechanics/results/'")
    except Exception as e:
        print(f"Nie udało się wygenerować wykresów: {e}")
    
    # Generowanie szczegółowego raportu
    print("\nGenerowanie szczegółowego raportu...")
    stats_analyzer.generate_comprehensive_report()
    
    print("\nSymulacja zakończona!")

if __name__ == "__main__":
    main() 