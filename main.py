import tournament
import data_analysis
import time

x = input("Podaj liczbę turniejów: ")
for i in range(int(x)):
    print(f"\n=== TURNIEJ {i+1}/{int(x)} ===")
    tournament.main()
    data_analysis.main()
    
    # Opóźnienie przed następnym turniejem
    if i < int(x) - 1:
        print(f"Obecnie jest {i+1}/{int(x)} turniejów.")
        print(f"🕒Oczekiwanie 5 sekund przed następnym turniejem...")

        time.sleep(5)

# Analiza skumulowana po wszystkich turniejmach
print(f"\n{'='*60}")
print("🎯 URUCHAMIAM ANALIZĘ SKUMULOWANĄ")
print(f"{'='*60}")
data_analysis.summary_analysis()

input("\n🎯 Naciśnij Enter aby zakończyć program...")

