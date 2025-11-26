from .person import Person

class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str, experience: int):
        super().__init__(name, age)
        self.subject = subject
        self.experience = experience

    def display_info(self):
        return (f"Teacher — Name: {self.name}, Age: {self.age}, "
                f"Subject: {self.subject}, Experience: {self.experience} years")
