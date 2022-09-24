import random as rd
import pathlib
import pickle

PATH = "../random.pickle"
ITERATIONS = 3_000_000
LOW = 0
HIGH = 1

with open(pathlib.Path(PATH), mode="wb") as file:
    for _ in range(ITERATIONS):
        file.write(
            pickle.dumps(
                rd.randint(
                    a=LOW,
                    b=HIGH,
                )
            )
        )
