"""Provides fields for letting the user input filter values."""

##############################################################################
# Python imports.
from typing import Any, Callable

##############################################################################
# Textual imports.
from textual.widgets import Input

##############################################################################
class FilterInput( Input ):
    """A numeric filter input widget."""

    CAST: Callable[ [ Any ], Any ] = str
    """Callable[ [ Any ], Any ]: The casting function.

    Note: It is expected that a `ValueError` will be raised if there is a
    problem with the value.
    """

    def __init__( self, *args: Any, **kwargs: Any ) -> None:
        """Initialise the input."""
        super().__init__( *args, **kwargs )
        # TODO: Workaround for https://github.com/Textualize/textual/issues/1216
        self.value = self.validate_value( self.value )

    def validate_value( self, value: str ) -> str:
        """Validate the input.

        Args:
            value (str): The value to validate.

        Returns:
            str: The acceptable value.
        """
        # If the input field isn't empty...
        if value.strip():
            try:
                # ...run it through the casting function. We don't care
                # about what comes out of the other end, we just case that
                # it makes it through at all.
                _ = self.CAST( value )
            except ValueError:
                # It's expected that the casting function will throw a
                # ValueError if there's a problem with the conversion (see
                # int and float for example) so, here we are. Make a
                # noise...
                self.app.bell()
                # ...and return what's in the input now because we're
                # rejecting the new value.
                return self.value
        # The value to test is either empty, or valid. Let's accept it.
        return value

##############################################################################
class IntInput( FilterInput ):
    """An input widget that only accepts integer float values."""

    CAST = int

##############################################################################
class FloatInput( FilterInput ):
    """An input widget that only accepts (most) float values."""

    CAST = float

### filter_input.py ends here
