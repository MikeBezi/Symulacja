# RPG SYSTEM

## 🎯 OBECNY STAN PROJEKTU
- ✅ Kompletny system RPG z walkami i turniejem
- ✅ 3 klasy postaci (Warrior, Hunter, Rouge)
- ✅ System przedmiotów z tierami (1-3)
- ✅ System walki turowej
- ✅ Turniej wszystkich vs wszystkich (190 walk)
- ✅ Zapisywanie wyników do JSON

## 🏗️ ARCHITEKTURA SYSTEMU

### Moduły i odpowiedzialności:
```
characters.py     → Definicje klas postaci
items.py         → System przedmiotów (broń, zbroja)
character_creator.py → Tworzenie postaci + wyposażenie
combat.py        → Mechanika walki + turniej
tournament.py    → Orkiestracja całego systemu
main.py         → Punkt wejścia
```

## 👥 KLASY POSTACI

### Character (bazowa):
- `name` - imię postaci
- `strength` - obrażenia
- `dexterity` - celność
- `hp` - punkty życia
- `speed` - kolejność ataku
- `dodge` - unik

### Specjalizacje:
```
Warrior:  STR=3, DEX=1, HP=3, SPD=2, DODGE=1
Hunter:   STR=2, DEX=3, HP=2, SPD=1, DODGE=2 
Rouge:    STR=1, DEX=2, HP=1, SPD=4, DODGE=2
```

## ⚔️ SYSTEM PRZEDMIOTÓW

### Struktura:
- **Item (bazowa)** → Weapon, Armor
- **Tiers**: 1 (1 stat), 2 (2 stats), 3 (3 stats)
- **Możliwe statystyki**: strength, dexterity, hp, speed, dodge
- **Wartości**: Tier 1 (1-2), Tier 2-3 (1-3)

### Typy:
```python
Bronie: Miecz, Topór, Łuk
Zbroje: Zbroja skórzana, Kolczuga, Zbroja płytowa
```

## ⚔️ MECHANIKA WALKI

### Kolejność:
1. **Speed** określa kto atakuje pierwszy
2. **Atak**: Rzut 1-10 ≤ dexterity = trafienie
3. **Unik**: Rzut 1-10 ≤ dodge = uniknięcie
4. **Obrażenia**: = strength atakującego
5. **Koniec**: gdy HP ≤ 0

### Klasa Combat:
- `reset_fighters()` - przywraca HP na start walki
- `attempt_hit()` - sprawdza trafienie i unik
- `deal_damage()` - zadaje obrażenia
- `fight()` - przeprowadza całą walkę

## 🏆 SYSTEM TURNIEJU

### Turniej:
- **190 walk** (20 postaci × 19 przeciwników ÷ 2)
- **Round-robin** - każdy z każdym raz
- **Statystyki**: wins, losses, win_rate
- **Ranking** według win_rate

### Dane wyjściowe:
```json
tournament_results.json - wyniki + logi walk
character_data.json     - dane postaci
item_history.json       - historia przedmiotów
```

## 🔄 PRZEPŁYW SYSTEMU

```
main.py 
  ↓
tournament.main()
  ↓
character_creator.main() → zwraca 20 postaci z ekwipunkiem
  ↓
combat.run_tournament() → 190 walk
  ↓
calculate_statistics() → oblicza statystyki
  ↓
save_tournament_results() → zapis do JSON
```

## 📊 KLUCZOWE FUNKCJE

### character_creator.py:
- `main()` - tworzy 20 postaci + ekwipunek (ZWRACA char_list)
- `equip_item()` - dodaje przedmiot do postaci
- `character_to_dict()` - konwersja do JSON

### combat.py:
- `run_tournament()` - przeprowadza wszystkie walki
- `calculate_statistics()` - oblicza statystyki win/loss
- `save_tournament_results()` - zapis wyników

### items.py:
- `generate_random_items()` - tworzy losowe przedmioty
- `Item._generate_stats()` - losuje statystyki wg tier

## 📁 STRUKTURA PLIKÓW

```
rpg_mechanics/
├── characters.py           # Klasy postaci
├── items.py               # System przedmiotów  
├── character_creator.py   # Tworzenie postaci
├── combat.py              # System walki
├── tournament.py          # Orkiestracja
├── main.py               # Punkt wejścia
├── tournament_results.json # Wyniki
├── character_data.json    # Dane postaci
└── item_history.json     # Historia przedmiotów
```
