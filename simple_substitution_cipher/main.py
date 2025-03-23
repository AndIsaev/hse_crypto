import string


def encrypt(text: str, shift: int) -> str:
    encrypted_text = ""
    len_alpha = len(string.ascii_lowercase)

    for char in text:
        if char.isalpha():
            # Если символ является буквой, выполняем замену
            is_upper = char.isupper()  # Проверяем регистр буквы
            base_char = 'A' if is_upper else 'a'
            position = ord(char) - ord(base_char)
            new_position = (position + shift) % len_alpha
            new_char = chr(new_position + ord(base_char))
            encrypted_text += new_char
        else:
            # Для остальных символов оставляем их без изменений
            encrypted_text += char

    return encrypted_text


def decrypt(ciphertext: str, shift: int) -> str:
    decrypted_text = ""

    for char in ciphertext:
        if char.isalpha():
            # Проверяем регистр буквы
            is_upper = char.isupper()
            base_char = 'A' if is_upper else 'a'

            # Определяем позицию символа относительно начала алфавита
            position = ord(char) - ord(base_char)

            # Вычитаем смещение и приводим результат обратно к диапазону 0–25
            new_position = (position - shift) % 26

            # Преобразуем новую позицию обратно в символ
            new_char = chr(new_position + ord(base_char))
            decrypted_text += new_char
        else:
            # Оставляем остальные символы без изменений
            decrypted_text += char

    return decrypted_text


if __name__ == "__main__":
    # todo: раскомментируйте при необходимости быстрой проверки
    # shift_amount = 3  # Сдвиг на 3 позиции вперед
    # message = "Hello World!"
    # encrypted_message = encrypt(message, shift_amount)
    # print("Исходное сообщение:", message)
    # print("Зашифрованное сообщение:", encrypted_message)
    #
    # decrypted_text = decrypt(encrypted_message, shift_amount)
    # print("Расшифрованное сообщение", decrypted_text)  # Выведет: "Hello World!"

    shift_amount = int(input("Введите ключ: "))
    print("Введен ключ: ", shift_amount)
    message = input("Введите введите текст для шифрования: ")
    print("Введен текст: ", message)
    encrypted_message = encrypt(message, shift_amount)
    print("Результат шифрования: ", encrypted_message)
    decrypted_text = decrypt(encrypted_message, shift_amount)
    print("Расшифрованное сообщение", decrypted_text)
