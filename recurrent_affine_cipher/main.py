def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Обратного элемента не существует")

def affine_recurrent_cipher(text, a, b, m, encrypt=True):
    if encrypt:
        # Шифрование
        def transform(i, char):
            return (a * ord(char) + b) % m
    else:
        # Расшифрование
        a_inv = mod_inverse(a, m)
        def transform(i, char):
            return (a_inv * (ord(char) - b)) % m

    result = []
    for i, char in enumerate(text):
        if char.isprintable() and not char.isspace():
            transformed = transform(i, char)
            result.append(chr(transformed))
        else:
            result.append(char)  # оставляем непринтируемые символы неизменными

    return ''.join(result)

def main():
    action = input("Введите 'e' для шифрования или 'd' для расшифрования: ").lower()
    text = input("Введите текст: ")
    try:
        a = int(input("Введите значение a: "))
        b = int(input("Введите значение b: "))
    except ValueError:
        print("Ключи должны быть числами.")
        return

    m = 256  # Используем 256 для поддержки всех символов ASCII

    if gcd(a, m) != 1:
        print(f"The value 'a' must be coprime with {m}.")
        return

    encrypt = action == 'e'
    result = affine_recurrent_cipher(text, a, b, m, encrypt)
    print("Результат:", result)

if __name__ == "__main__":
    main()
