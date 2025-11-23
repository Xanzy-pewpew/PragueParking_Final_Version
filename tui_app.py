from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container
from parking_core.garage_manager import ParkingGarage
from parking_core.models import Car 
from rich.panel import Panel
from input_screen import InputScreen

garage = ParkingGarage()

class StatusDisplay(Static):
    """Widget för att visa garagestatus."""
    def on_mount(self) -> None:
        self.update_status()

    def update_status(self):
        """Uppdaterar texten med aktuell information."""
        total_spots = len(garage.spots)
        occupied_spots = sum(1 for spot in garage.spots if spot.vehicles)
        
        status_text = (
            f"[bold green]PRAGUE PARKING V2[/bold green]\n"
            f"----------------------------------\n"
            f"🅿️ Totala Platser: [yellow]{total_spots}[/yellow]\n"
            f"🚗 Antal upptagna: [red]{occupied_spots}[/red]"
        )
        self.update(Panel(status_text, title="[b]Garage Status[/b]", border_style="cyan"))

class PragueParkingApp(App[None]):
    """Huvudapplikationen för Textual TUI."""
    
    BINDINGS = [
        ("q", "quit", "Avsluta (Q)"),
    ]
    
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
            StatusDisplay(),
            Button("1. Parkera Bil", id="park_btn", variant="primary"),
            Button("2. Hämta Bil", id="unpark_btn"),
        )
        yield Footer()

    def action_quit(self) -> None:
        """Avslutar applikationen."""
        self.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Hanterar knapptryckningar."""
        
        if event.button.id == "park_btn":
            self.push_screen(
                InputScreen(title="Parkera fordon", button_text="Parkera"),
                self.handle_parking_result,
            )
        
        elif event.button.id == "unpark_btn":
            self.push_screen(
                InputScreen(title="Hämta fordon", button_text="Hämta"),
                self.handle_unparking_result,
            )


    def handle_parking_result(self, reg_nr: str | None) -> None:
        """Hanterar resultatet från input-skärmen för parkering."""
        status_widget = self.query_one(StatusDisplay)
        
        if not reg_nr:
            self.notify("Parkering avbruten.", title="Parkering", severity="warning")
            return

        car = Car(reg_nr)
        spot_id = garage.park_vehicle(car)
        
        status_widget.update_status()

        if spot_id:
            self.notify(f"Bilen {reg_nr} parkerad på plats #{spot_id}", title="Parkering Lyckades", timeout=3)
        else:
            self.notify("Kunde inte parkera! Garaget fullt.", title="Fel", severity="error")

    
    def handle_unparking_result(self, reg_nr: str | None) -> None:
        """Hanterar resultatet från input-skärmen för uthämtning."""
        status_widget = self.query_one(StatusDisplay)
        
        if not reg_nr:
            self.notify("Uthämtning avbruten.", title="Uthämtning", severity="warning")
            return

        result = garage.unpark_vehicle(reg_nr)
        status_widget.update_status()

        if result:
            self.notify(f"Hämtat {result['reg_nr']} från plats #{result['spot_id']}. Pris: {result['price']} SEK (Dummy).", title="Uthämtning Lyckades", timeout=5)
        else:
            self.notify(f"Kunde inte hitta fordonet {reg_nr}.", title="Fel", severity="error")

if __name__ == "__main__":
    app = PragueParkingApp()
    app.run()