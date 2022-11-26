"""Provides error messages."""

##############################################################################
# Textual imports.
from textual.app     import RenderResult
from textual.widgets import Label

##############################################################################
class NoMatchingActivities( Label ):
    """The no-matches-found error message."""

    def __init__( self ) -> None:
        """Initialise the no-matches warning."""
        super().__init__( classes="hidden" )

    def render( self ) -> RenderResult:
        """Render the no-match message.

        Returns:
            RenerResult: The content of the error message.
        """
        return "Unable to find any activities that satisfy the current filters."

    def show( self ) -> None:
        """Show the warning message."""
        self.remove_class( "hidden" )
        self.set_timer( 2, self.hide )

    def hide( self ) -> None:
        """Hide the warning message."""
        self.add_class( "hidden" )

### error_boxen.py ends here
