import unittest
from organization_hierarchy import *

def employee_eq(e1, e2):
    name_eq = e1.name == e2.name
    position_eq = e1.position == e2.position
    eid_eq = e1.eid == e2.eid
    salary_eq = e1.salary == e2.salary
    rating_eq = e1.rating == e2.rating
    cons = [name_eq, position_eq, eid_eq, salary_eq, rating_eq]
    return all(cons)


class MergeTest(unittest.TestCase):
    def test_merge_1(self):
        l1 = []
        l2 = []
        self.assertEqual(merge(l1, l2), [], "Two empty list should obtain an empty list")
        l1 = [1 for _ in range(10)]
        l2 = [1 for _ in range(10)]
        exp = [1 for _ in range(20)]
        self.assertListEqual(merge(l1, l2), exp, "Two list with same elements should merge to a list with same elements")

    def test_merge_2(self):
        l1 = []
        l2 = [1, 2, 3]
        self.assertListEqual(merge(l1, l2), l2, "An empty list with an non empty list should obtain the non-empty one")
        self.assertListEqual(merge(l2, l1), l2, "An empty list with an non empty list should obtain the non-empty one")

    def test_merge_3(self):
        l1 = [1, 9]
        l2 = [2, 3, 4]
        exp = [1, 2, 3, 4, 9]
        self.assertListEqual(merge(l1, l2), exp, "You should obtain an ordered list")
        self.assertListEqual(merge(l2, l1), exp, "You should obtain an ordered list")
        exp.insert(0, 1)
        exp.append(9)
        self.assertListEqual(merge(merge(l1, l2), l1), exp, "You should obtain an ordered list")
        exp = [1, 1, 2, 2, 3, 3, 4, 4, 9, 9]
        self.assertListEqual(merge(merge(merge(l1, l2), l1), l2), exp, "You should obtain an ordered list")

    def test_merge_4(self):
        l1 = [1]
        l2 = [1, 2, 3]
        exp = [1, 1, 2, 3]
        self.assertListEqual(merge(l1, l2), exp, "You should obtain an ordered list")
        self.assertListEqual(merge(l2, l1), exp, "You should obtain an ordered list")
        self.assertListEqual(merge(l2, [9]), [1, 2, 3, 9], "You shoule obtain an ordered list")


class EmployeeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "e1", "Dev", 1000, 10)
        self.e2 = Employee(2, "e2", "HR", 2000, 10)
        self.e3 = Employee(3, "e3", "Eng", 3000, 10)
        self.employees = [self.e1, self.e2, self.e3]
        self.lt_format = "The employee1's eid is {!s} and the second employee's eid is {!s}".format

    def tearDown(self) -> None:
        self.e1 = Employee(1, "e1", "Dev", 1000, 10)
        self.e2 = Employee(2, "e2", "HR", 2000, 10)
        self.e3 = Employee(3, "e3", "Eng", 3000, 10)
        self.employees = [self.e1, self.e2, self.e3]

    def test_lt(self):
        self.assertLess(self.e1, self.e2, self.lt_format(self.e1.eid, self.e2.eid))
        self.assertGreater(self.e2, self.e1, self.lt_format(self.e2.eid, self.e1.eid))

    def test_lt_2(self):
        temp = Leader(100, "c", "w", 1000, 10, "CS")
        self.assertLess(self.e1, temp, self.lt_format(self.e1.eid, temp.eid))
        self.assertTrue(all([temp > e for e in self.employees]),
                        "The first employee's eid is 3 it is greater than every other employee")
        self.assertGreater(temp, self.e1, self.lt_format(temp.eid, self.e1.eid))
        temp2 = Leader(400, "d", "s", 2000, 20, "ECO")
        self.assertGreater(temp2, temp, self.lt_format(temp2.eid, temp.eid))

    def test_become_subordinate_1(self):
        self.e1.become_subordinate(None)
        self.assertIsNone(self.e1.get_superior())

    def test_become_subordinate_2(self):
        self.e3.become_subordinate(self.e2)
        self.assertTrue(employee_eq(self.e3.get_superior(), self.e2))
        self.e3.become_subordinate(self.e1)
        self.assertTrue(self.e2.get_direct_subordinates() == [])
        self.assertTrue(employee_eq(self.e3.get_superior(), self.e1))
        self.assertTrue(employee_eq(self.e1.get_direct_subordinates()[0], self.e3))

    def test_get_direct_subordinates_1(self):
        self.assertTrue([temp.get_direct_subordinates() == [] for temp in self.employees],
                        "You should return [] for employee with no subordinates")

    def test_get_direct_subordinates_2(self):
        self.e1.become_subordinate(self.e2)
        self.assertTrue(self.e1.get_direct_subordinates() == [], "")
        act = self.e2.get_direct_subordinates()
        self.assertTrue(employee_eq(self.e1, act[0]), "Simple")

    def test_get_direct_subordinates_3(self):
        self.e2.become_subordinate(self.e3)
        self.e1.become_subordinate(self.e3)
        act = self.e3.get_direct_subordinates()
        act_eids = [temp.eid for temp in act]
        self.assertListEqual(act_eids, [1, 2], "You should return the list by the sorting order of eid")
        self.assertTrue([employee_eq(act[i], self.employees[i])for i in range(2)], "You should obtain the same sub list")

    def test_get_all_leaf(self):
        self.assertTrue(all(temp.get_all_subordinates() == [] for temp in self.employees),
                        "You should return empty list for employee with no sub")

    def test_get_all_straight_line(self):
        """
        e3 -> e2 -> e1 -> e5 -> e4
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 6)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e1.become_subordinate(e2)
        e4.become_subordinate(e5)
        e5.become_subordinate(e1)
        e2.become_subordinate(e3)
        act = e3.get_all_subordinates()
        act_eids = [temp.eid for temp in act]
        self.assertListEqual(act_eids, [1, 2, 4, 5], "You should return the list by the sorting order of eid")
        employees.remove(e3)
        self.assertTrue([employee_eq(act[i], employees[i]) for i in range(len(employees))],
                        "You should obtain the same sub list")

    def test_get_all_left_tree(self):
        """
            e4
            /
          e2
          /\
        e3 e1
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 5)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e3.become_subordinate(e2)
        e1.become_subordinate(e2)
        e2.become_subordinate(e4)
        act = e4.get_all_subordinates()
        act_eids = [temp.eid for temp in act]
        self.assertListEqual(act_eids, [1, 2, 3], "You should return the list by the sorting order of eid")
        employees.remove(e4)
        self.assertTrue([employee_eq(act[i], employees[i]) for i in range(len(employees))],
                        "You should obtain the same sub list")

    def test_get_all_com_tree(self):
        """
             e4
            / \
          e3  e6
          /\  |
        e2 e1 e5
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 7)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e6 = employees[5]
        e3.become_subordinate(e4)
        e1.become_subordinate(e3)
        e2.become_subordinate(e3)
        e6.become_subordinate(e4)
        e5.become_subordinate(e6)
        act = e4.get_all_subordinates()
        act_eids = [temp.eid for temp in act]
        self.assertListEqual(act_eids, [1, 2, 3, 5, 6], "You should return the list by the sorting order of eid")
        employees.remove(e4)
        self.assertTrue([employee_eq(act[i], employees[i]) for i in range(len(employees))],
                        "You should obtain the same sub list")

    def test_get_head_1(self):
        self.assertTrue(all([employee_eq(temp.get_organization_head(), temp) for temp in self.employees]),
                        "Every one with no superior is the head")

    def test_get_head_2(self):
        """
                e3 -> e2 -> e1 -> e5 -> e4
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 6)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e1.become_subordinate(e2)
        e4.become_subordinate(e5)
        e5.become_subordinate(e1)
        e2.become_subordinate(e3)
        self.assertListEqual([employee.get_organization_head() for employee in employees], [e3 for _ in range(5)],
                             "The head in this tree is to be e4")

    def test_get_head_3(self):
        """
                    e4
                    /
                  e2
                  /\
                e3 e1
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 5)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e3.become_subordinate(e2)
        e1.become_subordinate(e2)
        e2.become_subordinate(e4)
        self.assertListEqual([employee.get_organization_head() for employee in employees], [e4 for _ in range(4)],
                             "The head in this tree is to be e4")

    def test_get_head_4(self):
        """
                     e4
                    / \
                  e3  e6
                  /\  |
                e2 e1 e5
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 7)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e6 = employees[5]
        e3.become_subordinate(e4)
        e1.become_subordinate(e3)
        e2.become_subordinate(e3)
        e6.become_subordinate(e4)
        e5.become_subordinate(e6)
        self.assertListEqual([employee.get_organization_head() for employee in employees], [e4 for _ in range(6)],
                             "The head in this tree is to be e4")

    def test_sup(self):
        self.assertTrue(all([temp.get_superior() is None for temp in self.employees]),
                        "Every leaf's superior has to be None")
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 7)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e6 = employees[5]
        e3.become_subordinate(e4)
        e1.become_subordinate(e3)
        e2.become_subordinate(e3)
        e6.become_subordinate(e4)
        e5.become_subordinate(e6)
        self.assertTrue(e4.get_superior() is None, "The e4 is root it has no superior")
        self.assertTrue(all([employee_eq(temp.get_superior(), e4) for temp in [e3, e6]]),
                        "Both e3 and e6 have e4 as the superior")
        self.assertTrue(all([employee_eq(temp.get_superior(), e3) for temp in [e2, e1]]),
                        "Both e2 and e1 have e3 as the superior")
        self.assertTrue(all([employee_eq(temp.get_superior(), e4) for temp in [e3, e6]]),
                        "Both e3 and e6 have e4 as the superior")
        self.assertTrue(employee_eq(e5.get_superior(), e6), "e5 is poing e6 as its superior")

    def test_remove_direct(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        subs = self.e1.get_direct_subordinates()
        self.e1.remove_subordinate_id(self.e2.eid)
        self.assertTrue(len(self.e1.get_direct_subordinates()) == len(subs),
                        "You should remove e2 from e1's subordinate")
        self.assertTrue(all([not employee_eq(self.e2, temp) for temp in self.e1.get_direct_subordinates()]),
                        "You should not contain e2 in the  subordinate list")
        self.assertTrue(len(self.e1.get_direct_subordinates()) == 1 and employee_eq(self.e3, self.e1.get_direct_subordinates()[0]))
        self.assertTrue(employee_eq(self.e2.get_superior(), self.e1), "You should let e1 remain as e2's superior")

    def test_remove_indirect(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        org_lis = self.e1.get_all_subordinates()
        self.e2.remove_subordinate_id(self.e3.eid)
        new_lis = self.e1.get_all_subordinates()
        self.assertTrue(len(org_lis) == len(new_lis) + 1,
                        "You should not include e3 in the subordinate list of e1")
        self.assertTrue(all([not employee_eq(self.e3, temp) for temp in new_lis]),
                        "You should not contain e3 in the  subordinate list")
        self.assertTrue(employee_eq(self.e3.get_superior(), self.e2), "You should let e2 remain as e3's superior")

    def test_get_employee(self):
        self.assertIsNone(self.e1.get_employee(self.e2.eid),
                          "You should return None if the given employee is not in the subordiant of e1")
        self.assertTrue(all([employee_eq(temp, temp.get_employee(temp.eid)) for temp in self.employees]),
                        "You should return the same employee if the eid is the same as itself")

    def test_get_employee2(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.assertTrue(all([employee_eq(temp, self.e1.get_employee(temp.eid)) for temp in self.employees[1:]]),
                        "You should return the same employee since it is in the subordinate")

    def test_get_employee3(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.assertTrue(all([employee_eq(temp, self.e1.get_employee(temp.eid)) for temp in self.employees[1:]]),
                        "You should return the same employee since it is in the subordinate")

    def test_get_employee4(self):
        """
                     e4
                    / \
                  e3  e6
                  /\  |
                e2 e1 e5
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100, 50) for i in range(1, 7)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e6 = employees[5]
        e3.become_subordinate(e4)
        e1.become_subordinate(e3)
        e2.become_subordinate(e3)
        e6.become_subordinate(e4)
        e5.become_subordinate(e6)
        self.assertTrue(all([employee_eq(temp, e4.get_employee(temp.eid)) for temp in employees]),
                        "You should return the same employee since it is in the subordinate")
        self.assertIsNone(e3.get_employee(e5.eid), "E5 is not a child of e3 have to return None for it")

    def test_get_paid_more_than1(self):
        self.assertTrue(all([temp.get_employees_paid_more_than(100000) == [] for temp in self.employees]),
                        "There is no employee get paid more than 100000")
        self.assertTrue(all([employee_eq(temp.get_employees_paid_more_than(0)[0], temp) and
                             len(temp.get_employees_paid_more_than(1)) == 1for temp in self.employees]),
                        "Every employee gets paid more than 1")

    def test_get_paid_more_than2(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        exp = self.e1.get_employees_paid_more_than(100)
        self.assertTrue(len(exp) == 3)
        self.assertTrue(all(employee_eq(exp[i], self.employees[i])for i in range(3)))

    def test_get_paid_more_than3(self):
        """
                     e6(100)
                    /       \
                  e5(200)  e4(300)
                  /\          |
                e3(500) e2(400) e1(600)
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (abs(6 - i) + 1), 50) for i in range(6, 0, -1)]
        e6 = employees[0]
        e5 = employees[1]
        e4 = employees[2]
        e3 = employees[3]
        e2 = employees[4]
        e1 = employees[5]
        e3.become_subordinate(e5)
        e2.become_subordinate(e5)
        e1.become_subordinate(e4)
        e4.become_subordinate(e6)
        e5.become_subordinate(e6)
        act = e6.get_employees_paid_more_than(200)
        exp = [e1, e2, e3, e4]
        self.assertTrue(len(act) == 4, "There are 4 employees get paid more than 200  ")
        self.assertTrue(all([employee_eq(exp[i], act[i]) for i in range(len(exp))]))

    def test_get_paid_more_than4(self):
        """
            e3(200) -> e2(100) -> e4(100) -> e5(200) -> e1(200)
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (i % 2 + 1), 50) for i in range(1, 6)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e1.become_subordinate(e5)
        e5.become_subordinate(e4)
        e4.become_subordinate(e2)
        e2.become_subordinate(e3)
        act = e3.get_employees_paid_more_than(100)
        exp = [e1, e3, e5]
        self.assertTrue(len(act) == 3, "From e3, there are 3 employees get paid more than 100  ")
        self.assertTrue(all([employee_eq(exp[i], act[i]) for i in range(len(exp))]))

    def test_get_higher_paid(self):
        self.assertTrue(all([_.get_higher_paid_employees() == []for _ in self.employees]))

    def test_get_higher_paid2(self):
        """
                    e3(200) -> e2(100) -> e4(100) -> e5(200) -> e1(200)
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (i % 2 + 1), 50) for i in range(1, 6)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e1.become_subordinate(e5)
        e5.become_subordinate(e4)
        e4.become_subordinate(e2)
        e2.become_subordinate(e3)
        act = e2.get_higher_paid_employees()
        exp = [e1, e3, e5]
        self.assertTrue(len(act) == 3, "There are 3 employees get paid more than 100")
        self.assertTrue(all([employee_eq(exp[i], act[i]) for i in range(len(exp))]))
        act2 = e4.get_higher_paid_employees()
        self.assertTrue(len(act2) == 3, "There are 3 employees get paid more than 100")
        self.assertTrue(all([employee_eq(exp[i], act2[i]) for i in range(len(exp))]))

    def test_get_higher_paid3(self):
        """
                            e6(100)
                           /       \
                         e5(200)  e4(300)
                         /\          |
                       e3(500) e2(400) e1(600)
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (abs(6 - i) + 1), 50) for i in range(6, 0, -1)]
        e6 = employees[0]
        e5 = employees[1]
        e4 = employees[2]
        e3 = employees[3]
        e2 = employees[4]
        e1 = employees[5]
        e3.become_subordinate(e5)
        e2.become_subordinate(e5)
        e1.become_subordinate(e4)
        e4.become_subordinate(e6)
        e5.become_subordinate(e6)
        self.assertTrue(e1.get_higher_paid_employees() == [], "No one in the tree get paid more than 600")
        act1 = e6.get_higher_paid_employees()
        exp1 = [e1, e2, e3, e4, e5]
        self.assertTrue(len(act1) == 5, "There are 5 employees get paid more than 100  ")
        self.assertTrue(all([employee_eq(exp1[i], act1[i]) for i in range(len(exp1))]))
        act2 = e5.get_higher_paid_employees()
        exp2 = [e1, e2, e3, e4]
        self.assertTrue(len(act2) == 4, "There are 4 employees get paid more than 200  ")
        self.assertTrue(all([employee_eq(exp2[i], act2[i]) for i in range(len(exp2))]))
        act3 = e4.get_higher_paid_employees()
        exp3 = [e1, e2, e3]
        self.assertTrue(len(act3) == 3, "There are 4 employees get paid more than 200  ")
        self.assertTrue(all([employee_eq(exp3[i], act3[i]) for i in range(len(exp3))]))
        for i in range(len(employees) - 1):
            act = employees[i].get_higher_paid_employees()
            exp = employees[i + 1:][::-1]
            acc = []
            for j in range(len(exp)):
                acc.append(employee_eq(act[j], exp[j]))
            self.assertTrue(all(acc))

    def test_get_common_2(self):
        """
            e1 -> e2 -> e3 -> e4 -> e5
        """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (i % 2 + 1), 50) for i in range(1, 6)]
        e1 = employees[0]
        e2 = employees[1]
        e3 = employees[2]
        e4 = employees[3]
        e5 = employees[4]
        e5.become_subordinate(e4)
        e4.become_subordinate(e3)
        e3.become_subordinate(e2)
        e2.become_subordinate(e1)
        for i in range(0, len(employees)):
            employee = employees[i]
            temp = list(filter(lambda x: employee.eid != x.eid, employees))
            for _ in temp:
                act = employee.get_closest_common_superior(_.eid)
                if _.eid < employee.eid:
                    exp = _
                else:
                    exp = employee
                self.assertTrue(employee_eq(exp, act), "The common superior for e{} and e{} is e{} your answer is e{}".format(i + 1, _.eid, exp.eid, act.eid))

    def test_get_common_3(self):
        """
                                    e6
                                   / \
                                 e5  e4
                                 /\   |
                               e3 e2 e1
                """
        employees = [Employee(i, str(i + 10), str(i + 100), 100 * (abs(6 - i) + 1), 50) for i in range(6, 0, -1)]
        e6 = employees[0]
        e5 = employees[1]
        e4 = employees[2]
        e3 = employees[3]
        e2 = employees[4]
        e1 = employees[5]
        e3.become_subordinate(e5)
        e2.become_subordinate(e5)
        e1.become_subordinate(e4)
        e4.become_subordinate(e6)
        e5.become_subordinate(e6)
        self.assertTrue(employee_eq(e5, e3.get_closest_common_superior(e2.eid)),
                        "The closest common superior for e3 and e2 is e5")
        self.assertTrue(employee_eq(e6, e5.get_closest_common_superior(e1.eid)),
                        "The closest common superior for e5 and e1 is e5")
        self.assertTrue(employee_eq(e6, e2.get_closest_common_superior(e4.eid)),
                        "The closest common superior for e2 and e3 is e6")
        self.assertTrue(employee_eq(e6, e5.get_closest_common_superior(e4.eid)),
                        "The closest common superior for e4 and e5 is e6")
        self.assertTrue(employee_eq(e4, e1.get_closest_common_superior(e4.eid)),
                        "The closest common superior for e1 and e4 is e4")


class OrganizationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 200, 20)
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e4 = Employee(4, "D", "PositionD", 400, 40)
        self.e5 = Employee(5, "E", "PositionE", 500, 50)
        self.organization = Organization()

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 200, 20)
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e4 = Employee(4, "D", "PositionD", 400, 40)
        self.e5 = Employee(5, "E", "PositionE", 500, 50)
        self.organization = Organization()

    def test_add(self):
        self.organization.add_employee(self.e1)
        head = self.organization.get_head()
        self.assertTrue(employee_eq(head, self.e1))

    def test_add2(self):
        self.organization.add_employee(self.e1)
        self.organization.add_employee(self.e2, self.e1.eid)
        head = self.organization.get_head()
        self.assertTrue(employee_eq(head, self.e1))
        self.assertTrue(len(head.get_direct_subordinates()) == 1)
        self.assertTrue(employee_eq(head.get_direct_subordinates()[0], self.e2))

    def test_add3(self):
        self.organization.add_employee(self.e1)
        self.organization.add_employee(self.e2, self.e1.eid)
        self.organization.add_employee(self.e3)
        head = self.organization.get_head()
        self.assertTrue(employee_eq(head, self.e3))
        self.assertTrue(len(head.get_direct_subordinates()) == 1)
        self.assertTrue(employee_eq(head.get_direct_subordinates()[0], self.e1))
        self.assertTrue(employee_eq(head.get_direct_subordinates()[0].get_direct_subordinates()[0], self.e2))

    def test_get_emp(self):
        for i in range(10):
            self.assertIsNone(self.organization.get_employee(i))

    def test_get_position(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        self.organization = Organization(self.e1)
        self.assertEqual([], self.organization.get_employees_with_position(""))

    def test_get_position2(self):
        self.e1.position = "Developer"
        self.e2.position = "Developer"
        self.e5.position = "Developer"
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        self.organization = Organization(self.e1)
        temp = self.organization.get_employees_with_position("Developer")
        temp.sort(key=lambda x:x.eid)
        eids = [_.eid for _ in temp]
        self.assertListEqual([1, 2, 5], eids)

    def test_get_avg(self):
        self.e1.position = "Developer"
        self.e2.position = "Developer"
        self.e5.position = "Developer"
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        self.organization = Organization(self.e1)
        self.assertEqual(300.0, self.organization.get_average_salary())
        self.assertEqual(800 / 3, self.organization.get_average_salary("Developer"))

    def test_get_next_id(self):
        self.e3.become_subordinate(self.e2)
        self.e4.become_subordinate(self.e3)
        self.organization = Organization(self.e2)
        self.assertEqual(1, self.organization.get_next_free_id())

    def test_get_next_id2(self):
        self.e2.become_subordinate(self.e1)
        self.e5.become_subordinate(self.e1)
        self.organization = Organization(self.e1)
        self.assertEqual(3, self.organization.get_next_free_id())

    def test_get_next_id3(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.organization = Organization(self.e1)
        self.assertEqual(4, self.organization.get_next_free_id())


if __name__ == '__main__':
    unittest.main(exit=False)
