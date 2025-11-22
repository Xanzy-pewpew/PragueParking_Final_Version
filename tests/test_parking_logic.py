import pytest
from parking_core.garage_manager import ParkingGarage
from parking_core.models import Car

@pytest.fixture
def garage():
    return ParkingGarage()

def test_garage_initializes_with_correct_capacity(garage):
    """Testar att garaget skapar rätt antal P-platser (100 från config)."""
    assert len(garage.spots) == 100
    
def test_park_car_successfully(garage):
    """Testar att en bil (storlek 4) kan parkeras på en ledig plats."""
    
    # Skapa ett fordon
    test_car = Car("ABC1234")
    
    # Försök parkera
    spot_id = garage.park_vehicle(test_car)

    assert spot_id is not None

    first_spot = garage.spots[spot_id - 1]
    assert first_spot.available_capacity == 0
    assert len(first_spot.vehicles) == 1