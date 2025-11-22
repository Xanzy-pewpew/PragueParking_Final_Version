from flask import Flask
# Importerar din nya ParkingGarage-klass från ditt nya modul/paket
from parking_core.garage_manager import ParkingGarage 

app = Flask(__name__) 
parking_garage = ParkingGarage()

@app.route('/')
def hello_world():
    # Visar att garaget kunde initialiseras och läsa konfiguration
    spot_count = len(parking_garage.spots)
    return f'Prague Parking V2 API is running! Config loaded. Capacity: {spot_count} spots.' 