# Symulator Mechaniki RPG

System do symulacji walk w grze RPG, uwzględniający różne atrybuty postaci, bronie i zbroje.

## Opis projektu

Projekt implementuje mechanikę gry RPG z następującymi elementami:
- System atrybutów postaci (siła, zręczność, inteligencja, wytrzymałość)
- Różnorodne bronie i zbroje wpływające na walkę
- Symulacja 20 bohaterów toczących ze sobą walki typu każdy-z-każdym
- Analiza statystyczna wyników i obliczenie prawdopodobieństwa zwycięstwa

## Struktura projektu

```
rpg_mechanics/
├── models/                # Modele używane w systemie
│   ├── character.py       # Definicje postaci i atrybutów
│   ├── equipment.py       # Definicje broni i zbroi
│   └── combat.py          # System walki
├── simulation/            # Moduł symulacji
│   ├── simulator.py       # Silnik symulacji
│   └── statistics.py      # Analiza wyników
├── results/               # Katalog na wygenerowane wykresy i raporty
├── doc/                   # Dokumentacja
│   └── mechanika.md       # Szczegółowy opis mechaniki gry
├── run_simulation.py      # Skrypt uruchamiający symulację
├── test_simulation.py     # Skrypt do testowania z parametrami
└── main.py                # Główny moduł projektu
```

## Instalacja i uruchomienie

### Wymagania

- Python 3.8 lub nowszy
- Matplotlib
- NumPy

### Instalacja zależności

```bash
pip install matplotlib numpy
```

### Uruchomienie symulacji

Standardowa symulacja:
```bash
# Z katalogu głównego projektu
python -c "import sys; sys.path.append('.'); from rpg_mechanics import main; main.main()"

# Lub z katalogu rpg_mechanics
cd rpg_mechanics
python run_simulation.py
```

Testowanie z niestandardowymi parametrami:
```bash
cd rpg_mechanics
python test_simulation.py --characters 10 --verbose --rounds 50
```

Dostępne parametry:
- `-c, --characters` - liczba bohaterów (domyślnie 20)
- `-v, --verbose` - wyświetla szczegóły każdej walki
- `-np, --no-plots` - nie generuje wykresów
- `-r, --rounds` - maksymalna liczba rund w walce (domyślnie 100)

## Elementy mechaniki

### Atrybuty postaci
- **Siła** - wpływa na obrażenia w walce wręcz
- **Zręczność** - wpływa na celność i uniki
- **Inteligencja** - wpływa na efektywność umiejętności
- **Wytrzymałość** - wpływa na maksymalne punkty życia

### Walka
System walki uwzględnia:
- Kalkulację obrażeń bazowych
- Modyfikatory bazujące na atrybutach
- Szansę na trafienie krytyczne
- Szansę na unik
- Akumulację zmęczenia
- Redukcję obrażeń przez zbroję

### Wyposażenie
Postacie mają dostęp do różnorodnego wyposażenia:
- 10 typów broni o różnych statystykach
- 10 typów zbroi o różnych statystykach

## Analiza wyników

System generuje szczegółową analizę obejmującą:
- Ranking postaci według liczby zwycięstw
- Prawdopodobieństwo zwycięstwa dla każdej postaci
- Korelację między atrybutami a wynikami walk
- Analizę skuteczności różnych typów broni i zbroi
- Wykres prawdopodobieństwa zwycięstwa
- Wykres korelacji atrybutów z wynikami

## Dokumentacja

Szczegółowa dokumentacja mechaniki gry znajduje się w pliku `doc/mechanika.md`. Zawiera ona:
- Opis wszystkich atrybutów i ich wpływu na walkę
- Listę dostępnych broni i zbroi z ich statystykami
- Szczegółowy opis algorytmów walki
- Zasady symulacji i analizy wyników

## Rozszerzenia projektu

Możliwe rozszerzenia projektu:
- Dodanie nowych typów postaci (klasy)
- Implementacja specjalnych umiejętności
- Rozbudowa systemu statystyk i analizy
- Dodanie efektów statusu (otrucie, ogłuszenie, itp.)
- Implementacja interfejsu graficznego

## Autorzy

Ten projekt został stworzony jako demonstracja mechaniki gry RPG do celów edukacyjnych. 