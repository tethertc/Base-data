from .person import Person

class AdminStaff(Person):
    def __init__(self, name: str, age: int, position: str, department: str):
        super().__init__(name, age)
        self.position = position
        self.department = department

    def display_info(self):
        return (f"Admin Staff — Name: {self.name}, Age: {self.age}, "
                f"Position: {self.position}, Department: {self.department}")
