from secrets import randbelow
import pathlib
import pickle

PATH = "../secrets.pickle"
ITERATIONS = 3_000_000
HIGH = 1

with open(pathlib.Path(PATH), mode="wb") as file:
    for _ in range(ITERATIONS):
        file.write(
            pickle.dumps(
                randbelow(HIGH + 1)
            )
        )
