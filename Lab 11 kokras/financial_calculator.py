import math
import logging

logging.basicConfig(filename="errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
        P = float(input("Введите сумму вклада (P): "))
        r = float(input("Введите годовую процентную ставку (в %, например 10): ")) / 100
        t = float(input("Введите срок вклада (в годах): "))
        n = 12

        if P <= 0 or r <= 0 or t <= 0:
            raise ValueError("Все значения должны быть положительными!")

        S = P * math.pow((1 + r / n), n * t)

        print(f"\nИтоговая сумма через {t} лет составит: {S:.2f} руб.\n")

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"Начальная сумма: {P}\n")
            f.write(f"Годовая ставка: {r * 100}%\n")
            f.write(f"Срок вклада: {t} лет\n")
            f.write(f"Количество начислений в год: {n}\n")
            f.write(f"Итоговая сумма: {S:.2f} руб.\n")

        print("Результаты сохранены в файл result.txt")

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
        logging.error(f"Ошибка ввода: {ve}")
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
        logging.error("Ошибка деления на ноль")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        logging.error(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
