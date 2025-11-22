from datetime import datetime

class Vehicle:
    """Basklass för alla fordon. Innehåller gemensamma egenskaper."""
    
    def __init__(self, reg_nr: str, v_type: str, size: int):
        self.reg_nr = reg_nr.upper()
        self.type = v_type
        self.size = size 
        self.entry_time = datetime.now()
        
    def __repr__(self):
        return f"{self.type} ({self.reg_nr})"

class Car(Vehicle):
    def __init__(self, reg_nr: str):
        super().__init__(reg_nr, "Car", 4)

class Motorcycle(Vehicle):
    def __init__(self, reg_nr: str):
        super().__init__(reg_nr, "Motorcycle", 2)

class Bicycle(Vehicle):
    def __init__(self, reg_nr: str):
        super().__init__(reg_nr, "Bicycle", 1)

class Bus(Vehicle):
    def __init__(self, reg_nr: str):
        super().__init__(reg_nr, "Bus", 16)