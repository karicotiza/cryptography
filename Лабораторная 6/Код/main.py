import datetime
from collections import Counter


class ElGamal:
    @staticmethod
    def decrypt(
            encrypted_message: int,
            o_secret: int,
            y: int,
            p: int,
            g: int,
            x: int,
    ) -> int:
        k = pow(o_secret, x, p)
        k_1 = pow(k, -1, p)
        c = encrypted_message * k_1
        return c


class CRT:
    @staticmethod
    def division(
            number: int,
            p: int,
            q: int,
            e: int,
    ):
        return CRT.chinese_remainder_theorem(
            q,
            pow(number % q, e, q),
            p,
            pow(number % p, e, p),
        )

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
    def euler_function(value: int) -> int:
        primes = CRT.canonical_decomposition(value).keys()
        multiplier = 1

        for element in primes:
            multiplier *= 1 - 1 / element

        return int(value * multiplier)

    @staticmethod
    def extended_euclid(a: int, b: int) -> tuple[int, int]:
        if b == 0:
            return (1, 0)
        (x, y) = CRT.extended_euclid(b, a % b)
        k = a // b
        return (y, x - k * y)

    @staticmethod
    def chinese_remainder_theorem(n1: int, r1: int, n2: int, r2: int) -> int:
        (x, y) = CRT.extended_euclid(n1, n2)
        m = n1 * n2
        n = r2 * x * n1 + r1 * y * n2
        return (n % m + m) % m


if __name__ == "__main__":
    encrypted_message = 160_936_054
    o_secret = 144_946_434
    y = 57_348_448
    p = 206_181_067
    g = 7
    x = 1

    print("Расшифрованное сообщение:", ElGamal.decrypt(encrypted_message, o_secret, y, p, g, x))

    #####

    number = 2_428_010_006_080_722_311 ** 50
    p = 2_038_074_743 ** 50
    q = 2_038_074_751 ** 50
    e = 1_299_709 ** 50

    import datetime
    date0 = datetime.datetime.now()
    print("Деление по модулю:", CRT.division(number, p, q, e))
    date1 = datetime.datetime.now()
    print(pow(number, e, (p * q)))
    date2 = datetime.datetime.now()

    print(date1 - date0)
    print(date2 - date1)