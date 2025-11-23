from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Container

class InputScreen(ModalScreen[str]):
    """En modal skärm som tar emot textinmatning (t.ex. registreringsnummer)."""

    def __init__(self, title: str, button_text: str = "Fortsätt", **kwargs) -> None:
        super().__init__(**kwargs)
        self.title_text = title
        self.button_text = button_text

    def compose(self) -> ComposeResult:
        yield Container(
            Static(f"[bold white]{self.title_text}[/bold white]"),
            Input(placeholder="Ange Reg.nummer", id="input_field", classes="box"),
            Button(self.button_text, id="submit_btn", variant="primary"),
            Button("Avbryt", id="cancel_btn", variant="error"),
        )

    CSS = """
    InputScreen {
        align: center middle;
    }
    InputScreen Container {
        width: 60%;
        height: auto;
        padding: 3;
        background: $surface;
        border: heavy $accent;
    }
    #input_field {
        margin-bottom: 2;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Hanterar knapptryckningar på skärmen."""
        if event.button.id == "submit_btn":
            input_widget = self.query_one("#input_field", Input)
            self.dismiss(input_widget.value.strip().upper())
        
        elif event.button.id == "cancel_btn":
            self.dismiss(None)