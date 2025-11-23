from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container
from parking_core.models import Car, Motorcycle, Bus 
from rich.panel import Panel 
from input_screen import InputScreen
from map_widget import ParkingMap
from state_manager import garage 

# Global instansen är nu flyttad till state_manager.py

class PragueParkingApp(App[None]):
    """Huvudapplikationen för Textual TUI."""
    
    BINDINGS = [
        ("q", "quit", "Avsluta (Q)"),
    ]
    
    # Uppdaterad CSS för att inkludera kart-layouten
    CSS = """
    Container {
        layout: vertical;
        padding: 1 2;
    }
    Button {
        width: 20;
        margin: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Skapar widgets (komponenterna) i applikationen."""
        yield Header(show_clock=True)
        yield Container(
            ParkingMap(), 
            Button("1. Parkera Fordon", id="park_btn", variant="primary"),
            Button("2. Hämta Fordon", id="unpark_btn"),
        )
        yield Footer()

    def action_quit(self) -> None:
        """Avslutar applikationen."""
        self.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Hanterar knapptryckningar."""
        
        if event.button.id == "park_btn":
            # UPPDATERAD PROMPT: Ber användaren om REGNR, ID och TYP
            self.push_screen(
                InputScreen(title="Parkera (Ange: REGNR,ID,TYP [Bil/MC/Buss])", button_text="Parkera"),
                self.handle_parking_result, 
            )
        
        elif event.button.id == "unpark_btn":
            # Ber användaren endast om reg.nr
            self.push_screen(
                InputScreen(title="Hämta fordon (Ange: REGNR)", button_text="Hämta"),
                self.handle_unparking_result, 
            )


    def handle_parking_result(self, full_input: str | None) -> None:
        """Hanterar resultatet från input-skärmen för parkering."""
        
        parking_map = self.query_one(ParkingMap)
        
        # Kontrollerar att vi har minst två kommatecken (3 delar totalt)
        if not full_input or full_input.count(',') < 2:
            self.notify("Ogiltigt format. Använd: Regnr,ID,Typ (Bil/MC/Buss)", title="Fel", severity="error")
            return
            
        try:
            # Delar upp input i tre delar: reg_nr, spot_id, v_type
            parts = [s.strip() for s in full_input.split(',')]
            reg_nr, spot_id_str, v_type_str = parts[0], parts[1], parts[2].lower()
            spot_id = int(spot_id_str)
        except (ValueError, IndexError):
            self.notify("Fel vid inläsning. Kontrollera formatet och att ID är ett nummer.", title="Fel", severity="error")
            return

        # Skapa fordonsobjektet baserat på typ-strängen
        vehicle = None
        if v_type_str in ["bil", "car"]:
            vehicle = Car(reg_nr)
        elif v_type_str in ["mc", "motorcycle"]:
            vehicle = Motorcycle(reg_nr)
        elif v_type_str in ["buss", "bus"]:
            vehicle = Bus(reg_nr)
        
        if vehicle is None:
            self.notify(f"Okänd fordonstyp '{v_type_str}'. Använd Bil, MC eller Buss.", title="Fel", severity="error")
            return

        # Kallar på den uppdaterade garage-metoden
        result_spot_id = garage.park_vehicle(vehicle, spot_id=spot_id) 
        
        parking_map.update_map() # UPPDATERA KARTAN VISUELLT

        if result_spot_id:
            self.notify(f"{vehicle.type} {reg_nr} parkerad på plats #{result_spot_id}", title="Parkering Lyckades", timeout=3)
        else:
            self.notify("Kunde inte parkera! Plats upptagen, för liten eller ogiltig.", title="Fel", severity="error")

    
    def handle_unparking_result(self, reg_nr: str | None) -> None:
        """Hanterar resultatet från input-skärmen för uthämtning."""
        
        parking_map = self.query_one(ParkingMap)
        
        if not reg_nr:
            self.notify("Uthämtning avbruten.", title="Uthämtning", severity="warning")
            return

        result = garage.unpark_vehicle(reg_nr)
        parking_map.update_map()

        if result:
            self.notify(f"Hämtat {result['reg_nr']} från plats #{result['spot_id']}. Pris: {result['price']} SEK (Dummy).", title="Uthämtning Lyckades", timeout=5)
        else:
            self.notify(f"Kunde inte hitta fordonet {reg_nr}.", title="Fel", severity="error")

if __name__ == "__main__":
    app = PragueParkingApp()
    app.run()