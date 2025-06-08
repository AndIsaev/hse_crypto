import hashlib
import random
from typing import Tuple

# Параметры эллиптической кривой для ГОСТ Р 34.10-2012 (256-битный вариант)
# Пример параметров (должны быть заменены на стандартные)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97
A = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94
B = 0x00000000000000000000000000000000000000000000000000000000000000A6
Q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893
X = 0x0000000000000000000000000000000000000000000000000000000000000001
Y = 0x8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14


class GOST34102012:
    def __init__(self):
        """Инициализация с параметрами эллиптической кривой"""
        self.p = P  # модуль поля
        self.a = A  # коэффициент a уравнения кривой
        self.b = B  # коэффициент b уравнения кривой
        self.q = Q  # порядок базовой точки
        self.x = X  # x-координата базовой точки
        self.y = Y  # y-координата базовой точки

    def generate_key_pair(self) -> Tuple[int, Tuple[int, int]]:
        """Генерация пары ключей (private, public)"""
        private_key = random.randint(1, self.q - 1)
        public_key = self.scalar_multiply(private_key, (self.x, self.y))
        return private_key, public_key

    def sign(self, message: bytes, private_key: int) -> tuple[int, int] | None:
        """Создание ЭЦП для сообщения"""
        # Шаг 1 - вычисление хэша сообщения
        e = self.hash_message(message)
        e = int.from_bytes(e, byteorder='big') % self.q
        if e == 0:
            e = 1

        while True:
            # Шаг 2 - генерация случайного числа k
            k = random.randint(1, self.q - 1)

            # Шаг 3 - вычисление точки кривой C = k*G
            c_x, _ = self.scalar_multiply(k, (self.x, self.y))

            # Шаг 4 - вычисление r = x_C mod q
            r = c_x % self.q
            if r == 0:
                continue

            # Шаг 5 - вычисление s = (r*d + k*e) mod q
            s = (r * private_key + k * e) % self.q
            if s == 0:
                continue

            return r, s

    def verify(self, message: bytes, signature: Tuple[int, int], public_key: Tuple[int, int]) -> bool:
        """Проверка ЭЦП"""
        r, s = signature

        # Шаг 1 - проверка условий 0 < r < q и 0 < s < q
        if not (0 < r < self.q and 0 < s < self.q):
            return False

        # Шаг 2 - вычисление хэша сообщения
        e = self.hash_message(message)
        e = int.from_bytes(e, byteorder='big') % self.q
        if e == 0:
            e = 1

        # Шаг 3 - вычисление v = e^(-1) mod q
        try:
            v = pow(e, -1, self.q)
        except ValueError:
            return False

        # Шаг 4 - вычисление z1 = s*v mod q, z2 = -r*v mod q
        z1 = (s * v) % self.q
        z2 = (-r * v) % self.q

        # Шаг 5 - вычисление точки C = z1*G + z2*Q
        point_g = self.scalar_multiply(z1, (self.x, self.y))
        point_q = self.scalar_multiply(z2, public_key)
        c_x, _ = self.point_add(point_g, point_q)

        # Шаг 6 - проверка равенства r = x_C mod q
        R = c_x % self.q
        return R == r

    def hash_message(self, message: bytes) -> bytes:
        """Вычисление хэша сообщения по ГОСТ Р 34.11-2012"""
        # В реальной реализации здесь должна быть функция из ГОСТ Р 34.11-2012
        # Для примера используем SHA-256
        h = hashlib.sha256(message).digest()
        return h[:32]  # Для 256-битной версии берем 32 байта

    def point_add(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int]:
        """Сложение двух точек на эллиптической кривой"""
        if p1 == (0, 0):
            return p2
        if p2 == (0, 0):
            return p1

        x1, y1 = p1
        x2, y2 = p2

        if x1 == x2 and y1 == y2:
            # Удвоение точки
            lam = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p)
        else:
            # Сложение разных точек
            lam = (y2 - y1) * pow(x2 - x1, -1, self.p)

        lam %= self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p

        return x3, y3

    def scalar_multiply(self, k: int, point: Tuple[int, int]) -> Tuple[int, int]:
        """Умножение точки на скаляр (алгоритм удвоения-сложения)"""
        result = (0, 0)  # Нейтральный элемент
        current = point

        while k > 0:
            if k % 2 == 1:
                result = self.point_add(result, current)
            current = self.point_add(current, current)
            k = k // 2

        return result


def save_key_to_file(filename: str, key) -> None:
    """Сохранение ключа в файл"""
    if isinstance(key, tuple):  # публичный ключ
        with open(filename, 'w') as f:
            f.write(f"{hex(key[0])} {hex(key[1])}")
    else:  # приватный ключ
        with open(filename, 'w') as f:
            f.write(hex(key))


def load_key_from_file(filename: str, is_public: bool = False):
    """Загрузка ключа из файла"""
    with open(filename, 'r') as f:
        content = f.read().strip()

    if is_public:
        x_hex, y_hex = content.split()
        return (int(x_hex, 16), int(y_hex, 16))
    else:
        return int(content, 16)


def save_signature_to_file(filename: str, signature: Tuple[int, int]) -> None:
    """Сохранение подписи в файл"""
    with open(filename, 'w') as f:
        f.write(f"{hex(signature[0])} {hex(signature[1])}")


def load_signature_from_file(filename: str) -> Tuple[int, int]:
    """Загрузка подписи из файла"""
    with open(filename, 'r') as f:
        r_hex, s_hex = f.read().strip().split()
    return (int(r_hex, 16), int(s_hex, 16))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='ГОСТ Р 34.10-2012 - Реализация электронной цифровой подписи'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Парсер для генерации ключей
    gen_parser = subparsers.add_parser('generate', help='Генерация ключевой пары')
    gen_parser.add_argument('--private', required=True, help='Файл для сохранения приватного ключа')
    gen_parser.add_argument('--public', required=True, help='Файл для сохранения публичного ключа')

    # Парсер для создания подписи
    sign_parser = subparsers.add_parser('sign', help='Создание подписи')
    sign_parser.add_argument('--file', required=True, help='Файл для подписи')
    sign_parser.add_argument('--private', required=True, help='Файл с приватным ключом')
    sign_parser.add_argument('--output', required=True, help='Файл для сохранения подписи')

    # Парсер для проверки подписи
    verify_parser = subparsers.add_parser('verify', help='Проверка подписи')
    verify_parser.add_argument('--file', required=True, help='Файл для проверки')
    verify_parser.add_argument('--signature', required=True, help='Файл с подписью')
    verify_parser.add_argument('--public', required=True, help='Файл с публичным ключом')

    args = parser.parse_args()
    gost = GOST34102012()

    if args.command == 'generate':
        # Генерация ключевой пары
        private_key, public_key = gost.generate_key_pair()
        save_key_to_file(args.private, private_key)
        save_key_to_file(args.public, public_key)
        print(f"Ключевая пара сгенерирована и сохранена в {args.private} и {args.public}")

    elif args.command == 'sign':
        # Создание подписи
        with open(args.file, 'rb') as f:
            message = f.read()

        private_key = load_key_from_file(args.private)
        signature = gost.sign(message, private_key)
        save_signature_to_file(args.output, signature)
        print(f"Подпись создана и сохранена в {args.output}")

    elif args.command == 'verify':
        # Проверка подписи
        with open(args.file, 'rb') as f:
            message = f.read()

        signature = load_signature_from_file(args.signature)
        public_key = load_key_from_file(args.public, is_public=True)

        if gost.verify(message, signature, public_key):
            print("Подпись ВЕРНА")
        else:
            print("Подпись НЕВЕРНА")


if __name__ == '__main__':
    main()