"""Provides a widget for making activity type choices."""

##############################################################################
# BoredAPI imports.
from bored_api import ActivityType

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.containers import Container
from textual.widgets    import Button

##############################################################################
class TypeChoices( Container ):
    """Container widget for the type choices buttons."""

    def compose( self ) -> ComposeResult:
        """Compose the type choices button collection.

        Returns:
            ComposeResult: The layout for the type choice buttons.
        """
        yield Button( "Any", id="any" )
        yield from ( Button(
            activity.value.capitalize(), id=activity.value
        ) for activity in ActivityType )

### type_choices.py ends here
