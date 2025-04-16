#!/usr/bin/env python
"""
Skrypt do testowania różnych parametrów symulacji RPG.
Pozwala na dostosowanie liczby postaci, wyświetlanie szczegółów walk
i modyfikację innych parametrów.
"""
import sys
import os
import time
import argparse

# Dodanie ścieżki nadrzędnej do sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from rpg_mechanics.models.character import Character
from rpg_mechanics.models.equipment import create_weapon, create_armor
from rpg_mechanics.models.combat import CombatSystem
from rpg_mechanics.simulation.simulator import Simulator
from rpg_mechanics.simulation.statistics import StatisticsAnalyzer

def run_custom_simulation(num_characters=20, verbose=False, generate_plots=True, max_rounds=100):
    """Uruchamia symulację z niestandardowymi parametrami."""
    print("=" * 50)
    print("SYMULATOR MECHANIKI RPG - TESTOWANIE")
    print("=" * 50)
    print(f"\nParametry symulacji:")
    print(f"- Liczba bohaterów: {num_characters}")
    print(f"- Szczegóły walk: {'Tak' if verbose else 'Nie'}")
    print(f"- Generowanie wykresów: {'Tak' if generate_plots else 'Nie'}")
    print(f"- Maksymalna liczba rund: {max_rounds}")
    print("\nInicjalizacja systemu...")
    
    # Inicjalizacja symulatora
    simulator = Simulator(num_characters=num_characters, verbose=verbose)
    
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
    
    # Generowanie wykresów jeśli włączone
    if generate_plots:
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

def main():
    """Główna funkcja parsująca argumenty z linii poleceń."""
    parser = argparse.ArgumentParser(description='Testowanie symulacji RPG z różnymi parametrami.')
    parser.add_argument('-c', '--characters', type=int, default=20,
                        help='Liczba bohaterów (domyślnie: 20)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Wyświetl szczegóły walk')
    parser.add_argument('-np', '--no-plots', action='store_true',
                        help='Nie generuj wykresów')
    parser.add_argument('-r', '--rounds', type=int, default=100,
                        help='Maksymalna liczba rund w walce (domyślnie: 100)')
    args = parser.parse_args()
    
    run_custom_simulation(
        num_characters=args.characters,
        verbose=args.verbose,
        generate_plots=not args.no_plots,
        max_rounds=args.rounds
    )

if __name__ == "__main__":
    main() 