# Dokumentacja Mechaniki Gry RPG

## Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [System atrybutów](#system-atrybutów)
3. [Wyposażenie](#wyposażenie)
4. [System walki](#system-walki)
5. [Symulacja](#symulacja)
6. [Analiza wyników](#analiza-wyników)

## Wprowadzenie

Mechanika gry RPG implementuje system symulacji walk między postaciami w świecie fantasy. System uwzględnia różne atrybuty postaci, ich wyposażenie oraz wprowadza elementy losowości w walkach. Celem projektu jest zbadanie wpływu różnych parametrów na wynik walki oraz określenie prawdopodobieństwa zwycięstwa dla każdej z postaci.

## System atrybutów

Każda postać posiada zestaw atrybutów wpływających na jej skuteczność w walce:

### Atrybuty podstawowe

- **Siła (STR)** - określa fizyczną siłę postaci
  - Wpływa na obrażenia w walce wręcz
  - Zwiększa obrażenia bazowe o 0.5 punktu za każdy punkt siły

- **Zręczność (DEX)** - określa zwinność i refleks postaci
  - Wpływa na szansę trafienia (3% za punkt)
  - Wpływa na szansę uników (1% za punkt)
  - Wpływa na szansę trafienia krytycznego (1% za punkt)
  - Wpływa na inicjatywę w walce

- **Inteligencja (INT)** - określa mądrość i wiedzę postaci
  - Potencjał do rozszerzenia na system magii
  - Obecnie ma mniejszy wpływ na walkę

- **Wytrzymałość (END)** - określa odporność i żywotność postaci
  - Wpływa na maksymalne punkty życia (+10 HP za każdy punkt)
  - Bazowe HP wynosi 50 punktów

### Atrybuty pochodne

- **Punkty życia (HP)** - określają ile obrażeń postać może przyjąć zanim umrze
  - Obliczane jako: 50 + (Wytrzymałość * 10)

- **Zmęczenie (Fatigue)** - akumuluje się podczas walki
  - Rośnie o 10 punktów po każdym ataku
  - Rośnie o 5 punktów po chybionym ataku
  - Przy 100 punktach zmęczenia postać nie może atakować
  - Zmniejsza skuteczność obrażeń o 0.5% za każdy punkt

## Wyposażenie

### Bronie

Bronie mają różne statystyki wpływające na walkę:

- **Obrażenia bazowe** - podstawowa wartość obrażeń zadawanych przez broń
- **Szybkość ataku** - wpływa na częstotliwość ataków (skala 1-10)
- **Bonusy do atrybutów** - niektóre bronie dają dodatkowe bonusy do atrybutów

#### Dostępne bronie

| Nazwa | Obrażenia | Szybkość | Bonusy |
|-------|-----------|----------|--------|
| Stalowy miecz | 10 | 5 | +2 STR |
| Ciężki topór | 15 | 3 | +3 STR |
| Ostry sztylet | 6 | 8 | +3 DEX |
| Długi łuk | 8 | 6 | +4 DEX |
| Długa włócznia | 12 | 4 | +1 STR, +1 DEX |
| Bojowy młot | 18 | 2 | +4 STR |
| Magiczny kostur | 7 | 5 | +5 INT |
| Ostra katana | 11 | 7 | +2 DEX |
| Dwuręczny miecz | 20 | 2 | +5 STR |
| Elegancki rapier | 8 | 9 | +5 DEX |

### Zbroje

Zbroje zapewniają ochronę przed obrażeniami, ale mogą ograniczać zwinność:

- **Wartość ochrony** - zmniejsza otrzymywane obrażenia o stałą wartość
- **Kara do zręczności** - niektóre cięższe zbroje zmniejszają zręczność
- **Bonus do wytrzymałości** - niektóre zbroje zwiększają wytrzymałość

#### Dostępne zbroje

| Nazwa | Ochrona | Kara do DEX | Bonus do END |
|-------|---------|-------------|-------------|
| Skórzana zbroja | 3 | 0 | +1 |
| Kolczuga | 5 | -1 | +2 |
| Pełna płytowa | 10 | -3 | +3 |
| Wielka tarcza | 4 | -1 | +1 |
| Magiczna szata | 4 | 0 | +2 |
| Wzmocniona skóra | 4 | 0 | +1 |
| Legendarna zbroja | 12 | -1 | +4 |
| Mistrzowska kolczuga | 7 | 0 | +2 |
| Lekka płytowa | 6 | -1 | +2 |
| Smocza skóra | 8 | 0 | +3 |

## System walki

Walka w systemie jest turowa i opiera się na poniższych zasadach:

### Inicjatywa

Na początku każdej rundy ustalana jest inicjatywa, która określa kolejność ataków:
- Inicjatywa = Zręczność * Losowy modyfikator (0-1)
- Postać z wyższą inicjatywą atakuje pierwsza

### Trafienie

Szansa na trafienie zależy od zręczności atakującego i broniącego się:
- Bazowa szansa: 50%
- Modyfikator zręczności atakującego: +3% za punkt
- Modyfikator zręczności broniącego: -1% za punkt
- Minimalna szansa trafienia: 10%
- Maksymalna szansa trafienia: 95%

### Obrażenia

Obliczanie zadawanych obrażeń:
1. Obrażenia bazowe = Obrażenia broni lub Siła/2 (jeśli brak broni)
2. Bonus od siły = Siła * 0.5
3. Obrażenia surowe = Obrażenia bazowe + Bonus od siły
4. Modyfikator zmęczenia = 1 - (Zmęczenie * 0.005)
5. Trafienie krytyczne (szansa = 5% + Zręczność * 1%) podwaja obrażenia
6. Końcowe obrażenia = Obrażenia surowe * Modyfikator zmęczenia * Modyfikator krytyczny
7. Redukcja przez zbroję: Końcowe obrażenia - Wartość ochrony zbroi
8. Minimalne zadawane obrażenia to 1 punkt

### Zmęczenie

System zmęczenia wprowadza mechanikę ograniczającą skuteczność w dłuższych walkach:
- Po każdym ataku zmęczenie wzrasta o 10 punktów
- Po chybionym ataku zmęczenie wzrasta o 5 punktów
- Przy poziomie zmęczenia 100 postać nie może zaatakować
- Postać odpoczywa (zmęczenie -5) w rundzie, w której nie może zaatakować
- Zmęczenie zmniejsza zadawane obrażenia o 0.5% za każdy punkt

### Przebieg walki

1. Ustalenie inicjatywy i kolejności ataków
2. Pierwsza postać wykonuje atak
3. Sprawdzenie czy druga postać przeżyła
4. Druga postać wykonuje atak (jeśli żyje)
5. Sprawdzenie czy pierwsza postać przeżyła
6. Powtórzenie kroków 1-5 aż do śmierci jednej z postaci lub osiągnięcia limitu rund

## Symulacja

Symulator tworzy 20 bohaterów z losowymi atrybutami i wyposażeniem, a następnie przeprowadza turniej, w którym każda postać walczy z każdą inną (190 walk).

### Generowanie postaci

- Imiona wybierane są losowo z puli 30 imion bohaterów fantasy
- Atrybuty (siła, zręczność, inteligencja, wytrzymałość) losowane są w zakresie 5-15
- Broń i zbroja przydzielane są losowo z dostępnych opcji

### Turniej

Turniej odbywa się w formacie "każdy z każdym":
- Każda postać walczy z każdą inną dokładnie raz
- Po każdej walce aktualizowane są statystyki zwycięstw i porażek
- Maksymalna liczba rund w pojedynczej walce to 100
- Jeśli żadna postać nie umrze przed limitem rund, zwycięzcą zostaje ta z większą ilością pozostałych punktów życia

## Analiza wyników

Po zakończeniu symulacji przeprowadzana jest szczegółowa analiza wyników:

### Ranking bohaterów

Postacie są sortowane według liczby zwycięstw i wyświetlane wraz z ich statystykami.

### Prawdopodobieństwo zwycięstwa

Dla każdej postaci obliczane jest prawdopodobieństwo zwycięstwa jako stosunek liczby wygranych walk do liczby wszystkich walk.

### Korelacja atrybutów

Analiza korelacji między poszczególnymi atrybutami a wynikami walk:
- Obliczana jest korelacja Pearsona między wartościami atrybutów a współczynnikiem zwycięstw
- Identyfikowany jest atrybut mający największy wpływ na wynik walki

### Skuteczność ekwipunku

Analiza wpływu broni i zbroi na wyniki walk:
- Obliczany jest współczynnik zwycięstw dla każdego typu broni i zbroi
- Identyfikowane są najskuteczniejsze i najmniej skuteczne elementy wyposażenia

### Wykresy

Generowane są wykresy przedstawiające:
1. Prawdopodobieństwo zwycięstwa dla każdej postaci
2. Korelację między atrybutami a wynikami walk

### Wnioski i sugestie balansu

Na podstawie analizy formułowane są wnioski dotyczące:
- Najważniejszych atrybutów
- Najskuteczniejszych kombinacji ekwipunku
- Sugestii dotyczących balansu broni i zbroi 