class Character:
    def __init__(self, name):
        self.name = name
        self.strength = 1  # Wpływa na obrażenia w walce wręcz
        self.dexterity = 1  # Wpływa na celność i uniki
        self.hp = 1  # Wpływa na efektywność umiejętności
        self.speed = 1  # Wpływa na kolejność ataku
        self.dodge = 1  # Wpływa na maksymalne punkty życia
        

class Hunter(Character):
    def __init__(self, name):
        super().__init__(name)
        
        # Uzupełnienie statystyk specyficznych dla łowcy
        self.strength = 2
        self.dexterity = 3
        self.hp = 2
        self.speed = 1     
        self.dodge = 2

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        
        # Uzupełnienie statystyk specyficznych dla wojownika
        self.strength = 3
        self.dexterity = 1
        self.hp = 3
        self.speed = 2     
        self.dodge = 1

class Rouge(Character):
    def __init__(self, name):
        super().__init__(name)
        
        # Uzupełnienie statystyk specyficznych dla łotrzyka
        self.strength = 1
        self.dexterity = 2
        self.hp = 1
        self.speed = 4     
        self.dodge = 2




