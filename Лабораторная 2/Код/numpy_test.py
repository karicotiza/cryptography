import pickle
import numpy as np
import pathlib

PATH = "../numpy.pickle"
ITERATIONS = 3_000_000
LOW = 0
HIGH = 1

with open(pathlib.Path(PATH), mode="wb") as file:
    for element in np.random.randint(
            low=LOW,
            high=HIGH + 1,
            size=ITERATIONS,
            dtype=np.uint8,
    ):
        file.write(
            pickle.dumps(
                int(element)
            )
        )
