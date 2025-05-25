import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import seaborn as sns
import os
from datetime import datetime

class TournamentAnalyzer:
    def __init__(self):
        self.tournament_data = None
        self.character_data = None
        self.item_data = None
        
    def load_data(self):
        # Wczytywanie danych z plików JSON - bierze ostatni wpis w przypadku wielu JSON-ów
        try:
            # Tournament results - może mieć wiele JSON-ów, bierzemy ostatni
            with open("json/tournament_results.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                json_sections = [section.strip() for section in content.split('\n\n') if section.strip()]
                last_json = json_sections[-1]
                self.tournament_data = json.loads(last_json)
            
            # Character data - może mieć wiele JSON-ów, bierzemy ostatni
            with open("json/character_data.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                json_sections = [section.strip() for section in content.split('\n\n') if section.strip()]
                last_json = json_sections[-1]
                self.character_data = json.loads(last_json)
                
            # Item history - może mieć wiele JSON-ów, bierzemy ostatni
            with open("json/item_history.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                json_sections = [section.strip() for section in content.split('\n\n') if section.strip()]
                last_json = json_sections[-1]
                self.item_data = json.loads(last_json)
            
            print("✅ Dane wczytane pomyślnie!")
            print(f"📊 Znaleziono {len(json_sections)} wpisów, używam ostatniego")
            return True
        
        except FileNotFoundError as e:
            print(f"❌ Nie znaleziono pliku: {e}")
            return False
        
        except json.JSONDecodeError as e:
            print(f"❌ Błąd parsowania JSON: {e}")
            return False
    
    def prepare_analysis_data(self):
        # Połączenie statystyk turnieju z danymi postaci
        stats = self.tournament_data["statistics"]
        characters = self.character_data["characters"]
        
        analysis_data = []
        
        for char in characters:
            name = char["name"]
            if name in stats:
                # Dodaj dane postaci
                row = {
                    "name": name,
                    "class": char["class"],
                    "win_rate": stats[name]["win_rate"],
                    "wins": stats[name]["wins"],
                    "losses": stats[name]["losses"],
                    
                    # Statystyki końcowe (bazowe + ekwipunek)
                    "strength": char["stats"]["strength"],
                    "dexterity": char["stats"]["dexterity"], 
                    "hp": char["stats"]["hp"],
                    "speed": char["stats"]["speed"],
                    "dodge": char["stats"]["dodge"]
                }
                
                # Dodaj informacje o ekwipunku
                if char["equipment"]["weapon"]:
                    row["weapon_tier"] = char["equipment"]["weapon"]["tier"]
                    row["weapon_type"] = char["equipment"]["weapon"]["name"]
                    # Dodaj czysty typ broni (bez tieru)
                    row["weapon_base_type"] = char["equipment"]["weapon"]["name"].split("(")[0].strip()
                    # Sumuj bonusy z broni
                    weapon_stats = char["equipment"]["weapon"]["stats"]
                    for stat, value in weapon_stats.items():
                        row[f"weapon_{stat}"] = value
                
                if char["equipment"]["armor"]:
                    row["armor_tier"] = char["equipment"]["armor"]["tier"]
                    row["armor_type"] = char["equipment"]["armor"]["name"]
                    # Dodaj czysty typ zbroi (bez tieru)
                    row["armor_base_type"] = char["equipment"]["armor"]["name"].split("(")[0].strip()
                    # Sumuj bonusy ze zbroi
                    armor_stats = char["equipment"]["armor"]["stats"]
                    for stat, value in armor_stats.items():
                        row[f"armor_{stat}"] = value
                
                analysis_data.append(row)
        
        return pd.DataFrame(analysis_data).fillna(0)
    
    def analyze_stat_correlations(self, df):
        # Analiza korelacji między statystykami a współczynnikiem wygranych
        stats_to_analyze = ["strength", "dexterity", "hp", "speed", "dodge"]
        correlations = {}
        
        for stat in stats_to_analyze:
            corr, p_value = pearsonr(df[stat], df["win_rate"])
            correlations[stat] = {"correlation": corr, "p_value": p_value}
        
        return correlations
    
    def analyze_equipment_impact(self, df):
        # Analiza tierów broni
        weapon_analysis = df.groupby("weapon_tier")["win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        # Analiza tierów zbroi
        armor_analysis = df.groupby("armor_tier")["win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        # Analiza typów broni (bez tierów)
        weapon_base_type_analysis = df.groupby("weapon_base_type")["win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        # Analiza typów zbroi (bez tierów)
        armor_base_type_analysis = df.groupby("armor_base_type")["win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        return {
            "weapon_tier": weapon_analysis,
            "armor_tier": armor_analysis,
            "weapon_base_type": weapon_base_type_analysis,
            "armor_base_type": armor_base_type_analysis
        }
    
    def save_data_analysis(self, filename, dpi=300):         
        charts_folder = "data_analysis"
        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = filename.rsplit('.', 1)
        timestamped_filename = f"{name}_{timestamp}.{ext}" 

        plt.tight_layout()
        filepath = os.path.join(charts_folder, timestamped_filename)
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close()

    def create_stat_correlation_plot(self, correlations):
        # Tworzy wykres korelacji statystyk
        stats = list(correlations.keys())
        corr_values = [correlations[stat]["correlation"] for stat in stats]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(stats, corr_values, color=['skyblue' if x >= 0 else 'lightcoral' for x in corr_values])
        
        plt.title("Korelacja statystyk z współczynnikiem wygranych", fontsize=14, fontweight='bold')
        plt.xlabel("Statystyki")
        plt.ylabel("Współczynnik korelacji")
        plt.ylim(-1, 1)
        plt.grid(axis='y', alpha=0.3)
        
        # Dodaj wartości na słupkach
        for bar, value in zip(bars, corr_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02 if value >= 0 else bar.get_height() - 0.05,
                    f'{value:.3f}', ha='center', va='bottom' if value >= 0 else 'top', fontweight='bold')
        
        self.save_data_analysis("stat_correlations.png", dpi=300)
    
    def create_equipment_analysis_plots(self, equipment_data):
        # Tworzy wykresy analizy ekwipunku
        fig, ((ax1, ax2)) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Wykres 1: Tier broni
        weapon_tier_data = equipment_data["weapon_tier"]
        ax1.bar(weapon_tier_data.index, weapon_tier_data["mean"], 
                color=['lightgreen', 'gold', 'orange'], alpha=0.7)
        ax1.set_title("Średni win rate według tier broni", fontweight='bold')
        ax1.set_xlabel("Tier broni")
        ax1.set_ylabel("Średni win rate (%)")
        for i, v in enumerate(weapon_tier_data["mean"]):
            ax1.text(weapon_tier_data.index[i], v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
        
        # Wykres 2: Tier zbroi
        armor_tier_data = equipment_data["armor_tier"]
        ax2.bar(armor_tier_data.index, armor_tier_data["mean"],
                color=['lightblue', 'silver', 'gold'], alpha=0.7)
        ax2.set_title("Średni win rate według tier zbroi", fontweight='bold')
        ax2.set_xlabel("Tier zbroi")
        ax2.set_ylabel("Średni win rate (%)")
        for i, v in enumerate(armor_tier_data["mean"]):
            ax2.text(armor_tier_data.index[i], v + 1, f'{v:.1f}%', ha='center', fontweight='bold')      
        
        self.save_data_analysis("equipment_analysis.png", dpi=300)
    
    def create_heatmap_analysis(self, df):
        # Tworzy heatmapę korelacji wszystkich statystyk
        # Wybierz tylko numeryczne kolumny do analizy korelacji
        numeric_cols = ["win_rate", "strength", "dexterity", "hp", "speed", "dodge", 
                       "weapon_tier", "armor_tier"]
        corr_data = df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_data, annot=True, cmap='RdBu_r', center=0,
                    square=True, fmt='.3f', cbar_kws={"shrink": .8})
        plt.title("Heatmapa korelacji wszystkich czynników", fontsize=14, fontweight='bold')

        self.save_data_analysis("correlation_heatmap.png", dpi=300)
    
    def generate_report(self, correlations, equipment_data, df):
        # Generuje raport z analizy
        print("\n" + "="*60)
        print("📊 RAPORT ANALIZY TURNIEJU RPG")
        print("="*60)
        
        print("\n🎯 NAJWAŻNIEJSZE STATYSTYKI:")
        sorted_stats = sorted(correlations.items(), key=lambda x: abs(x[1]["correlation"]), reverse=True)
        for i, (stat, data) in enumerate(sorted_stats, 1):
            significance = "***" if data["p_value"] < 0.001 else "**" if data["p_value"] < 0.01 else "*" if data["p_value"] < 0.05 else ""
            print(f"{i}. {stat.upper()}: r={data['correlation']:.3f} {significance}")
        
        print("\n⚔️ ANALIZA EKWIPUNKU:")
        print("\nTiery broni (średni win rate):")
        for tier, rate in equipment_data["weapon_tier"]["mean"].items():
            print(f"   Tier {tier}: {rate:.1f}%")
        
        print("\nTiery zbroi (średni win rate):")
        for tier, rate in equipment_data["armor_tier"]["mean"].items():
            print(f"   Tier {tier}: {rate:.1f}%")
        
        print("\n🏆 TOP 3 WOJOWNIKÓW:")
        top_fighters = df.nlargest(3, "win_rate")
        for i, (_, fighter) in enumerate(top_fighters.iterrows(), 1):
            print(f"{i}. {fighter['name']} ({fighter['class']}): {fighter['win_rate']:.1f}%")
            print(f"   STR={fighter['strength']}, DEX={fighter['dexterity']}, HP={fighter['hp']}, SPD={fighter['speed']}, DODGE={fighter['dodge']}")
        
        print("\n" + "="*60)
    
    def run_full_analysis(self):
        # Przeprowadza pełną analizę danych
        if not self.load_data():
            return
        
        # Przygotuj dane
        df = self.prepare_analysis_data()
        print(f"📊 Przygotowano dane dla {len(df)} wojowników")
        
        # Analiza korelacji statystyk
        correlations = self.analyze_stat_correlations(df)
        
        # Analiza wpływu ekwipunku
        equipment_data = self.analyze_equipment_impact(df)
        
        # Tworzy wykresy
        self.create_stat_correlation_plot(correlations)
        self.create_equipment_analysis_plots(equipment_data)
        self.create_heatmap_analysis(df)
        
        # Generuje raport
        self.generate_report(correlations, equipment_data, df)
        
        return df, correlations, equipment_data
    
    def load_summary_data(self):
        # Wczytanie danych z tournament_summary.json
        try:
            with open("json/tournament_summary.json", "r", encoding="utf-8") as f:
                self.summary_data = json.load(f)
            print("✅ Dane z podsumowania turnieju wczytane pomyślnie!")
            return True
        except FileNotFoundError:
            print("❌ Nie znaleziono pliku tournament_summary.json")
            print("💡 Najpierw uruchom kilka turnieji aby wygenerować dane")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Błąd parsowania JSON: {e}")
            return False
    
    def prepare_summary_analysis_data(self):
        # Przygotowanie DataFrame z danych skumulowanych
        fighters = self.summary_data["fighters"]
        analysis_data = []
        
        for fighter_name, data in fighters.items():
            # Oblicz ogólny win rate
            total_fights = data["tournament_results"]["total_fights"]
            total_wins = data["tournament_results"]["total_wins"]
            overall_win_rate = (total_wins / total_fights * 100) if total_fights > 0 else 0
            
            row = {
                "name": fighter_name,
                "overall_win_rate": round(overall_win_rate, 2),
                "total_wins": total_wins,
                "total_losses": data["tournament_results"]["total_losses"],
                "total_fights": total_fights,
                
                # Statystyki postaci (z ostatniego turnieju)
                "strength": data["stats"]["strength"],
                "dexterity": data["stats"]["dexterity"],
                "hp": data["stats"]["hp"],
                "speed": data["stats"]["speed"],
                "dodge": data["stats"]["dodge"],
                
                # Ekwipunek
                "weapon_tier": data["equipment"]["weapon_tier"],
                "armor_tier": data["equipment"]["armor_tier"]
            }
            analysis_data.append(row)
        
        return pd.DataFrame(analysis_data)
    
    def analyze_summary_stat_correlations(self, df):
        # Analiza korelacji dla danych skumulowanych
        stats_to_analyze = ["strength", "dexterity", "hp", "speed", "dodge"]
        correlations = {}
        
        for stat in stats_to_analyze:
            corr, p_value = pearsonr(df[stat], df["overall_win_rate"])
            correlations[stat] = {"correlation": corr, "p_value": p_value}
        
        return correlations
    
    def analyze_summary_equipment_impact(self, df):
        # Analiza wpływu ekwipunku dla danych skumulowanych
        weapon_analysis = df.groupby("weapon_tier")["overall_win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        # Analiza tierów zbroi
        armor_analysis = df.groupby("armor_tier")["overall_win_rate"].agg([
            "mean", "median", "count", "std"
        ]).round(2)
        
        return {
            "weapon_tier": weapon_analysis,
            "armor_tier": armor_analysis
        }
    
    def save_final_analysis(self, filename, dpi=300):
        # Zapisanie wykresów do folderu final_analysis
        charts_folder = "final_analysis"
        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = filename.rsplit('.', 1)
        timestamped_filename = f"{name}_{timestamp}.{ext}" 

        plt.tight_layout()
        filepath = os.path.join(charts_folder, timestamped_filename)
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close()
    
    def create_summary_correlation_plot(self, correlations):
        # Tworzy wykres korelacji dla danych skumulowanych
        stats = list(correlations.keys())
        corr_values = [correlations[stat]["correlation"] for stat in stats]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(stats, corr_values, color=['skyblue' if x >= 0 else 'lightcoral' for x in corr_values])
        
        plt.title("Korelacja statystyk z ogólnym win rate (wiele turnieji)", fontsize=14, fontweight='bold')
        plt.xlabel("Statystyki")
        plt.ylabel("Współczynnik korelacji")
        plt.ylim(-1, 1)
        plt.grid(axis='y', alpha=0.3)
        
        # Dodaj wartości na słupkach
        for bar, value in zip(bars, corr_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02 if value >= 0 else bar.get_height() - 0.05,
                    f'{value:.3f}', ha='center', va='bottom' if value >= 0 else 'top', fontweight='bold')
        
        self.save_final_analysis("summary_stat_correlations.png", dpi=300)
    
    def generate_summary_report(self, correlations, equipment_data, df):
        # Generuje raport dla danych skumulowanych
        print("\n" + "="*80)
        print("📊 RAPORT ANALIZY SKUMULOWANEJ (WIELE TURNIEJI)")
        print("="*80)
        
        # Informacje ogólne
        total_fights = df["total_fights"].iloc[0] if len(df) > 0 else 0
        total_tournaments = total_fights // 19 if total_fights > 0 else 0  # 19 walk na turniej dla 20 postaci
        
        print(f"\n📈 PRZEGLĄD OGÓLNY:")
        print(f"   Szacowana liczba turnieji: {total_tournaments}")
        print(f"   Łączna liczba walk na wojownika: {total_fights}")
        print(f"   Analizowanych wojowników: {len(df)}")
        
        print("\n🎯 NAJWAŻNIEJSZE STATYSTYKI:")
        sorted_stats = sorted(correlations.items(), key=lambda x: abs(x[1]["correlation"]), reverse=True)
        for i, (stat, data) in enumerate(sorted_stats, 1):
            significance = "***" if data["p_value"] < 0.001 else "**" if data["p_value"] < 0.01 else "*" if data["p_value"] < 0.05 else ""
            print(f"{i}. {stat.upper()}: r={data['correlation']:.3f} {significance}")
        
        print("\n⚔️ ANALIZA EKWIPUNKU:")
        print("\nTiery broni (średni win rate):")
        for tier, rate in equipment_data["weapon_tier"]["mean"].items():
            count = equipment_data["weapon_tier"]["count"][tier]
            print(f"   Tier {tier}: {rate:.1f}% ({count} wojowników)")
        
        print("\nTiery zbroi (średni win rate):")
        for tier, rate in equipment_data["armor_tier"]["mean"].items():
            count = equipment_data["armor_tier"]["count"][tier]
            print(f"   Tier {tier}: {rate:.1f}% ({count} wojowników)")
        
        print("\n🏆 TOP 5 WOJOWNIKÓW (ogólny win rate):")
        top_fighters = df.nlargest(5, "overall_win_rate")
        for i, (_, fighter) in enumerate(top_fighters.iterrows(), 1):
            print(f"{i}. {fighter['name']}: {fighter['overall_win_rate']:.1f}% ({fighter['total_wins']}W/{fighter['total_losses']}L)")
            print(f"   STR={fighter['strength']}, DEX={fighter['dexterity']}, HP={fighter['hp']}, SPD={fighter['speed']}, DODGE={fighter['dodge']}")
            print(f"   Ekwipunek: Broń T{fighter['weapon_tier']}, Zbroja T{fighter['armor_tier']}")
        
        print("\n" + "="*80)
    
    def run_summary_analysis(self):
        # Przeprowadza analizę danych skumulowanych z tournament_summary.json
        print("\n🎯 ROZPOCZYNAM ANALIZĘ SKUMULOWANYCH DANYCH...")
        
        if not self.load_summary_data():
            return None
        
        # Przygotuj dane
        df = self.prepare_summary_analysis_data()
        print(f"📊 Przygotowano dane skumulowane dla {len(df)} wojowników")
        
        # Analizy
        correlations = self.analyze_summary_stat_correlations(df)
        equipment_data = self.analyze_summary_equipment_impact(df)
        
        # Tworzy wykresy - tylko korelacje (najbardziej przydatne)
        print("📈 Tworzę wykres korelacji...")
        self.create_summary_correlation_plot(correlations)
        
        # Generuje raport
        self.generate_summary_report(correlations, equipment_data, df)
        
        print("✅ Analiza skumulowana zakończona! Wyniki w folderze 'final_analysis'")
        return df, correlations, equipment_data

def main():
    analyzer = TournamentAnalyzer()
    return analyzer.run_full_analysis()

def summary_analysis():
    analyzer = TournamentAnalyzer()
    return analyzer.run_summary_analysis()