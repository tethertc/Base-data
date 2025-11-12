def divide_numbers():
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))
        result = a / b
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
    except ValueError:
        print("Ошибка: введено не число!")
    else:
        print(f"Результат деления: {result}")
    finally:
        print("Работа программы завершена.")


if __name__ == "__main__":
    divide_numbers()
