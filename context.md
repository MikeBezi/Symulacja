# RPG SYSTEM - KONTEKST PROJEKTU

## 🎯 OBECNY STAN PROJEKTU
- ✅ Kompletny system RPG z walkami i turniejem
- ✅ 3 klasy postaci (Warrior, Hunter, Rouge)
- ✅ System przedmiotów z tierami (1-3)
- ✅ System walki turowej
- ✅ Turniej wszystkich vs wszystkich (190 walk)
- ✅ Zapisywanie wyników do JSON
- ✅ Działający main.py jako punkt wejścia

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
- `strength` - obrażenia (1-10+)
- `dexterity` - celność (1-10+)  
- `hp` - punkty życia (1-10+)
- `speed` - kolejność ataku (1-10+)
- `dodge` - unik (1-10+)

### Specjalizacje:
```python
Warrior:  STR=3, DEX=1, HP=3, SPD=2, DODGE=1  # Tank
Hunter:   STR=2, DEX=3, HP=2, SPD=1, DODGE=2  # Łucznik
Rouge:    STR=1, DEX=2, HP=1, SPD=4, DODGE=2  # Szybki
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

## 🎲 AKTUALNY BALANS

### Rozkład tierów:
- **Tier 1**: 10 broni + 10 zbroi
- **Tier 2**: 7 broni + 7 zbroi  
- **Tier 3**: 3 bronie + 3 zbroje

### Najlepsi wojownicy (przykład):
1. Tomasz - 94.7% (DEX=7, STR=6)
2. Rafał - 89.5% (DEX=7)
3. Wiktoria - 89.5% (STR=4, DEX=5)

## 🚀 PUNKTY ROZSZERZENIA

### Łatwe do dodania:
- **Nowe klasy postaci** (Mage, Paladin, Assassin)
- **Nowe typy przedmiotów** (Ring, Amulet, Shield)
- **Nowe statystyki** (magic, armor, critical)
- **Skille/Abilities** dla klas
- **Elementy** (Fire, Ice, Lightning)

### Średnie:
- **GUI** (tkinter/pygame)
- **Kampania** zamiast turnieju
- **Leveling system**
- **Crafting przedmiotów**

### Trudne:
- **AI przeciwnicy** z strategią
- **Multiplayer**
- **Graficzna walka turowa**

## 🐛 ZNANE PROBLEMY/UWAGI

- ✅ Duplikacja kodu była naprawiona
- ✅ main.py działa poprawnie
- ⚠️ Brak walidacji danych wejściowych
- ⚠️ Brak limitów statystyk (można mieć 100+ HP)
- ⚠️ Random seed nie jest kontrolowany

## 📁 STRUKTURA PLIKÓW

```
rpg_mechanics/
├── characters.py           # Klasy postaci
├── items.py               # System przedmiotów  
├── character_creator.py   # Tworzenie postaci
├── combat.py              # System walki
├── tournament.py          # Orkiestracja
├── main.py               # Punkt wejścia
├── context.md            # Ten plik
├── tournament_results.json # Wyniki
├── character_data.json    # Dane postaci
└── item_history.json     # Historia przedmiotów
```

## 🎯 NASTĘPNE KROKI

### Priorytet 1:
- [ ] Dodanie nowych klas postaci
- [ ] Rozszerzenie systemu przedmiotów
- [ ] Balansowanie statystyk

### Priorytet 2:  
- [ ] GUI dla systemu
- [ ] Zapisywanie/Wczytywanie postaci
- [ ] System skillów

### Priorytet 3:
- [ ] Kampania single-player
- [ ] Crafting system
- [ ] Graficzna prezentacja walk 