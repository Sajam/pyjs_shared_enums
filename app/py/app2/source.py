from enum import Enum


class ColorsEnum(Enum):
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]

    @property
    def darker(self):
        new = [100, 100, 100]
        new[self.value.index(255)] = 255

        return new
