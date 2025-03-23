import string

# Русская версия алфавита
russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Латинская версия алфавита
latin_alphabet = string.ascii_lowercase


# Дополнительные функции для определения используемого алфавита
def determine_alphabet(text):
    if any(c.isalpha() and c.lower() in latin_alphabet for c in text):
        return latin_alphabet
    elif any(c.isalpha() and c.lower() in russian_alphabet for c in text):
        return russian_alphabet
    else:
        raise ValueError("Текст содержит недопустимые символы.")


# Основные функции остаются прежними
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    t, new_t = 0, 1
    r, new_r = m, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        raise ValueError("Обратного элемента не существует!")
    if t < 0:
        t += m
    return t


def encrypt_affine(text, a, b, alphabet):
    cipher_text = []
    for char in text:
        if char.isalpha():
            index = alphabet.index(char.lower())  # Преобразуем все буквы в нижний регистр
            encrypted_index = (a * index + b) % len(alphabet)
            cipher_char = alphabet[encrypted_index]
            cipher_text.append(cipher_char.upper() if char.isupper() else cipher_char)
        else:
            cipher_text.append(char)  # Оставляем другие символы без изменений
    return ''.join(cipher_text)


def decrypt_affine(cipher_text, a, b, alphabet):
    decrypted_text = []
    inverse_a = mod_inverse(a, len(alphabet))
    for char in cipher_text:
        if char.isalpha():
            index = alphabet.index(char.lower())
            decrypted_index = inverse_a * (index - b) % len(alphabet)
            decrypted_char = alphabet[decrypted_index]
            decrypted_text.append(decrypted_char.upper() if char.isupper() else decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


# Функция для получения параметров от пользователя
def get_parameters():
    print("Выберите режим:")
    print("1. Шифрование")
    print("2. Дешифровка")
    mode = int(input("Ваш выбор: "))

    print("\nВведите открытый текст или шифртекст:")
    text = input().strip()

    print("\nВведите коэффициент a (должен быть взаимно простым с длиной алфавита):")
    a = int(input())

    print("\nВведите смещение b:")
    b = int(input())

    return mode, text, a, b


def main():
    try:
        mode, text, a, b = get_parameters()

        # Определяем алфавит в зависимости от введённого текста
        alphabet = determine_alphabet(text)

        if mode == 1:
            # Шифрование
            cipher_text = encrypt_affine(text, a, b, alphabet)
            print(f"\nЗашифрованный текст: {cipher_text}")
        elif mode == 2:
            # Дешифрование
            decrypted_text = decrypt_affine(text, a, b, alphabet)
            print(f"\nРасшифрованный текст: {decrypted_text}")
        else:
            print("Неверный выбор режима.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")



# Основная программа
if __name__ == "__main__":
    main()
