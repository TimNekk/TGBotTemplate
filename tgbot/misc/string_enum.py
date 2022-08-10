from enum import Enum
from typing import Any


class StringEnum(Enum):
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        return self.name
