"""Provides the widget that holds the details of an activity."""

##############################################################################
# Python imports.
from typing      import Any, cast
from datetime    import datetime
from dataclasses import asdict
from webbrowser  import open as open_url

##############################################################################
# BoredAPI imports.
from bored_api import BoredActivity

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.binding    import Binding
from textual.widget     import Widget
from textual.widgets    import Static, Button
from textual.containers import Horizontal
from textual.message    import Message
from textual.events     import MouseDown

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Local imports.
from .focus_within import focus_within

##############################################################################
class WebLink( Button ):
    """A button that links to a URL."""

    def __init__( self, link: str ) -> None:
        """Initialise the link button."""
        self._link = link
        super().__init__( Text.from_markup( ":link:" ), variant="primary" )

    def visit( self ) -> None:
        """Visit the URL for the link."""
        open_url( self._link )

##############################################################################
class Activity( Widget ):
    """A widget that holds and displays a suggested activity."""

    BINDINGS = [
        Binding( "d", "delete", "Delete" ),
        Binding( "ctrl+up", "move_up", "Move Up" ),
        Binding( "ctrl+down", "move_down", "Move Down" ),
        Binding( "escape", "deselect", "Switch to Types" )
    ]
    """Bindings for the widget."""

    def __init__( self, activity: BoredActivity, chosen_at: datetime | None = None ):
        """Initialise the activity widget.

        Args:
            activity (BoredActivity): The activity to display.
            chosen_at (datetime | None, optional): the time the activity was chosen.
        """
        super().__init__()
        self.activity  = activity
        self.chosen_at = datetime.now() if chosen_at is None else chosen_at

    @property
    def as_dict( self ) -> dict[ str, Any ]:
        """dict[ str, Any]: The activity as a dictionary."""
        return asdict( self.activity ) | { "chosen_at": self.chosen_at }

    @staticmethod
    def from_dict( activity: dict[ str, Any ] ) -> "Activity":
        """Create a new activity from the given dictionary.

        Args:
            activity (dict[ str, Any]): The dictionary to load data from.

        Returns:
            Activity: An activity widget created from the data.
        """
        chosen_at = datetime.fromisoformat( activity[ "chosen_at" ] )
        del activity[ "chosen_at" ]
        return Activity( BoredActivity( **activity ), chosen_at )

    @property
    def is_first( self ) -> bool:
        """bool: Is this the first activity in the activity list?"""
        return self.parent is not None and self.parent.children[ 0 ] == self

    @property
    def is_last( self ) -> bool:
        """bool: Is this the last activity in the activity list?"""
        return self.parent is not None and self.parent.children[ -1 ] == self

    class Moved( Message ):
        """A message to indicate that an activity has moved."""

    def action_move_up( self ) -> None:
        """Move this activity up one place in the list."""
        if self.parent is not None and not self.is_first:
            parent = cast( Widget, self.parent )
            parent.move_child(
                self, before=parent.children.index( self ) - 1
            )
            self.emit_no_wait( self.Moved( self ) )
            self.scroll_visible()

    def action_move_down( self ) -> None:
        """Move this activity up down place in the list."""
        if self.parent is not None and not self.is_last:
            cast( Widget, self.parent ).move_child(
                self, after=self.parent.children.index( self ) + 1
            )
            self.emit_no_wait( self.Moved( self ) )
            self.scroll_visible()

    def compose( self ) -> ComposeResult:
        """Compose the activity.

        Returns:
            ComposeResult: The layout for the main screen.
        """
        yield Static( self.chosen_at.strftime( '%c' ), classes="timestamp" )
        yield Static(
            f"[b]{self.activity.activity}[/b]\n\n"
            f"It's considered to have an accessibility of score of {self.activity.accessibility}"
            " (0 being the most accessible; 1 being the least), "
            f"is a {self.activity.type.value} type of activity, "
            + (
                f"requires {self.activity.participants} participants "
                if self.activity.participants > 1 else ""
            ) +
            f"and has a price score of {self.activity.price} (0 being free)."
        )
        yield Horizontal(
            Button(
                Text.from_markup( ":up_arrow:" ),
                id="up", classes="mover", variant="primary"
            ),
            Button(
                Text.from_markup( ":down_arrow:" ),
                id="down", classes="mover", variant="primary"
            ),
            *( [ WebLink( link=self.activity.link ) ] if self.activity.link else [] ),
            Button( Text.from_markup( ":cross_mark:" ), id="delete", variant="primary" ),
            classes="buttons"
        )

    class Dropped( Message ):
        """A message to indicate that an activity was dropped."""

    async def drop_activity( self ) -> None:
        """Drop the current activity, letting the parent know we're doing so."""
        # This seems to work, I can't make this fail, but I'm not 100%
        # convinced by this. I want the parent to know that I'm being
        # removed, and I want to remove. I want the parent to know I've been
        # removed *after* I've been removed because it will want to save the
        # list and I should be missing from it. That would suggest the
        # remove comes first then the message send follows, but Textual gets
        # very upset (for reasons that seem to make sense) if I do that.
        #
        # So here I am, sending the message and *then* removing and... it
        # seems to work and I don't know why if I'm honest.
        await self.emit( self.Dropped( self ) )
        await self.remove()

    async def on_button_pressed( self, event: Button.Pressed ) -> None:
        """React to a button being pressed on the widget."""
        event.stop()
        if event.button.id == "delete":
            await self.drop_activity()
        elif event.button.id == "up":
            self.action_move_up()
        elif event.button.id == "down":
            self.action_move_down()
        elif isinstance( event.button, WebLink ):
            event.button.visit()

    async def action_delete( self ) -> None:
        """Delete action; removes this activity."""
        await self.drop_activity()

    def on_mouse_down( self, _: MouseDown ) -> None:
        """React to the mouse button going down within us."""
        if not focus_within( self ):
            self.query( Button ).first().focus()
            self.scroll_visible()

    class Deselect( Message ):
        """Message to send when a user wants to deselect an action."""

    def action_deselect( self ) -> None:
        """Message the parent that we want to give up focus."""
        self.emit_no_wait( self.Deselect( self ) )

### activity.py ends here
