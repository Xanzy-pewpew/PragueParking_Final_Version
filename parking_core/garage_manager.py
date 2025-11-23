from parking_core.models import ParkingSpot, Vehicle
from datetime import datetime, timedelta

class ParkingGarage:
    """Huvudklassen för parkeringsgaraget, hanterar platser och fordon."""
    
    # Priser (timpris i SEK)
    HOURLY_RATE = 15
    MAX_DAILY_COST = 90
    
    def __init__(self, num_spots: int = 100):
        # Initialiserar 100 platser, alla med kapacitet 4 (standard för bil)
        self.spots = [ParkingSpot(i + 1, max_capacity=4) for i in range(num_spots)]

    def park_vehicle(self, vehicle: Vehicle, spot_id: int | None = None) -> int | None:
        """
        Parkerar ett fordon. Kan ta emot ett specifikt spot_id.
        Returnerar spot_id om parkeringen lyckas, annars None.
        """
        target_spot = None

        if spot_id is not None:
            # Försök parkera på specifik plats (val av användare/karta)
            try:
                # Observera: Spots är 0-indexerade, men ID är 1-indexerat
                target_spot = self.spots[spot_id - 1]
            except IndexError:
                # Ogiltigt ID
                return None 

            if target_spot.can_accommodate(vehicle):
                target_spot.add_vehicle(vehicle)
                return target_spot.id
            else:
                # Platsen är upptagen/för liten
                return None 
        
        else:
            # Hitta första lediga plats (Ursprunglig funktionalitet om spot_id ej ges)
            for spot in self.spots:
                if spot.can_accommodate(vehicle):
                    target_spot = spot
                    target_spot.add_vehicle(vehicle)
                    return target_spot.id
        
        return None # Inga lediga platser hittades

    def unpark_vehicle(self, reg_nr: str) -> dict | None:
        """
        Tar bort fordonet, beräknar kostnaden och returnerar detaljer.
        Returnerar en dict med resultat, eller None om fordonet inte hittas.
        """
        reg_nr = reg_nr.upper()
        
        for spot in self.spots:
            for vehicle in spot.vehicles:
                if vehicle.reg_nr == reg_nr:
                    
                    # 1. Beräkna kostnad
                    cost = self._calculate_cost(vehicle.entry_time)
                    
                    # 2. Ta bort fordonet från platsen
                    spot.remove_vehicle(vehicle)
                    
                    # 3. Returnera information
                    return {
                        "reg_nr": reg_nr,
                        "spot_id": spot.id,
                        "price": cost,
                        "entry_time": vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S")
                    }
        
        return None # Fordonet hittades inte

    def find_vehicle(self, reg_nr: str) -> dict | None:
        """Hittar ett fordon och returnerar dess plats-ID och typ."""
        reg_nr = reg_nr.upper()
        
        for spot in self.spots:
            for vehicle in spot.vehicles:
                if vehicle.reg_nr == reg_nr:
                    return {
                        "reg_nr": reg_nr,
                        "spot_id": spot.id,
                        "type": vehicle.type
                    }
        return None

    def _calculate_cost(self, entry_time: datetime) -> int:
        """Hjälpmetod för att beräkna parkeringskostnaden."""
        time_parked = datetime.now() - entry_time
        
        # Simulera avrundning uppåt till närmaste timme
        hours = max(1, (time_parked.total_seconds() / 3600))
        total_hours = int(hours) if hours == int(hours) else int(hours) + 1
        
        total_cost = total_hours * self.HOURLY_RATE
        
        # Beräkna maximal dygnskostnad
        days_parked = time_parked.days
        max_cost_for_period = days_parked * self.MAX_DAILY_COST + self.MAX_DAILY_COST
        
        # Kostnaden är det lägsta av den beräknade timkostnaden och max dygnskostnad
        return min(total_cost, max_cost_for_period)