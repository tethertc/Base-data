import unittest
from people.student import Student
from people.teacher import Teacher
from people.admin_staff import AdminStaff

class TestPeople(unittest.TestCase):

    def test_student(self):
        s = Student("Aidar", 19, "CS-23", 3.5)
        self.assertIn("Aidar", s.display_info())
        self.assertIn("CS-23", s.display_info())

    def test_teacher(self):
        t = Teacher("Marat", 45, "Math", 20)
        self.assertIn("Math", t.display_info())
        self.assertIn("20", t.display_info())

    def test_admin_staff(self):
        a = AdminStaff("Dana", 33, "Secretary", "Office 1")
        self.assertIn("Secretary", a.display_info())
        self.assertIn("Office 1", a.display_info())

if __name__ == "__main__":
    unittest.main()
