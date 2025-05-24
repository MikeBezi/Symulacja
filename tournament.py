import character_creator
import combat

def main():
    print("=== TURNIEJ RPG ===\n")
    
    # Etap 1: Tworzenie postaci
    print("ETAP 1: Tworzenie postaci...")
    char_list = character_creator.main()
    
    # Etap 2: Przygotowanie turnieju
    print("\nETAP 2: Przygotowanie turnieju...")
    print(f"Przygotowano {len(char_list)} wojowników do turnieju!")

    
    # Etap 3: Turniej
    print(f"\nETAP 3: START TURNIEJ!")
    print(f"Liczba walk: {len(char_list) * (len(char_list) - 1) // 2}")
    
    results = combat.run_tournament(char_list)
    
    # Etap 4: Statystyki
    print("\nETAP 4: Obliczanie statystyk...")
    statistics = combat.calculate_statistics(results)
    
    # Tworzenie mapowania nazw na obiekty postaci
    char_dict = {character.name: character for character in char_list}
    
    # Sortowanie wojowników według win_rate
    sorted_fighters = sorted(statistics.items(), key=lambda x: x[1]["win_rate"], reverse=True)
    
    print("\n=== RANKING WOJOWNIKÓW ===")
    for i, (fighter_name, stats) in enumerate(sorted_fighters, 1):
        character = char_dict[fighter_name]  # Pobierz obiekt postaci
        
        # Informacje o broni
        weapon_info = f"Broń: {character.weapon.name} {character.weapon.stats}" if hasattr(character, 'weapon') else "Broń: Brak"
        
        # Informacje o zbroi
        armor_info = f"Zbroja: {character.armor.name} {character.armor.stats}" if hasattr(character, 'armor') else "Zbroja: Brak"
        
        print(f"{i:2d}. {fighter_name} - STR={character.strength}, DEX={character.dexterity}, HP={character.hp}, SPD={character.speed}, DODGE={character.dodge}")
        print(f"    {weapon_info}")
        print(f"    {armor_info}")
        print(f"    Wygrane: {stats['wins']:2d}, Przegrane: {stats['losses']:2d}, Współczynnik: {stats['win_rate']:5.1f}%")
        print()
    
    # Etap 5: Zapis wyników
    print("\nETAP 5: Zapisywanie wyników...")
    combat.save_tournament_results(results, statistics)
    
    print("\n=== TURNIEJ ZAKOŃCZONY ===")
    print("Wyniki zapisane w tournament_results.json")
    print(f"Najlepszy wojownik: {sorted_fighters[0][0]} ({sorted_fighters[0][1]['win_rate']}% wygranych)")
