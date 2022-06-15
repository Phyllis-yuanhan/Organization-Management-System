import unittest
from organization_hierarchy import *
from a2_test import employee_eq
class TestLeader(unittest.TestCase):
    def setUp(self) -> None:
        def assertFun(employee, data, isLeader):
            err_format = "The expected {} is {} your result is {}".format
            eid, name, position, salary, rating, department = data[0], data[1], data[2], data[3],data[4], data[5]
            self.assertEqual(eid, employee.eid, err_format("eid", eid, employee.eid))
            self.assertEqual(name, employee.name, err_format("name", name, employee.name))
            self.assertEqual(position, employee.position, err_format("position", position, employee.position))
            self.assertEqual(rating, employee.rating, err_format("rating", rating, employee.rating))
            self.assertEqual(department, employee.get_department_name(), err_format("department", department, employee.get_department_name()))
            self.assertEqual(isLeader, isinstance(employee, Leader), err_format("isLeader", isLeader, isinstance(employee, Leader)))
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.assertFun = assertFun

    def tearDown(self) -> None:
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def test_init(self):
        self.assertFun(self.e1, [1, "A", "PositionA", 100, 10, "CS"], True)

    def test_department_name(self):
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        self.assertFun(self.e3, [3, "C", "PositionC", 100, 30, "Math"], False)
        self.assertFun(self.e2, [2, "B", "PositionB", 100, 20, "Math"], True)

    def test_department_name2(self):
        self.e2 = Leader(2, "B", "PositionB", 100, 20, "Math")
        self.e3 = Leader(3, "C", "PositionC", 100, 30, "Econ")
        self.e4.become_subordinate(self.e2)
        self.e5.become_subordinate(self.e3)
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.assertFun(self.e1, [1, "A", "PositionA", 100, 10, "CS"], True)
        self.assertFun(self.e2, [2, "B", "PositionB", 100, 20, "Math"], True)
        self.assertFun(self.e3, [3, "C", "PositionC", 100, 30, "Econ"], True)
        self.assertFun(self.e4, [4, "D", "PositionD", 100, 40, "Math"], False)
        self.assertFun(self.e5, [5, "E", "PositionE", 100, 50, "Econ"], False)

    def test_get_employee(self):
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3.become_subordinate(self.e2)
        self.e4.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        e2_emps = self.e2.get_department_employees()
        e2_emps.sort(key=lambda x: x.eid)
        self.assertTrue(len(e2_emps) == 3)
        self.assertFun(e2_emps[0], [2, "B", "PositionB", 100, 20, "Math"], True)
        self.assertFun(e2_emps[1], [3, "C", "PositionC", 100, 30, "Math"], False)
        self.assertFun(e2_emps[2], [4, "D", "PositionD", 100, 40, "Math"], False)

    def test_hierarchy(self):
        temp = self.e1.get_position_in_hierarchy()
        self.assertEqual(temp, "PositionA, CS")
        self.assertEqual(self.e3.get_position_in_hierarchy(), "PositionC")

    def test_hierarchy2(self):
        e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        self.assertEqual('Worker', e1.get_position_in_hierarchy())
        e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        e3 = Leader(3, "Temp", "Head", 20000, 30, "HeadDepartment")
        e4 = Leader(4, "Bigg Boss", "CEO", 50000, 60, "Company")
        e1.become_subordinate(e2)
        e2.become_subordinate(e3)
        e3.become_subordinate(e4)
        self.assertEqual('Worker, Department, HeadDepartment, Company', e1.get_position_in_hierarchy())
        self.assertEqual('Manager, Department, HeadDepartment, Company', e2.get_position_in_hierarchy())
        self.assertEqual('Head, HeadDepartment, Company', e3.get_position_in_hierarchy())
        self.assertEqual('CEO, Company', e4.get_position_in_hierarchy())

    def test_hierarchy3(self):
        e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        e3 = Leader(3, "Temp", "Head", 20000, 30, "HeadDepartment")
        e4 = Leader(4, "Bigg Boss", "CEO", 50000, 60, "Company")
        e3.become_subordinate(e4)
        e1.become_subordinate(e3)
        e2.become_subordinate(e4)
        self.assertEqual('Worker, HeadDepartment, Company', e1.get_position_in_hierarchy())
        self.assertEqual('Manager, Department, Company', e2.get_position_in_hierarchy())
        self.assertEqual('Head, HeadDepartment, Company', e3.get_position_in_hierarchy())
        self.assertEqual('CEO, Company', e4.get_position_in_hierarchy())

if __name__ == '__main__':
    unittest.main()
