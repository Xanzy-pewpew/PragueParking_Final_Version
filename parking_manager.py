from models import Car, Motorcycle
from utils import encode, decode, find_in_slot, DLM_S

CAPACITY = 100

class ParkingManager:
    def __init__(self):
        self.slots = [""] * CAPACITY
        
    def search_vehicle(self, reg_nr):
        reg_nr = reg_nr.upper()
        for i, content in enumerate(self.slots):
            v_type = find_in_slot(content, reg_nr)
            if v_type: return i + 1, v_type 
        return None, None 
        
    def park_vehicle(self, vehicle):
        
        if vehicle.type_code == "CAR":
            for i, content in enumerate(self.slots):
                if not content:
                    self.slots[i] = encode(vehicle)
                    return i + 1
                    
        elif vehicle.type_code == "MC":
            
            # Försök dubbelparkera
            for i, content in enumerate(self.slots):
                if content and DLM_S not in content and decode(content)[0][0] == "MC":
                    self.slots[i] += f"{DLM_S}{encode(vehicle)}"
                    return i + 1 

            # Hitta tom plats
            for i, content in enumerate(self.slots):
                if not content: 
                    self.slots[i] = encode(vehicle)
                    return i + 1 
                    
        return None 

    def unpark_vehicle(self, reg_nr):
        search_result = self.search_vehicle(reg_nr)
        slot_number, v_type = search_result if search_result else (None, None) 
        
        if not slot_number: return None 
            
        index = slot_number - 1
        content = self.slots[index]
        reg_nr = reg_nr.upper()
        
        if v_type == "CAR":
            self.slots[index] = ""
        elif v_type == "MC":
            v_strs = content.split(DLM_S)
            new_v_strs = [s for s in v_strs if not s.endswith(reg_nr)]
            self.slots[index] = DLM_S.join(new_v_strs)
            
        return slot_number, v_type

    def move_vehicle(self, old_slot_nr, new_slot_nr):
        old_idx = old_slot_nr - 1
        new_idx = new_slot_nr - 1
        
        if not (0 <= old_idx < CAPACITY and 0 <= new_idx < CAPACITY):
            return "Fel: Ogiltigt platsnummer."
        
        content = self.slots[old_idx]
        if not content: return f"Fel: Plats {old_slot_nr} är tom."

        reg_nr = input(f"Plats {old_slot_nr} innehåll: {content}\nAnge regnummer att flytta: ").upper()
        v_type = find_in_slot(content, reg_nr)

        if not v_type: return f"Fel: Fordon {reg_nr} hittades ej på plats {old_slot_nr}."
             
        vehicle = Car(reg_nr) if v_type == "CAR" else Motorcycle(reg_nr)
        encoded_v = encode(vehicle)

        new_content = self.slots[new_idx]
        
        if v_type == "CAR" and new_content:
             return f"Fel: Kan ej flytta Bil till plats {new_slot_nr}. Plats upptagen."
        if v_type == "MC" and DLM_S in new_content:
             return f"Fel: Kan ej flytta MC till plats {new_slot_nr}. Plats full (2 MC)."

        self.unpark_vehicle(reg_nr)
        
        new_content = self.slots[new_idx] 

        if not new_content:
            self.slots[new_idx] = encoded_v
        else:
            self.slots[new_idx] += f"{DLM_S}{encoded_v}"

        return f"✅ Fordon {reg_nr} flyttat från {old_slot_nr} till {new_slot_nr}."