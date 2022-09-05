from typing import Optional


class PruefstelleError(Exception):
    """Exception base class"""

    def __init__(self, name: Optional[str] = None):
        self.name = name
        if name is None:
            self.name = self.__class__.__name__

    pass
