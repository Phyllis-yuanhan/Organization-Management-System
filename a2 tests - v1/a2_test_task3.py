import unittest
from a2_test import employee_eq
from organization_hierarchy import *


class TestBecomeLeader(unittest.TestCase):
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
        self.assertFun = assertFun
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def test_simple(self):
        leader = self.e1.become_leader("CS")
        self.assertFun(leader, [1, "A", "PositionA", 100, 10, "CS"], True)
        self.assertTrue(employee_eq(leader, self.e1))

    def test_simple2(self):
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        leader = self.e1.become_leader("HR")
        self.assertFun(leader, [1, "A", "PositionA", 100, 10, "HR"], True)

    def test_simple3(self):
        self.e2.become_subordinate(self.e1)
        leader = self.e1.become_leader("CS")
        self.assertFun(leader, [1, "A", "PositionA", 100, 10, "CS"], True)
        children = leader.get_direct_subordinates()
        self.assertTrue(len(children) == 1, "You should maintain the original structure")
        self.assertFun(children[0], [2, "B", "PositionB", 200, 20, "CS"], False)

    def test_simple4(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        leader = self.e2.become_leader("CS")
        self.assertFun(leader, [2, "B", "PositionB", 200, 20, "CS"], True)
        children = leader.get_direct_subordinates()
        self.assertTrue(len(children) == 1)
        self.assertFun(children[0], [3, "C", "PositionC", 300, 30, "CS"], False)
        self.assertFun(leader.get_superior(), [1, "A", "PositionA", 100, 10, ""], False)
        self.assertTrue(employee_eq(self.e1.get_direct_subordinates()[0], leader))

    def test_complex(self):
        """
        Before:
             e1(1, "A", "PositionA", 100, "CS")
            /  |
           e2 e3(3, "C", "PositionC", 300, "Math")
           |   |
           e4  e5
        After:
             e1(1, "A", "PositionA", 100, "CS")
            /  |
           e2 e3(3, "C", "PositionC", 300, "HR")
           |   |
           e4  e5
        """
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e3 = Leader(3, "C", "PositionC", 300, 30, "Math")
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e2)
        self.e5.become_subordinate(self.e3)
        leader = self.e3.become_leader("HR")
        self.assertFun(leader, [3, "C", "PositionC", 300, 30, "HR"], True)
        self.assertFun(leader.get_superior(), [1, "A", "PositionA", 100, 10, "CS"], True)
        child = leader.get_direct_subordinates()
        self.assertTrue(len(child), 1)
        self.assertFun(child[0], [5, "E", "PositionE", 500, 50, "HR"], False)
        head = leader.get_organization_head()
        left_root = head.get_direct_subordinates()[0]
        self.assertFun(left_root, [2, "B", "PositionB", 200, 20, "CS"], False)
        self.assertFun(left_root.get_direct_subordinates()[0], [4, "D", "PositionD", 400, 40, "CS"], False)

    def test_complex2(self):
        """
        Before:
             e1(1, "A", "PositionA", 100, "CS")
            /  |
           e2(2, "B", "PositionB", 200, "Math") e3
           |   |
           e4  e5
        After:
             e1(1, "A", "PositionA", 100, "CS")
            /  |
           e2(2, "B", "PositionB", 200, "Math") e3
           |                                    |
           e4(4, "D", "PositionD", 400, "HR")  e5
        """
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e2)
        self.e5.become_subordinate(self.e3)
        leader = self.e4.become_leader("HR")
        self.assertFun(leader, [4, "D", "PositionD", 400, 40, "HR"], True)
        self.assertFun(leader.get_superior(), [2, "B", "PositionB", 200, 20, "Math"], True)
        child = leader.get_direct_subordinates()
        self.assertTrue(len(child) == 0)
        head = leader.get_organization_head()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)
        right_root = head.get_direct_subordinates()[1]
        self.assertFun(right_root, [3, "C", "PositionC", 300, 30, "CS"], False)
        self.assertFun(right_root.get_direct_subordinates()[0], [5, "E", "PositionE", 500, 50, "CS"], False)


class TestBecomeEmployee(unittest.TestCase):
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
        self.assertFun = assertFun
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def tearDown(self) -> None:
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def test_simple(self):
        employee = self.e1.become_employee()
        self.assertFun(employee, [1, "A", "PositionA", 100, 10, ""], False)
        self.assertTrue(employee_eq(employee, self.e1))

    def test_simple2(self):
        self.e2.become_subordinate(self.e1)
        employee = self.e1.become_employee()
        self.assertFun(employee, [1, "A", "PositionA", 100, 10, ""], False)
        self.assertFun(employee.get_direct_subordinates()[0], [2, "B", "PositionB", 200, 20, ""], False)

    def test_linear(self):
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        employee = self.e2.become_employee()
        self.assertFun(employee, [2, "B", "PositionB", 200, 20, "CS"], False)
        self.assertFun(employee.get_direct_subordinates()[0], [3, "C", "PositionC", 300, 30, "CS"], False)
        self.assertFun(employee.get_superior(), [1, "A", "PositionA", 100, 10, "CS"], True)
        head = employee.get_organization_head()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)

    def test_complex(self):
        """
        Before:
        e1(1, "A", "PositionA", 100, 10, "CS")
        |
        e2(2, "B", "PositionB", 200, 20, "Math")
        |
        e3(3, "C", "PositionC", 300, 30, "Econ")
        /|
        e4(4, "D", "PositionD", 400, 40, "HR") e5(5, "E", "PositionE", 500, 50, "Design")
        After:
        e1(1, "A", "PositionA", 100, 10, "CS")
        |
        e2(2, "B", "PositionB", 200, 20, "Math")
        |
        e3(3, "C", "PositionC", 300, 30)
        /|
        e4(4, "D", "PositionD", 400, 40, "HR") e5(5, "E", "PositionE", 500, 50, "Design")
        """
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3 = Leader(3, "C", "PositionC", 300, 30, "Econ")
        self.e4 = Leader(4, "D", "PositionD", 400, 40, "HR")
        self.e5 = Leader(5, "E", "PositionE", 500, 50, "Design")
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        employee = self.e3.become_employee()
        self.assertFun(employee, [3, "C", "PositionC", 300, 30, "Math"], False)
        child = employee.get_direct_subordinates()
        self.assertTrue(len(child) == 2)
        e4 = child[0]
        self.assertFun(e4, [4, "D", "PositionD", 400, 40, "HR"], True)
        e5 = child[1]
        self.assertFun(e5, [5, "E", "PositionE", 500, 50, "Design"], True)
        superior = employee.get_superior()
        self.assertFun(superior, [2, "B", "PositionB", 200, 20, "Math"], True)
        head = employee.get_organization_head()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)


class TestChangeLeader(unittest.TestCase):
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
        self.assertFun = assertFun
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def tearDown(self) -> None:
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)

    def test_simple(self):
        head = self.e1.change_department_leader()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)

    def test_simple2(self):
        """
        Before:
        e1(1, A, PositionA, 100, 10, "CS")
        |
        e2(2, B, PositionB, 200, 20)
        After:
        e2(2, B, PositionB, 200, 20, "CS")
        |
        e1(1, A, PositionA, 100, 10)
        """
        self.e2.become_subordinate(self.e1)
        head = self.e2.change_department_leader()
        self.assertFun(head, [2, "B", "PositionB", 200, 20, "CS"], True)
        child = head.get_direct_subordinates()
        self.assertTrue(len(child) == 1)
        self.assertFun(child[0], [1, "A", "PositionA", 100, 10, "CS"], False)

    def test_linear(self):
        """
        Before:
        e1(1, A, PositionA, 100, 10, CS)
        |
        e2(2, B, PositionB, 200, 20, Math)
        |
        e3(3, C, PositionC, 300, 30)
        |
        e4(4, D, PositionD, 400, 40, HR)
        |
        e5(5, E, PositionE, 500, 50, Design)
        After:
        e1(1, A, PositionA, 100, 10, CS)
        |
        e3(3, C, PositionC, 300, 30, Math)
        /                               \
        e2(2, B, PositionB, 200, 20) e4(4, D, PositionD, 400, 40, HR)
                                    |
                                    e5(5, E, PositionE, 500, 50, Design)
        """
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e4 = Leader(4, "D", "PositionD", 400, 40, "HR")
        self.e5 = Leader(5, "E", "PositionE", 500, 50, "Design")
        self.e5.become_subordinate(self.e4)
        self.e4.become_subordinate(self.e3)
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        head = self.e3.change_department_leader()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)
        e3 = head.get_direct_subordinates()[0]
        self.assertFun(e3, [3, "C", "PositionC", 300, 30, "Math"], True)
        e3_child = e3.get_direct_subordinates()
        self.assertFun(e3_child[0], [2, "B", "PositionB", 200, 20, "Math"], False)
        self.assertFun(e3_child[1], [4, "D", "PositionD", 400, 40, "HR"], True)
        e5 = e3_child[1].get_direct_subordinates()[0]
        self.assertFun(e5, [5, "E", "PositionE", 500, 50, "Design"], True)

    def test_handout(self):
        """
        Before:
             e1(1, A, PositionA, 100, 10, CS)
            / \
           e2  e3
               /\
            e4  e5
        After:
            e3(3, C, PositionC, 300, 30, CS)
            /                           | \
           e1(1, A, PositionA, 100, 10) e4 e5
           |
           e2
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        head = self.e3.change_department_leader()
        self.assertFun(head, [3, "C", "PositionC", 300, 30, "CS"], True)
        self.assertIsNone(head.get_superior())
        children = head.get_direct_subordinates()
        self.assertTrue(len(children) == 3)
        e1 = children[0]
        e4 = children[1]
        e5 = children[2]
        self.assertFun(e4, [4, "D", "PositionD", 400, 40, "CS"], False)
        self.assertFun(e5, [5, "E", "PositionE", 500, 50, "CS"], False)
        self.assertFun(e1, [1, "A", "PositionA", 100, 10, "CS"], False)
        e2 = e1.get_direct_subordinates()[0]
        self.assertFun(e2, [2, "B", "PositionB", 200, 20, "CS"], False)

    def test_handout2(self):
        """
        Before:
             e1(1, A, PositionA, 100, 10, CS)
            / \
           e2  e3
               /\
            e4  e5
        After:
            e4(4, D, PositionD, 400, 40, CS)
            |
            e1
            /\
            e2 e3
                |
                e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        head = self.e4.change_department_leader()
        self.assertFun(head, [4, "D", "PositionD", 400, 40, "CS"], True)
        e1 = head.get_direct_subordinates()[0]
        self.assertFun(e1, [1, "A", "PositionA", 100, 10, "CS"], False)
        self.assertFun(e1.get_superior(), [4, "D", "PositionD", 400, 40, "CS"], True)
        e1_child = e1.get_direct_subordinates()
        self.assertTrue(len(e1_child) == 2)
        e2, e3 = e1_child[0], e1_child[1]
        self.assertFun(e2, [2, "B", "PositionB", 200, 20, "CS"], False)
        self.assertFun(e3, [3, "C", "PositionC", 300, 30, "CS"], False)
        self.assertFun(e2.get_superior(), [1, "A", "PositionA", 100, 10, "CS"], False)
        self.assertFun(e3.get_superior(), [1, "A", "PositionA", 100, 10, "CS"], False)
        e5 = e3.get_direct_subordinates()[0]
        self.assertFun(e5, [5, "E", "PositionE", 500, 50, "CS"], False)

    def test_complex(self):
        """
        Before:
            e1(1, A, PositionA, 100, 10, CS)
            /|
          e2 e3(3, C, PositionC, 300, 30, Econ)
             /|
            e4 e5
            /
            e6
        After:
            e1(1, A, PositionA, 100, 10, CS)
            /|
          e2 e6(6, F, PositionF, 600, 60, Econ)
             |
             e3
             /|
            e4 e5
        """
        self.e3 = Leader(3, "C", "PositionC", 300, 30, "Econ")
        e6 = Employee(6, "F", "PositionF", 600, 60)
        e6.become_subordinate(self.e4)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        self.e3.become_subordinate(self.e1)
        self.e2.become_subordinate(self.e1)
        head = e6.change_department_leader()
        self.assertFun(head, [1, "A", "PositionA", 100, 10, "CS"], True)
        e1_child = head.get_direct_subordinates()
        e2, new_e6 = e1_child[0], e1_child[1]
        self.assertFun(new_e6.get_superior(), [1, "A", "PositionA", 100, 10, "CS"], True)
        self.assertFun(e2, [2, "B", "PositionB", 200, 20, "CS"], False)
        self.assertFun(new_e6, [6, "F", "PositionF", 600, 60, "Econ"], True)
        e6_child = new_e6.get_direct_subordinates()
        self.assertTrue(len(e6_child) == 1)
        e3 = e6_child[0]
        self.assertFun(e3, [3, "C", "PositionC", 300, 30, "Econ"], False)
        self.assertFun(e3.get_superior(), [6, "F", "PositionF", 600, 60, "Econ"], True)
        e3_child = e3.get_direct_subordinates()
        self.assertTrue(len(e3_child) == 2)
        e4, e5 = e3_child[0], e3_child[1]
        self.assertFun(e4, [4, "D", "PositionD", 400, 40, "Econ"], False)
        self.assertFun(e4.get_superior(), [3, "C", "PositionC", 300, 30, "Econ"], False)
        self.assertTrue(e4.get_direct_subordinates() == [])
        self.assertFun(e5, [5, "E", "PositionE", 500, 50, "Econ"], False)
if __name__ == '__main__':
    unittest.main()
