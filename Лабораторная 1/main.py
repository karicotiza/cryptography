from random import sample
from collections import Counter


class Encryptor:
    def __init__(self, text: str) -> None:
        self.text = text
        self.BITS = 17
        self.frequency = Counter()
        self.key: dict = self.__make_key()

    def __make_key(self) -> dict:
        encryption_key = dict()

        text = [letter for letter in self.text.lower() if letter]
        text = "".join(text)

        counted_letters = Counter(text)
        text_length = len(text)

        frequency = {}

        for key, value in counted_letters.items():
            frequency[key] = counted_letters[key] / (text_length / 100)

        self.frequency = dict((k,round(v, 2)) for k,v in frequency.items())

        size = {
            2: "",
            3: "",
            4: "",
            5: "",
        }

        for key, value in frequency.items():
            if value >= 5:
                size[5] += key
            elif value >= 2:
                size[4] += key
            elif value >= 1:
                size[3] += key
            else:
                size[2] += key

        for key, value in size.items():
            numbers = sample(
                range(
                    10 ** (key - 1),
                    10 ** key - 1
                ),
                len(value) * key
            )

            for index in range(len(value)):
                memory = []
                for _ in range(key):
                    memory.append(numbers[0])
                    numbers.pop(0)
                encryption_key[value[index]] = memory

        return encryption_key

    def encrypt(self, text: str) -> str:
        text = [letter for letter in text.lower() if letter]

        ciphertext = ""
        used_letters = {}
        for letter in text:
            if (letter not in used_letters) or (used_letters[letter] == len(self.key[letter]) - 1):
                used_letters[letter] = 0
            else:
                used_letters[letter] += 1

            ciphertext += self.__add_the_non_significant_zeros(
                self.key[letter][used_letters[letter]]
            )

        return ciphertext

    def __add_the_non_significant_zeros(self, value: int) -> str:
        substitution = str(value)
        substitution = "0" * (self.BITS - len(bin(int(substitution))) + 2) + str(bin(int(substitution)))[2:]
        return substitution

    def save_key(self, path: str) -> None:
        self.__save_file(path, self.key)

    def save_frequency(self, path: str) -> None:
        self.__save_file(path, self.frequency)

    @staticmethod
    def __save_file(path: str, dictionary: dict) -> None:
        with open(path, "w", encoding="utf-8") as file:
            for key, value in dictionary.items():
                file.write(
                    f"{key}: {value}\n"
                )

    def __str__(self):
        return self.encrypt(self.text)


class Decryptor:
    def __init__(self, path_to_key: str) -> None:
        self.BITS = 17
        self.key: dict = self.__load_key(path_to_key)

    @staticmethod
    def __load_key(path_to_key: str) -> dict:
        decryption_key = dict()
        with open(path_to_key, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line[:-1].split(": ")
                decryption_key[key] = eval(value)

        return decryption_key

    def decrypt(self, text: str, ) -> str:
        text = [text[index - self.BITS: index] for index in range(self.BITS, len(text) + 1, self.BITS)]
        text = [int(section, 2) for section in text]

        decrypted_text = ""
        for section in text:
            for key, value in self.key.items():
                if section in value:
                    decrypted_text += key

        return decrypted_text


if __name__ == "__main__":
    while True:
        user_input = str(input("Текст для шифрования: "))
        encryptor = Encryptor(user_input)

        encryptor.save_key("key.txt")
        encryptor.save_frequency("frequency.txt")

        decryptor = Decryptor("key.txt")
        decrypted_text = decryptor.decrypt(str(encryptor))

        print("Текст в зашифрованном виде: ", encryptor, "\n")
        print("Расшифрованный шифротекст: ", decrypted_text, "\n")
