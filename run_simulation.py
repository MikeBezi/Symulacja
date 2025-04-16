#!/usr/bin/env python
"""
Skrypt do uruchamiania symulacji RPG.
Uruchom z katalogu głównego projektu poleceniem: python run_simulation.py
"""
import sys
import os

# Dodanie ścieżki nadrzędnej do sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from rpg_mechanics.main import main

if __name__ == "__main__":
    main() 