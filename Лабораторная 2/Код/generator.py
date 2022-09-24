from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Sequence:
    x1: int
    x2: int = 0
    x3: int = 0

    def get(self):
        return self.x1, self.x2, self.x3


class Generator:
    def __init__(self):
        self.__SEED = datetime.now().microsecond

    def __generate(self, iterations: int):
        memory = []

        x1, x2, x3 = Sequence(
            self.__SEED
        ).get()

        for index in range(iterations):
            x = (1176 * x3 + 1476 * x2 + 1776 * x1) % (2 ** 32 - 5)
            x1, x2, x3 = x, x1, x2
            memory.append(x)

        return memory

    def get(self, iterations: int):
        return self.__generate(iterations)

    def to_file(self, path: Path, iterations: int):
        with open(path, mode="w", encoding="utf-8") as file:
            for element in self.__generate(iterations):
                file.write(
                    str(element) + "\n"
                )


if __name__ == "__main__":
    generator = Generator()
    generator.to_file(
        Path("../test.txt"),
        1_000_000
    )
