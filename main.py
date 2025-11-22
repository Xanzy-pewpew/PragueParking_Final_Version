import sys
from parking_manager import ParkingManager, CAPACITY 
from models import Car, Motorcycle 
from utils import decode

parking_manager = ParkingManager()

# Hjälpfunktioner
def get_valid_reg_nr():
    while True:
        reg_nr = input("Ange regnummer (max 10 tecken): ").strip().upper()
        if 1 <= len(reg_nr) <= 10 and ' ' not in reg_nr and '#' not in reg_nr and '|' not in reg_nr:
            return reg_nr
        print("Ogiltigt regnummer.")

def get_valid_slot_nr(prompt):
    while True:
        try:
            slot_nr = int(input(prompt))
            if 1 <= slot_nr <= CAPACITY: return slot_nr
            print(f"Ogiltigt platsnummer (1-{CAPACITY}).")
        except ValueError:
            print("Ogiltig inmatning. Ange ett heltal.")


# Hanteringsfunktioner

def handle_park_vehicle():
    print("\n--- 1. Parkera ---")
    reg_nr = get_valid_reg_nr()
    if parking_manager.search_vehicle(reg_nr)[0]: return print(f"❌ Fordon {reg_nr} redan parkerat.")
        
    v_type_input = input("Bil (B) eller Motorcykel (M)? ").upper()
    if v_type_input == 'B': vehicle = Car(reg_nr)
    elif v_type_input == 'M': vehicle = Motorcycle(reg_nr)
    else: return print("Ogiltigt val.")
            
    slot_nr = parking_manager.park_vehicle(vehicle)
    
    if slot_nr: print(f"✅ Fordon {reg_nr} parkerat! Kör till plats **{slot_nr}**.")
    else: print("❌ Tyvärr, parkeringen är full.")

def handle_unpark_vehicle():
    print("\n--- 2. Avparkera ---")
    reg_nr = get_valid_reg_nr()
    result = parking_manager.unpark_vehicle(reg_nr)
    
    if result:
        slot_nr, v_type = result
        print(f"✅ Fordon {reg_nr} ({v_type}) uthämtat från plats {slot_nr}.")
    else:
        print(f"❌ Fordon {reg_nr} hittades inte.")

def handle_move_vehicle():
    print("\n--- 3. Flytta fordon ---")
    old_slot_nr = get_valid_slot_nr("Från plats (1-100): ")
    new_slot_nr = get_valid_slot_nr("Till plats (1-100): ")
    print(parking_manager.move_vehicle(old_slot_nr, new_slot_nr))

def handle_search_vehicle():
    print("\n--- 4. Sök fordon ---")
    reg_nr = get_valid_reg_nr()
    slot_nr, v_type = parking_manager.search_vehicle(reg_nr)
    
    if slot_nr: print(f"🔎 Fordon {reg_nr} ({v_type}) hittades på plats **{slot_nr}**.")
    else: print(f"❌ Fordon {reg_nr} hittades inte.")

def handle_visualization():
    print("\n--- 5. Översikt ---")
    occupied_count = 0
    
    for i in range(CAPACITY):
        slot_nr = i + 1
        content = parking_manager.slots[i]
        
        if content:
            occupied_count += 1
            decoded = decode(content)
            
            if len(decoded) == 1 and decoded[0][0] == "CAR": status = "BIL"
            elif len(decoded) == 2 and decoded[0][0] == "MC": status = "MC x2 (FULL)"
            elif len(decoded) == 1 and decoded[0][0] == "MC": status = "MC x1"
            else: status = "Upptagen"
                
            print(f"Plats {slot_nr:03d} [{status:<13}]: {content}")
            
    print(f"\nStatistik: {occupied_count} av {CAPACITY} platser är upptagna.")


# Huvudmeny

def main_menu():
    parking_manager.park_vehicle(Car("BILAR1"))
    parking_manager.park_vehicle(Motorcycle("MCY1"))
    parking_manager.park_vehicle(Motorcycle("MCY2")) 

    options = {
        '1': handle_park_vehicle,
        '2': handle_unpark_vehicle,
        '3': handle_move_vehicle,
        '4': handle_search_vehicle,
        '5': handle_visualization,
        '6': lambda: (print("Programmet avslutas."), sys.exit(0))
    }

    while True:
        print("\n=== Prague Parking V1 ===")
        print("1. Parkera\n2. Avparkera\n3. Flytta\n4. Sök\n5. Översikt\n6. Avsluta")
        choice = input("Välj (1-6): ")
        
        action = options.get(choice)
        if action:
            action()
        else:
            print("Ogiltigt val.")

if __name__ == "__main__":
    main_menu()