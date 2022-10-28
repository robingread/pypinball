import typing


class MockEventHandler:
    """
    Mock Event Handler class mainly intended for testing purposes. Internally
    this class keeps a record of all the events that have been received.
    """

    def __init__(self):
        self._events = list()

    @property
    def events(self) -> typing.List:
        """
        Get the list of received events.

        Returns:
            list: Events.
        """
        return self._events

    def clear(self) -> None:
        """
        Clear the list of recorded events.
        """
        self._events.clear()

    def handle_event(self, event) -> None:
        """
        Handle an event. This method will append the event to the internal
        list.

        Args:
            event (GameEvents): Event.
        """
        self._events.append(event)
