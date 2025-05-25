import character_creator
import combat
import json
import os
from datetime import datetime

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
    
    # ETAP 6: Aktualizacja podsumowania turnieju
    print("Aktualizowanie podsumowania turnieju...")
    update_tournament_summary(char_list, statistics)
    
    print("\n=== TURNIEJ ZAKOŃCZONY ===")
    print("Wyniki zapisane w tournament_results.json")
    print(f"Najlepszy wojownik: {sorted_fighters[0][0]} ({sorted_fighters[0][1]['win_rate']}% wygranych)")

def update_tournament_summary(char_list, statistics):

    json_folder = "json"
    filename = "tournament_summary.json"
    filepath = os.path.join(json_folder, filename)
    
    # Wczytaj istniejące dane lub stwórz nowe
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                summary_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            summary_data = {"total_tournaments": 0, "fighters": {}}
    else:
        summary_data = {"total_tournaments": 0, "fighters": {}}
    
    # Zwiększ licznik turnieji
    summary_data["total_tournaments"] += 1
    summary_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Aktualizuj dane dla każdej postaci
    for character in char_list:
        fighter_name = character.name
        
        # Pobierz statystyki z turnieju
        fighter_stats = statistics.get(fighter_name, {"wins": 0, "losses": 0, "fights": 0})
        
        # Jeśli postać nie istnieje w podsumowaniu, dodaj ją
        if fighter_name not in summary_data["fighters"]:
            summary_data["fighters"][fighter_name] = {
                "tournament_results": {
                    "total_wins": 0,
                    "total_losses": 0,
                    "total_fights": 0
                },
                "stat_totals": {
                    "strength": 0,
                    "dexterity": 0,
                    "hp": 0,
                    "speed": 0,
                    "dodge": 0
                },
                "equipment_totals": {
                    "weapon_tier": 0,
                    "armor_tier": 0
                },
                "tournaments_played": 0
            }
        
        # Backward compatibility: dodaj equipment_totals jeśli nie istnieje
        if "equipment_totals" not in summary_data["fighters"][fighter_name]:
            summary_data["fighters"][fighter_name]["equipment_totals"] = {
                "weapon_tier": 0,
                "armor_tier": 0
            }
        
        # Aktualizuj skumulowane wyniki walk
        summary_data["fighters"][fighter_name]["tournament_results"]["total_wins"] += fighter_stats["wins"]
        summary_data["fighters"][fighter_name]["tournament_results"]["total_losses"] += fighter_stats["losses"]
        summary_data["fighters"][fighter_name]["tournament_results"]["total_fights"] += fighter_stats["fights"]
        
        # Aktualizuj sumy statystyk (do liczenia średnich)
        summary_data["fighters"][fighter_name]["stat_totals"]["strength"] += character.strength
        summary_data["fighters"][fighter_name]["stat_totals"]["dexterity"] += character.dexterity
        summary_data["fighters"][fighter_name]["stat_totals"]["hp"] += character.hp
        summary_data["fighters"][fighter_name]["stat_totals"]["speed"] += character.speed
        summary_data["fighters"][fighter_name]["stat_totals"]["dodge"] += character.dodge
        
        # Aktualizuj sumy ekwipunku (do liczenia średnich)
        summary_data["fighters"][fighter_name]["equipment_totals"]["weapon_tier"] += character.weapon.tier if hasattr(character, 'weapon') else 0
        summary_data["fighters"][fighter_name]["equipment_totals"]["armor_tier"] += character.armor.tier if hasattr(character, 'armor') else 0
        
        summary_data["fighters"][fighter_name]["tournaments_played"] += 1
        
        # Oblicz średnie statystyki
        tournaments = summary_data["fighters"][fighter_name]["tournaments_played"]
        summary_data["fighters"][fighter_name]["stats"] = {
            "strength": round(summary_data["fighters"][fighter_name]["stat_totals"]["strength"] / tournaments, 1),
            "dexterity": round(summary_data["fighters"][fighter_name]["stat_totals"]["dexterity"] / tournaments, 1),
            "hp": round(summary_data["fighters"][fighter_name]["stat_totals"]["hp"] / tournaments, 1),
            "speed": round(summary_data["fighters"][fighter_name]["stat_totals"]["speed"] / tournaments, 1),
            "dodge": round(summary_data["fighters"][fighter_name]["stat_totals"]["dodge"] / tournaments, 1)
        }
        
        # Oblicz średnie tiery ekwipunku
        summary_data["fighters"][fighter_name]["equipment"] = {
            "weapon_tier": round(summary_data["fighters"][fighter_name]["equipment_totals"]["weapon_tier"] / tournaments, 1),
            "armor_tier": round(summary_data["fighters"][fighter_name]["equipment_totals"]["armor_tier"] / tournaments, 1)
        }
    
    # Zapisz zaktualizowane dane
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Podsumowanie turnieju zaktualizowane: {filename}")
    print(f"📊 Łącznie turnieji: {summary_data['total_tournaments']}")
