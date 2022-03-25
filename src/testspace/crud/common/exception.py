


class NotFoundException(Exception):
    def __init__(self, item, message) -> None:
        super().__init__(item, message)
        self.item = item
        self.message = message