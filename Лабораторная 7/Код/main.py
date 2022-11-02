class Misc:
    @staticmethod
    def is_value_reducible(value_: int) -> bool:
        return pow(
            -1,
            int(
                (value_ - 1) / 2
            ),
            value_,
        ) == 1

    @staticmethod
    def is_polynomial_reducible(polynomial_: str) -> bool:
        polynomial_ = [int(letter) for letter in polynomial_ if letter.isdigit()]
        return not max(polynomial_) > 7


class Polynomial:
    def __init__(self, equation: str) -> None:
        self.__equation = equation

    def get_degrees(self):
        return f"degrees of 'x': {tuple(self)}"

    @staticmethod
    def __calculate_polynomial(iterable) -> int:
        memory_ = 0

        for degree in iterable:
            memory_ += 2 ** degree

        return memory_

    def __iter__(self):
        for letter in (
            self.__equation
                .replace("x ** ", "")
                .replace(" + ", "")
        ):
            if letter.isdigit():
                letter = int(letter)
                if letter > 1:
                    yield letter
                else:
                    yield 0
            elif letter == "x":
                yield 1
            else:
                pass

    def __str__(self):
        return self.__equation

    def __int__(self):
        return self.__calculate_polynomial(self)

    def __index__(self):
        return int(self)

    def __add__(self, other):
        return int(self) ^ int(other)

    def __radd__(self, other):
        return int(self) ^ int(other)

    def __mul__(self, other):
        a_ = int(self)
        b_ = int(other)
        product = 0
        for _ in range(8):
            if (b_ & 1) == 1:
                product ^= a_
            hi_bit_set = a_ & 0x80
            a_ = (a_ << 1) & 0xFF
            if hi_bit_set == 0x80:
                a_ ^= 0x1B
            b_ >>= 1
        return int(product)


class Hex:
    @staticmethod
    def int_to_hex(value: int) -> str:
        return hex(value)[2:].upper()

    @staticmethod
    def hex_to_int(value: str) -> int:
        return int(value, base=16)

    @staticmethod
    def hex_to_polynomial(value: str) -> Polynomial:
        memory_ = []

        for index, byte in enumerate(bin(Hex.hex_to_int(value))[::-1][:-2]):
            byte = int(byte)
            if byte:
                if index == 0:
                    memory_.append(" + 1")
                elif index == 1:
                    memory_.append(" + x")
                elif index + 1 == len(bin(Hex.hex_to_int(value))[::-1][:-2]):
                    memory_.append(f"x ** {index}")
                else:
                    memory_.append(f" + x ** {index}")

        return Polynomial("".join(reversed(memory_)))


if __name__ == "__main__":
    p = (
        17, 13, 23, 7, 73, 3, 41, 29
    )

    polynomials_1 = (
        "x ** 8 + x ** 7 + x ** 4 + 1",
        "x ** 8 + x ** 7 + x ** 4 + x ** 2 + 1",
        "x ** 8 + x ** 5 + x ** 4 + x ** 3 + x ** 2 + 1",
        "x ** 8 + x ** 7 + x ** 3 + 1"
    )

    polynomials_2 = (
        "x ** 8 + x ** 7 + x ** 3 + 1",
        "x ** 7 + x ** 3 + 1",

        "x ** 8 + x ** 5 + x ** 3 + x ** 2 + 1",
        "x ** 5 + x ** 3 + x ** 2 + 1",

        "x ** 8 + x ** 4 + x ** 3 + x ** 2 + 1",
        "x ** 4 + x ** 3 + x ** 2 + 1",

        "x ** 8 + x ** 6 + x ** 5 + x + 1",
        "x ** 6 + x ** 5 + x ** 2 + 1",
    )

    for element in p:
        print(f"Is {element} reducible - {Misc.is_value_reducible(element)}")

    for element in polynomials_1:
        print(f"Is '{element}' reducible - {Misc.is_polynomial_reducible(element)}")

    for element in polynomials_2:
        memory = Polynomial(element)
        print(
            f"Equation: {memory}",
            f"Degrees: {memory.get_degrees()}",
            f"HEX: {Hex.int_to_hex(int(memory))}",
            sep="\n",
            end="\n\n"
        )

    a = Hex.hex_to_polynomial("74")
    b = Hex.hex_to_polynomial("D5")
    print(f"'{Hex.int_to_hex(int(a))}' + '{Hex.int_to_hex(int(b))}' = '{Hex.int_to_hex(a + b)}'")
    print(f"'{Hex.int_to_hex(int(a))}' * '{Hex.int_to_hex(int(b))}' = '{Hex.int_to_hex(a * b)}'")
