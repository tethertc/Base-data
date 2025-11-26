from .person import Person

class Student(Person):
    def __init__(self, name: str, age: int, group: str, gpa: float):
        super().__init__(name, age)
        self.group = group
        self.gpa = gpa

    def display_info(self):
        return (f"Student — Name: {self.name}, Age: {self.age}, "
                f"Group: {self.group}, GPA: {self.gpa}")
