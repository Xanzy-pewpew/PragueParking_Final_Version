from textual.widgets import Static
from textual.app import ComposeResult
from rich.text import Text
from state_manager import garage # <--- NY IMPORT FRÅN STATE_MANAGER

class ParkingMap(Static):
    """Visuell karta över parkeringsgaraget (10x10) som uppdateras dynamiskt."""
    
    DEFAULT_CSS = """
    ParkingMap {
        height: 12; 
        width: auto;
        padding: 1 2;
        border: heavy steelblue;
        content-align: center top; 
    }
    """

    def on_mount(self) -> None:
        """Kallas när widgeten monteras, ritar kartan initialt."""
        self.update_map()

    def update_map(self) -> None:
        """Ritar om kartan baserat på aktuell garage-status."""
        map_text = Text()
        spots = garage.spots
        
        for i, spot in enumerate(spots):
            spot_id = i + 1
            
            # Logik för att bestämma färg/status
            if spot.available_capacity == 0:
                # Platsen är HELT FULL (röd)
                color = "red"
                symbol = " 🅿️ "
            elif spot.available_capacity == spot.max_capacity:
                # Helt LEDIG plats (grön)
                color = "green"
                symbol = " 🟢 "
            else:
                # Delvis upptagen plats (gul)
                color = "yellow"
                symbol = " 🟡 "

            # Skapa ID-strängen (t.ex. 005, 050, 100)
            id_str = str(spot_id).zfill(3) 
            
            map_text.append(f"{symbol}", style=f"bold {color}")
            map_text.append(f"{id_str} ", style="dim")
            
            # 10 platser per rad
            if spot_id % 10 == 0:
                map_text.append("\n")

        self.update(map_text)