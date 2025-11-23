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

class ParkingSpot:
    """Representerar en enskild parkeringsplats med kapacitet."""

    def __init__(self, spot_id: int, max_capacity: int):
        self.id = spot_id
        self.max_capacity = max_capacity
        self.available_capacity = max_capacity
        self.vehicles = [] # Lista över fordon (Vehicle-objekt) parkerade på platsen

    @property
    def is_full(self) -> bool:
        """Kollar om platsen är helt fylld."""
        return self.available_capacity == 0
    
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Kollar om fordonet får plats på denna plats."""
        return vehicle.size <= self.available_capacity
    
    def add_vehicle(self, vehicle: Vehicle):
        """Lägger till fordon och uppdaterar kapacitet."""
        if self.can_accommodate(vehicle):
            self.vehicles.append(vehicle)
            self.available_capacity -= vehicle.size

    def remove_vehicle(self, vehicle: Vehicle):
        """Tar bort fordon och återställer kapacitet (används i GarageManager)."""
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            self.available_capacity += vehicle.size