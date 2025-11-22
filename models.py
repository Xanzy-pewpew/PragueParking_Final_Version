class Vehicle:
    def __init__(self, reg_nr):
        self.reg_nr = reg_nr.upper() 
        self.size = 0 
        self.type_code = "UNKNOWN"
        
class Car(Vehicle):
    def __init__(self, reg_nr):
        super().__init__(reg_nr)
        self.size = 1
        self.type_code = "CAR"
        
class Motorcycle(Vehicle):
    def __init__(self, reg_nr):
        super().__init__(reg_nr)
        self.size = 0.5 
        self.type_code = "MC"