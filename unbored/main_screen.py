"""Provides the main screen for the application."""

##############################################################################
# Python imports.
from dataclasses import asdict, is_dataclass
from datetime import datetime
from json import JSONEncoder, dumps, loads
from pathlib import Path
from typing import Any, Final

##############################################################################
# BoredAPI imports.
from bored_api import ActivityType, BoredClient, BoredException

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header

##############################################################################
# XDG imports.
from xdg import xdg_data_home

from .activity import Activity
from .filters import Filters

##############################################################################
# Local imports.
from .type_choices import TypeChoices


##############################################################################
class ActivityEncoder(JSONEncoder):
    """JSON encoder that understands about activities."""

    def default(self, o: object) -> Any:
        """Handle unknown values."""
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, ActivityType):
            return o.value
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


##############################################################################
class Main(Screen):
    """The main application screen."""

    BINDINGS = [
        Binding("m", "toggle_darkness", "Light/Dark Mode"),
        Binding("f", "filters", "Filters"),
        Binding("escape", "quit", "Close"),
    ]
    """The bindings for the main screen."""

    def compose(self) -> ComposeResult:
        """Compose the main screen.

        Returns:
            The layout for the main screen.
        """

        # pylint:disable=attribute-defined-outside-init
        self.choices = TypeChoices()
        self.activities = VerticalScroll(id="activities")
        self.filters = Filters(classes="hidden")

        # We don't want the activities list to get focus, only the stuff
        # inside.
        self.activities.can_focus = False

        yield Header()
        with Vertical():
            yield self.choices
            yield self.activities
            yield self.filters
        yield Footer()

    def on_mount(self) -> None:
        """Set up the screen on mount."""
        self.api = BoredClient()
        self.choices.become_focused()
        self.load_activity_list()

    ACTIVITY_FILE: Final = Path("unbored.json")
    """The name of the file that the list it saved to."""

    @property
    def data_file(self) -> Path:
        """The full path to the file for saving the data.

        Note:
            As a side effect of access the directory will be crated if it
            doesn't exist.
        """
        (save_to := xdg_data_home() / "unbored").mkdir(parents=True, exist_ok=True)
        return save_to / self.ACTIVITY_FILE

    def save_activity_list(self) -> None:
        """Save the activity list to disk."""
        self.data_file.write_text(
            dumps(
                [activity.as_dict for activity in self.activities.query(Activity)],
                cls=ActivityEncoder,
                indent=4,
            )
        )

    def load_activity_list(self) -> None:
        """Load the activity list from disk."""
        if self.data_file.exists():
            to_mount: list[Activity] = []
            for activity in loads(self.data_file.read_text()):
                activity["type"] = ActivityType(activity["type"])
                to_mount.append(Activity.from_dict(activity))
            if to_mount:
                self.activities.mount(*to_mount)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the button press."""

        # We're going to build up a collection of options to dictate the
        # choice made.
        options: dict[str, Any] = {}

        # If the button wasn't the any button, it'll have been one of the
        # activity type buttons. The filter value is in the button ID.
        if event.button.id is not None and event.button.id != "any":
            options["type"] = event.button.id

        # If it looks like we've got a participants filter...
        if (participants := self.filters.participants) is not None:
            # ...add that.
            options["participants"] = participants

        # See if we should apply price filtering.
        min_price, max_price = self.filters.price
        if min_price is not None:
            options["min_price"] = min_price
        if max_price is not None:
            options["max_price"] = max_price

        # See if we should apply accessibility filtering.
        min_accessibility, max_accessibility = self.filters.accessibility
        if min_accessibility is not None:
            options["min_accessibility"] = min_accessibility
        if max_accessibility is not None:
            options["max_accessibility"] = max_accessibility

        # Get the new activity.
        try:
            await self.activities.mount(
                Activity(await self.api.get(**options)), before=0
            )
            self.save_activity_list()
        except BoredException:
            self.notify(
                "Unable to find any activities that satisfy the current filters.",
                severity="error",
            )

    def action_filters(self) -> None:
        """Toggle the display of the filters."""
        if self.filters.shown:
            self.filters.hide()
        else:
            self.filters.show()

    def action_toggle_darkness(self) -> None:
        """Toggle dark mode for the application."""
        self.app.dark = not self.app.dark

    def on_activity_moved(self, _: Activity.Moved) -> None:
        """React to an activity being moved."""
        self.save_activity_list()

    def on_activity_dropped(self, _: Activity.Dropped) -> None:
        """React to an activity being dropped."""
        self.save_activity_list()

    def on_activity_deselect(self) -> None:
        """Handle an activity wanting to give up focus."""
        self.choices.become_focused()

    def on_filters_hidden(self) -> None:
        """Handle the filters being hidden."""
        self.choices.become_focused()


### main_screen.py ends here
