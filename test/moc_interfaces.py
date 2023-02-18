import pypinball


class MocDisplayInterface(pypinball.DisplayInterface):
    def clear(self) -> None:
        pass

    def display_image(self, path: str) -> None:
        pass

    def update(self) -> None:
        pass
