from enum import Enum


class StringEnum(Enum):
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.name
