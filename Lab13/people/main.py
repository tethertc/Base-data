from people.student import Student
from people.teacher import Teacher
from people.admin_staff import AdminStaff

def main():
    people = [
        Student("Aidar", 19, "CS-23", 3.7),
        Teacher("Marat", 45, "Math", 20),
        AdminStaff("Dana", 33, "Secretary", "Office 1")
    ]

    print("=== Полиморфизм в действии ===")
    for person in people:
        print(person.display_info())

if __name__ == "__main__":
    main()
