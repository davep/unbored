"""Main application class for the app."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .            import __version__
from .main_screen import Main

##############################################################################
class Unbored( App[ None ] ):
    """The main application class."""

    CSS_PATH = "unbored.css"
    """The name of the CSS file for the application."""

    TITLE = "Unbored"
    """The title of the application."""

    SUB_TITLE = f"v{__version__}"
    """The sub-title of the application."""

    SCREENS = {
        "main": Main
    }
    """The collection of application screens."""

    def on_mount( self ) -> None:
        """Set up the application on startup."""
        self.push_screen( "main" )

##############################################################################
def run() -> None:
    """Run the application."""
    Unbored().run()

### app.py ends here
