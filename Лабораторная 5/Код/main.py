import math
import random as rd
import numpy as np


class Primes:
    @staticmethod
    def __list_of_primes(value: int) -> np.array:
        memory = np.ones(value // 3 + (value % 6 == 2), dtype=bool)
        for i in range(1, int(value ** 0.5) // 3 + 1):
            if memory[i]:
                k = 3 * i + 1 | 1
                memory[k * k // 3::2 * k] = False
                memory[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
        return np.r_[2, 3, ((3 * np.nonzero(memory)[0][1:] + 1) | 1)]

    @staticmethod
    def __get_random(bits: int) -> int:
        return rd.randrange(2 ** (bits - 1) + 1, 2 ** bits - 1)

    @staticmethod
    def __get_low_level_prime(value):
        while True:
            pc = Primes.__get_random(value)

            for divisor in Primes.__list_of_primes(350):
                if pc % divisor == 0 and divisor ** 2 <= pc:
                    break
            else:
                return pc

    @staticmethod
    def __trial_composite(round_tester: int, ec: int, mrc: int, max_divisions_by_wwo: int) -> bool:
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(max_divisions_by_wwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    @staticmethod
    def __is_miller_rabin(mrc: int) -> bool:
        max_divisions_by_wwo = 0
        ec = mrc - 1
        while ec % 2 == 0:
            ec >>= 1
            max_divisions_by_wwo += 1

        number_of_rabin_trials = 20
        for i in range(number_of_rabin_trials):
            round_tester = rd.randrange(2, mrc)
            if Primes.__trial_composite(round_tester, ec, mrc, max_divisions_by_wwo):
                return False
        return True

    @staticmethod
    def get_prime(bits: int) -> int:
        while True:
            prime_candidate = Primes.__get_low_level_prime(bits)
            if not Primes.__is_miller_rabin(prime_candidate):
                continue
            else:
                return prime_candidate


class RSA:
    def __init__(self, bits: int) -> None:
        self.__p = Primes.get_prime(bits)
        self.__q = Primes.get_prime(bits)
        self.__n = self.__p * self.__q
        self.__fi = (self.__p - 1) * (self.__q - 1)
        self.__e = RSA.__find_e(self.__fi)
        self.__d = RSA.__find_d(self.__e, self.__fi)

    @staticmethod
    def __co_prime(value_1: int, value_2: int) -> bool:
        return math.gcd(value_1, value_2) == 1

    @staticmethod
    def __find_e(threshold: int) -> int:
        while True:
            memory = rd.randint(1, threshold)
            if RSA.__co_prime(threshold, memory):
                return memory

    @staticmethod
    def __find_d(e_value: int, fi_value: int) -> int:
        return pow(e_value, -1, fi_value)

    def get_parameters(self):
        return {
            "p": self.__p,
            "q": self.__q,
            "n": self.__n,
            "fi": self.__fi,
            "e": self.__e,
            "d": self.__d,
        }

    def encrypt(self, message: str) -> list:
        return [
            pow(ord(letter), self.__e, self.__n) for letter in message
        ]

    def decrypt(self, message: list) -> str:
        return "".join([
            chr(pow(element, self.__d, self.__n))
            for element
            in message
        ])

    def get_public_key(self):
        return {
            "e": self.__e,
            "n": self.__n,
        }


if __name__ == '__main__':
    bits_ = 1024
    message_ = "Привет мир, тут много текста ABCD @#$ 漢字 ?"
    rsa = RSA(bits_)
    parameters = rsa.get_parameters()

    enc = rsa.encrypt(message_)
    dec = rsa.decrypt(enc)

    print(f"Текст: {message_}")
    print(f"Шифрованный текст: {enc}")
    print(f"Расшифрованный текст: {dec}")

    print(f"Параметры: {parameters}")
