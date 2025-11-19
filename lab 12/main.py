import json
import os


class Student:
    def __init__(self, name, group, gpa):
        self.__name = name
        self.__group = group
        self.__gpa = gpa

    @property
    def name(self):
        return self.__name

    @property
    def group(self):
        return self.__group

    @property
    def gpa(self):
        return self.__gpa

    def display_info(self):
        print(f"Имя: {self.__name}, Группа: {self.__group}, GPA: {self.__gpa}")

    def update_gpa(self, new_gpa):
        if 0 <= new_gpa <= 5:
            self.__gpa = new_gpa
        else:
            print("Ошибка: GPA должен быть 0–5")

    def to_dict(self):
        return {
            "name": self.__name,
            "group": self.__group,
            "gpa": self.__gpa
        }


class Group:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Студент {student.name} добавлен.")

    def remove_student(self, name):
        for s in self.students:
            if s.name == name:
                self.students.remove(s)
                print(f"Студент {name} удалён.")
                return
        print("Студент не найден.")

    def show_all(self):
        if not self.students:
            print("Список пуст.")
        else:
            print("\n=== Все студенты ===")
            for s in self.students:
                s.display_info()

    def get_top_students(self, threshold):
        print(f"\n=== Студенты с GPA > {threshold} ===")
        top = [s for s in self.students if s.gpa > threshold]
        if not top:
            print("Нет таких студентов.")
        else:
            for s in top:
                s.display_info()

    def save_to_file(self, filename="students.json"):
        data = [s.to_dict() for s in self.students]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные сохранены.")

    def load_from_file(self, filename="students.json"):
        if not os.path.exists(filename):
            print("Файла нет — нечего загружать.")
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.students = [Student(d["name"], d["group"], d["gpa"]) for d in data]
        print("Данные загружены из файла.")


# -------------------------
#             М Е Н Ю
# -------------------------
def show_menu():
    print("\n===== МЕНЮ СИСТЕМЫ УЧЁТА СТУДЕНТОВ =====")
    print("1. Добавить студента")
    print("2. Удалить студента")
    print("3. Показать всех студентов")
    print("4. Показать лучших студентов (GPA > порога)")
    print("5. Сохранить в файл")
    print("6. Загрузить из файла")
    print("0. Выход")
    print("========================================")


if __name__ == "__main__":
    group = Group()

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ")

        if choice == "1":
            name = input("Имя: ")
            group_name = input("Группа: ")
            gpa = float(input("GPA (0-5): "))

            student = Student(name, group_name, gpa)
            group.add_student(student)

        elif choice == "2":
            name = input("Введите имя студента для удаления: ")
            group.remove_student(name)

        elif choice == "3":
            group.show_all()

        elif choice == "4":
            threshold = float(input("Введите порог GPA: "))
            group.get_top_students(threshold)

        elif choice == "5":
            group.save_to_file()

        elif choice == "6":
            group.load_from_file()

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Неверный пункт! Попробуйте снова.")
