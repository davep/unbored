"""Provides the filters input panel for the app."""

##############################################################################
# Python imports.
from typing import TypeVar

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.binding    import Binding
from textual.widgets    import Label
from textual.containers import Vertical
from textual.message    import Message
from textual.events     import DescendantBlur

##############################################################################
# Local imports.
from .focus_within import focus_within
from .filter_input import FilterInput, IntInput, FloatInput

##############################################################################
class Filters( Vertical ):
    """Filtering sidebar."""

    BINDINGS = [
        Binding( "escape", "close", "Close Filters" )
    ]
    """The bindings for the filter pop-over."""

    def compose( self ) -> ComposeResult:
        """Compose the filter panel.

        Returns:
            ComposeResult: The layout for the filters panel.
        """
        yield Label( "Filters", classes="h1" )
        yield Label( "Participants:", classes="h2" )
        yield IntInput( id="participants", placeholder="Number of participants" )
        yield Label( "Minimum Price:", classes="h2" )
        yield FloatInput( id="min_price", placeholder="Between 0 (free) and 1 (expensive)" )
        yield Label( "Maximum Price:", classes="h2" )
        yield FloatInput( id="max_price", placeholder="Between 0 (free) and 1 (expensive)" )
        yield Label( "Minimum Accessibility:", classes="h2" )
        yield FloatInput( id="min_accessibility", placeholder="Between 0 (most) and 1 (least)" )
        yield Label( "Maximum Accessibility:", classes="h2" )
        yield FloatInput( id="max_accessibility", placeholder="Between 0 (most) and 1 (least)" )

    def on_descendant_blur( self, _: DescendantBlur ) -> None:
        """Watch and handle focus changes in the inputs."""
        # If focus moved outside of our inputs...
        if not focus_within( self ):
            # ...auto-close.
            self.hide()

    def on_mount( self ) -> None:
        """Configure the filters once we're composed."""
        self.hide()

    @property
    def participants( self ) -> int | None:
        """int | None: The participants filter value.

        If the user appears to have provided a value, it will be an integer.
        If there is no given value or it doesn't look this will be `None`.
        """
        try:
            if ( value := int( self.query_one( "#participants", IntInput ).value.strip() ) ) > 0:
                return value
        except ValueError:
            pass
        return None

    TClamp = TypeVar( "TClamp", int, float )
    """A clampable type."""

    @staticmethod
    def clamp( value: TClamp | None, min_val : TClamp, max_val: TClamp ) -> TClamp | None:
        """Clamp a value.

        Args:
            value (TClamp | None): The value to clamp.
            min_val (TClamp): The minimum value.
            max_val (TClamp): The maximum value.

        Returns:
            TClamp | None: The clamped value.

        Note:
            If the value is `None`, then `None` will be returned.
        """
        if value is None:
            return value
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value

    def _min_max_value( self, value: str ) -> tuple[ float | None, float | None ]:
        """Get a min/max float value from the filters.

        Args:
            value (str): The name of the filter value to get.

        Returns:
            tuple[ float | None, float | None ]: The filter value.
        """
        def _value( which: str ) -> float | None:
            try:
                if ( price := float(
                        self.query_one( f"#{which}_{value}", FloatInput ).value.strip()
                ) ) <= 0:
                    price = None
            except ValueError:
                price = None
            return price

        # Get the filter values.
        min_value = self.clamp( _value( "min" ), 0, 1 )
        max_value = self.clamp( _value( "max" ), 0, 1 )

        # Let's be nicer to a confused user, I guess.
        if min_value is not None and max_value is not None and max_value < min_value:
            return max_value, min_value

        # Finally, return what we've got.
        return min_value, max_value

    @property
    def price( self ) -> tuple[ float | None, float | None ]:
        """tuple[ float | None, float | None ]: The price filter.

        A tuple of minimum and maximum price filters. If no filter value was
        provided for either of the values then they will be `None`.
        """
        return self._min_max_value( "price" )

    @property
    def accessibility( self ) -> tuple[ float | None, float | None ]:
        """tuple[ float | None, float | None ]: The accessibility filter.

        A tuple of minimum and maximum accessibility filters. If no filter
        value was provided for either of the values then they will be
        `None`.
        """
        return self._min_max_value( "accessibility" )

    def action_close( self ) -> None:
        """Close action for the filters."""
        self.hide()

    class Shown( Message ):
        """Message sent out when the filters are shown."""

    def show( self ) -> None:
        """Show the filter options."""
        for field in self.query( FilterInput ):
            field.can_focus = True
        self.query( FilterInput ).first().focus()
        self.remove_class( "hidden" )
        self.emit_no_wait( self.Shown( self ) )

    class Hidden( Message ):
        """Message sent out when the filters are hidden."""

    def hide( self ) -> None:
        """Hide the filter options."""
        self.add_class( "hidden" )
        for field in self.query( FilterInput ):
            field.can_focus = False
        self.emit_no_wait( self.Hidden( self ) )

    @property
    def shown( self ) -> bool:
        """bool: Are the filters currently shown?"""
        return not self.has_class( "hidden" )

### filters.py ends here
