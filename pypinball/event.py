import typing


class Event:
    """
    The Event class can be used to handle event by registering callback methods
    which are then called when the Event is emitted using the ``emit()`` method
    or the ``__call__()`` dunder method.
    """

    def __init__(self):
        self._handlers: typing.Set[typing.Callable] = set()

    def __call__(self, *args, **kwargs) -> None:
        self.emit(*args, **kwargs)

    def __add__(self, other: typing.Callable):
        self.register_handler(func=other)
        return self

    def __sub__(self, other: typing.Callable):
        self.unregister_handler(func=other)
        return self

    @property
    def num_handlers(self) -> int:
        """
        Get the number of registered handlers.

        Returns:
            int: Number of handlers.
        """
        return len(self._handlers)

    def clear(self) -> None:
        """
        Clear all the registered handlers.

        Returns:
            None
        """
        self._handlers.clear()

    def emit(self, *args, **kwargs) -> None:
        """
        Emit the event.

        Args:
            *args:
            **kwargs:

        Returns:
            None
        """
        for func in self._handlers:
            if not callable(func):
                continue
            func(*args, **kwargs)

    def register_handler(self, func: typing.Callable) -> None:
        """
        Register a callback handler.

        Args:
            func: Callback function.

        Returns:
            None
        """
        self._handlers.add(func)

    def unregister_handler(self, func: typing.Callable) -> None:
        """
        Unregister a callback handler.

        Args:
            func: Callback function.

        Returns:
            None
        """
        self._handlers.remove(func)
