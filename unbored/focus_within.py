"""Provides a function for checking for focus within a widget."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
def focus_within( widget: Widget ) -> bool:
    """Is focus somewhere within the given widget?

    Args:
        widget (Widget): The widget to test.

    Returns:
        bool: `True` if focus is within the widget, otherwise `False`.
    """
    return bool( widget.query( "*:focus-within" ) )

### focus_within.py ends here
