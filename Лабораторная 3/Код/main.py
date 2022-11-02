from collections import Counter


class Solver:
    # Каноническое разложение чисел m и n
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

    # Алгоритм Евклида (вторая версия)
    @staticmethod
    def euclid_algorithm(first_value: int, second_value: int) -> int:
        while first_value != second_value:
            if first_value > second_value:
                first_value -= second_value
            else:
                second_value -= first_value

        return first_value

    # Нахождение НОД
    @staticmethod
    def greatest_common_divisor(first_value: int, second_value: int, mode: str = "euclid") -> int:
        match mode:
            case "euclid":
                return Solver.euclid_algorithm(first_value, second_value)

            case "decomposition":
                memory = 1

                for key, value in (
                        Solver.canonical_decomposition(first_value) & Solver.canonical_decomposition(second_value)
                ).items():
                    memory *= key ** value

                return memory

            case _:
                raise ValueError("Mode should be 'euclid' or 'decomposition'")

    # Соотношение Безу
    @staticmethod
    def bezu_ratio(first_number: int, second_number: int) -> dict:
        u, u_, v, v_ = 1, 0, 0, 1
        while second_number:
            q = first_number // second_number
            first_number, second_number = second_number, first_number % second_number
            u, u_ = u_, u - u_ * q
            v, v_ = v_, v - v_ * q
        return {"u": u, "v": v, "gcd": first_number}

    # Вычисление Фи
    @staticmethod
    def euler_function(value: int) -> int:
        primes = Solver.canonical_decomposition(value).keys()
        multiplier = 1

        for element in primes:
            multiplier *= 1 - 1 / element

        return int(value * multiplier)

    # Взаимно обратные по умножению элементы
    @staticmethod
    def pairs_of_inverse_multiplication(value: int) -> list:
        memory = []
        degree = Solver.euler_function(value) - 1

        for i in range(2, value):
            if Solver.greatest_common_divisor(value, i) == 1:
                memory.append(i)

        for index, element in enumerate(memory):
            memory[index] = (element, pow(element, degree, value))

        return memory

    # Обратные к элементам
    @staticmethod
    def inverses_to_the_element(ring: int, value: int):
        if Solver.greatest_common_divisor(ring, value) == 1:
            return pow(value, (Solver.euler_function(ring) - 1), ring)


if __name__ == "__main__":
    M1 = 911_851_594_3
    N1 = 338_649_668_9
    K2 = 19
    N2 = 26
    M2 = 2004

    print(
        f"1. {Solver.canonical_decomposition(M1)}, {Solver.canonical_decomposition(N1)}",
        f"2. {Solver.greatest_common_divisor(M1, N1)}, {Solver.greatest_common_divisor(M1, N1, mode='decomposition')}",
        f"3. {Solver.bezu_ratio(N1, M1)}",
        f"4. {Solver.euler_function(K2)}, {Solver.euler_function(N2)}, {Solver.euler_function(M2)}",
        f"5. {Solver.pairs_of_inverse_multiplication(K2)}, {Solver.pairs_of_inverse_multiplication(N2)}",
        f"6. {Solver.inverses_to_the_element(M2, 5)}, {Solver.inverses_to_the_element(M2, 6)}, "
        f"{Solver.inverses_to_the_element(M2, 7)}",
        sep="\n",
    )
