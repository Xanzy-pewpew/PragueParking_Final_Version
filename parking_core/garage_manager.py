import json
from .models import Vehicle

CONFIG_PATH = 'parking_config.json'

class ParkingSpot:
    """Klass 4: Representerar en enskild parkeringsplats."""
    def __init__(self, spot_id: int, total_capacity: int):
        self.id = spot_id
        self.capacity = total_capacity
        self.available_capacity = total_capacity
        self.vehicles = [] # Lista med Vehicle-objekt

    def park(self, vehicle: Vehicle) -> bool:
        """Försöker parkera ett fordon."""
        if self.available_capacity >= vehicle.size:
            self.vehicles.append(vehicle)
            self.available_capacity -= vehicle.size
            return True
        return False
        
    def __repr__(self):
        return f"Spot {self.id} ({self.available_capacity}/{self.capacity} available)"

class ParkingGarage:
    """Klass 5: Huvudklassen som hanterar alla P-platser och logik."""
    
    def __init__(self):
        self.config = self._load_config()
        capacity = self.config.get("garage_capacity", 100)
        spot_size = self.config.get("default_spot_capacity", 4)
        
        self.spots = [ParkingSpot(i + 1, spot_size) for i in range(capacity)] 

    def _load_config(self):
        """Läser in konfigurationen från JSON-filen."""
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Varning: Kunde inte läsa {CONFIG_PATH}. Använder standardvärden.")
            return {}

    def park_vehicle(self, vehicle: Vehicle) -> int | None:
        """Huvudlogik för parkering. Letar efter första lediga plats."""
        
        for spot in self.spots:
            if vehicle.type == "Bus" and spot.id > self.config.get("spot_bus_limit", 50):
                continue

            if spot.park(vehicle):
                return spot.id
                
        return None
    
    def unpark_vehicle(self, reg_nr: str) -> dict | None:
        """Hittar ett fordon efter reg.nummer och tar bort det."""
        target_reg = reg_nr.upper()

        for spot in self.spots:
            for vehicle in spot.vehicles:
                if vehicle.reg_nr == target_reg:
                    
                    spot.vehicles.remove(vehicle)
                    spot.available_capacity += vehicle.size
                    
                    return {
                        "reg_nr": target_reg,
                        "spot_id": spot.id,
                        "price": 50
                    }
        
        return None