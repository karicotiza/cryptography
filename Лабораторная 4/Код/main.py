import numpy as np
import random
from math import gcd
from collections import Counter


class Substitution:
    def __init__(self, top_row: list, bottom_row):
        self.__array = np.array(
            [
                top_row,
                bottom_row,
            ]
        )

    def __mul__(self, other):
        if not isinstance(other, Substitution):
            raise TypeError("A substitution can only be multiplied by a substitution")

        memory = []

        for value in other.get_substitution()[0]:
            index = np.where(other.get_substitution()[1] == value)[0][0]
            index = other.get_substitution()[0][index]
            index = np.where(self.__array[0] == index)[0][0]
            memory.append(self.__array[1][index])

        return Substitution(other.get_substitution()[0], memory)

    def __str__(self):
        return str(self.get_substitution())

    def __swap_rows(self) -> np.array:
        return np.flip(self.__array)

    def __sort_columns(self) -> np.array:
        return self.__swap_rows()[:, self.__swap_rows()[0].argsort()]

    def get_substitution(self) -> np.array:
        return self.__array

    def get_reverse_substitution(self) -> np.array:
        return self.__sort_columns()

    def get_cycles(self) -> list:
        memory = []
        array = self.__array

        while len(array[0]) > 0:
            index = 0
            sequence = []
            locations = []

            while True:
                if len(locations) > 1:
                    if locations[0] == locations[-1]:
                        sequence.pop()
                        break
                index = np.where(array[0] == array[1][index])[0][0]
                sequence.append(array[0, index])
                locations.append(index)

            memory.append(sequence)
            array = np.delete(array, locations, axis=1)

        return [tuple(sequence) for sequence in memory]

    @staticmethod
    def get_random_substitution(size: int, radius: int):
        memory = random.sample(range(1, radius + 1), size)

        return Substitution(
            memory,
            random.sample(memory, size)
        )


# class Primes:
#     @staticmethod
#     def list_of_primes(value: int) -> np.array:
#         memory = np.ones(value // 3 + (value % 6 == 2), dtype=bool)
#         for i in range(1, int(value ** 0.5) // 3 + 1):
#             if memory[i]:
#                 k = 3 * i + 1 | 1
#                 memory[k * k // 3::2 * k] = False
#                 memory[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
#         return np.r_[2, 3, ((3 * np.nonzero(memory)[0][1:] + 1) | 1)]
#
#     @staticmethod
#     def primes_in_range(start: int, stop: int) -> np.array:
#         return Primes.list_of_primes(stop)[np.where(Primes.list_of_primes(stop) >= start)[0][0]::]


class CyclicGroups:
    @staticmethod
    def is_cyclic(value: int, verbose: bool = False):
        decomposition = CyclicGroups.canonical_decomposition(value)
        if verbose:
            print(decomposition)

        conditions = [
            value == 1,
            value == 2,
            value == 4,
            len(decomposition) == 1,
            len(decomposition) == 2 and decomposition[2] == 1
        ]

        return True if True in conditions else False

    @staticmethod
    def canonical_decomposition(value: int) -> Counter:
        memory = []
        prime_number = 2

        while prime_number ** 2 <= value:
            if value % prime_number == 0:
                memory.append(prime_number)
                value //= prime_number
            else:
                prime_number += 1

        if value > 1:
            memory.append(value)

        return Counter(memory)

    @staticmethod
    def find_any_forming_element(value: int):
        decomposition = CyclicGroups.canonical_decomposition(value - 1)
        for number in range(2, value):
            flag = False
            for element in list(decomposition.keys()):
                result = pow(number, int((value - 1) / element), value)
                if result == 1:
                    flag = True
            if flag:
                continue
            return number

    @staticmethod
    def find_all_forming_element(value: int):
        co_prime_set = {
            number for
            number in
            range(1, value)
            if gcd(number, value) == 1
        }

        return [
            element for
            element in
            range(1, value)
            if co_prime_set == {
                pow(element, powers, value) for
                powers in
                range(1, value)
            }
        ]


if __name__ == "__main__":
    f = Substitution(
        [1, 2, 3, 4, 5, 6, 7],
        [5, 7, 2, 4, 6, 1, 3],
    )

    g = Substitution(
        [1, 2, 3, 4, 5, 6, 7],
        [4, 7, 3, 6, 2, 5, 1],
    )

    # print(f.get_reverse_substitution())
    # print(f * g)
    # print(g * f)
    # print(f.get_cycles())
    # print(Substitution.get_random_substitution(7, 7))

    # m = {
    #     1: 60951,
    #     2: 493039,
    #     3: 18,
    #     4: 2741,
    # }
    #
    # print(CyclicGroups.is_cyclic(m[1]))
    # print(CyclicGroups.is_cyclic(m[2]))
    # print(CyclicGroups.find_all_forming_element(m[3]))
    # print(CyclicGroups.find_any_forming_element(m[4]))

    print(Primes.primes_in_range(20_000, 100_000_00))
