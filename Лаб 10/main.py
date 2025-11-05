import json

# --- Ввод данных пользователем ---
employees = []
n = int(input("Введите количество работников Сбербанка: "))

for i in range(n):
    name = input(f"Имя работника {i + 1}: ")
    position = input("Должность: ")
    salary = float(input("Средняя зарплата (в рублях): "))
    employees.append({"name": name, "position": position, "salary": salary})

# --- Сохранение в текстовый файл ---
with open("employees.txt", "w", encoding="utf-8") as f:
    for e in employees:
        f.write(f"{e['name']} | {e['position']} | {e['salary']}\n")

# --- Чтение из файла ---
print("\nДанные из файла employees.txt:")
with open("employees.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# --- Сериализация в JSON ---
with open("employees.json", "w", encoding="utf-8") as jf:
    json.dump(employees, jf, ensure_ascii=False, indent=4)

# --- Фильтрация по зарплате ---
threshold = float(input("\nВведите минимальную зарплату для фильтрации: "))
filtered = [e for e in employees if e["salary"] >= threshold]

print("\nРаботники с зарплатой выше порога:")
for e in filtered:
    print(f"{e['name']} ({e['position']}) - Зарплата: {e['salary']} руб.")
