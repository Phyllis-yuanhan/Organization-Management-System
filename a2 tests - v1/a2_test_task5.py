import unittest
from organization_hierarchy import *

class TestSalaryTree(unittest.TestCase):
    def setUp(self) -> None:
        def assertFun(tree, data):
            department_name, salary, numChild = data[0], data[1], data[2]
            self.assertEqual(department_name, tree.department_name)
            self.assertEqual(salary, tree.salary)
            self.assertEqual(numChild, len(tree.subdepartments))
        self.assertFun = assertFun

    def test_none(self):
        o = Organization()
        self.assertIsNone(create_department_salary_tree(o))

    def test_simple(self):
        o = Organization()
        e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        o.add_employee(e2)
        o.add_employee(e1, 2)
        o.add_employee(e3)
        dst = create_department_salary_tree(o)
        self.assertFun(dst, ["Company", 50000, 1])
        child = dst.subdepartments[0]
        self.assertFun(child, ["Department", 15000, 0])

    def test_handout(self):
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "Some Corp")
        e2 = Leader(2, "Dave", "CFO", 150000, 30, "Finance")
        e3 = Employee(3, "Bob", "Assistant", 80000, 20)
        e4 = Leader(4, "Ellen", "Head", 70000, 20, "HR")
        e5 = Employee(5, "Gina", "Employee", 40000, 70)
        e6 = Employee(6, "Fred", "Manager", 60000, 10)
        e7 = Employee(7, "Carol", "Secretary", 60000, 40)
        e2.become_subordinate(e1)
        e3.become_subordinate(e1)
        e4.become_subordinate(e1)
        e5.become_subordinate(e4)
        e6.become_subordinate(e4)
        e7.become_subordinate(e1)
        o = Organization(e1)
        dst = create_department_salary_tree(o)
        self.assertFun(dst, ["Some Corp", 130000, 2])
        fin = dst.subdepartments[0]
        hr = dst.subdepartments[1]
        self.assertFun(fin, ["Finance", 150000, 0])
        self.assertFun(hr, ["HR", (170000 / 3), 0])

    def test_linear(self):
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "CS")
        self.e2 = Leader(2, "B", "PositionB", 200, 20, "Math")
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        o = Organization(self.e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 100, 1])
        math = root.subdepartments[0]
        self.assertFun(math, ["Math", 250, 0])

    def test_no_compress(self):
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "CS")
        e2 = Leader(2, "Dave", "CFO", 150000, 30, "Math")
        e3 = Leader(3, "Bob", "Assistant", 80000, 20, "Econ")
        e4 = Leader(4, "Ellen", "Head", 70000, 20, "HR")
        e5 = Leader(5, "Gina", "Employee", 40000, 70, "Design")
        e5.become_subordinate(e3)
        e4.become_subordinate(e2)
        e3.become_subordinate(e1)
        e2.become_subordinate(e1)
        o = Organization(e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 250000, 2])
        Math = root.subdepartments[0]
        Econ = root.subdepartments[1]
        self.assertFun(Math, ["Math", 150000, 1])
        self.assertFun(Econ, ["Econ", 80000, 1])
        HR = Math.subdepartments[0]
        Design = Econ.subdepartments[0]
        self.assertFun(HR, ["HR", 70000, 0])
        self.assertFun(Design, ["Design", 40000, 0])

    def test_multiple_compress(self):
        """
        Before:
            e1(CS)
            /   \
        e2      e3(Econ)
                /   \
                e4  e5(Design)
                    /\
                e6      e7
        After:
            CS
            |
            Econ
            |
            Design
        """
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "CS")
        e2 = Employee(2, "Dave", "CFO", 150000, 30)
        e3 = Leader(3, "Bob", "Assistant", 80000, 20, "Econ")
        e4 = Employee(4, "Ellen", "Head", 70000, 20)
        e5 = Leader(5, "Gina", "Employee", 30000, 70, "Design")
        e6 = Employee(6, "Fred", "Manager", 60000, 10)
        e7 = Employee(7, "Carol", "Secretary", 60000, 40)

        e7.become_subordinate(e5)
        e6.become_subordinate(e5)
        e5.become_subordinate(e3)
        e4.become_subordinate(e3)
        e3.become_subordinate(e1)
        e2.become_subordinate(e1)
        o = Organization(e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 200000, 1])
        econ = root.subdepartments[0]
        self.assertFun(econ, ["Econ", 75000.0, 1])
        design = econ.subdepartments[0]
        self.assertFun(design, ["Design", 50000.0, 0])

    def test_multiple_compress_2(self):
        """
        Before:
            e1(CS)
            |
           e2(Math)
           /|  \
        e3(Econ)  e4 e5(Design)
        |               |
        e6              e7

        After:
            CS
            |
            Math
            /\
         Econ Design
        """
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "CS")
        e2 = Leader(2, "Dave", "CFO", 150000, 30, "Math")
        e3 = Leader(3, "Bob", "Assistant", 80000, 20, "Econ")
        e4 = Employee(4, "Ellen", "Head", 70000, 20)
        e5 = Leader(5, "Gina", "Employee", 30000, 70, "Design")
        e6 = Employee(6, "Fred", "Manager", 60000, 10)
        e7 = Employee(7, "Carol", "Secretary", 60000, 40)
        e2.become_subordinate(e1)
        e3.become_subordinate(e2)
        e4.become_subordinate(e2)
        e5.become_subordinate(e2)
        e6.become_subordinate(e3)
        e7.become_subordinate(e5)
        o = Organization(e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 250000.0, 1])
        Math = root.subdepartments[0]
        self.assertFun(Math, ["Math", 110000.0, 2])
        Econ = Math.subdepartments[0]
        Design = Math.subdepartments[1]
        self.assertFun(Econ, ["Econ", 70000.0, 0])
        self.assertFun(Design, ["Design", 45000.0, 0])

    def test_multiple_compress_3(self):
        """
        Before:
                        e1(CS)
            /           |       \
            e2(Math)    e3    e4(Econ)
            /|  \               /       |   \
        e5(Design)e6  e7(Ling) e8(Music) e9 e10(Nero)
        |              |        |           |
        e11            e12      e13         e14
        After:
            CS
            /   |
            Math    Econ
            /\          /|
        Design Ling Music Nero
        """
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "CS")
        e2 = Leader(2, "Dave", "CFO", 150000, 30, "Math")
        e3 = Employee(3, "Ellen", "Head", 70000, 20)
        e4 = Leader(4, "Bob", "Assistant", 80000, 20, "Econ")
        e5 = Leader(5, "Gina", "Employee", 30000, 70, "Design")
        e6 = Employee(6, "Fred", "Manager", 60000, 10)
        e7 = Leader(7, "Carol", "Secretary", 60000, 40, "Ling")
        e8 = Leader(8, "Carol", "Secretary", 60000, 40, "Music")
        e9 = Employee(9, "Fred", "Manager", 60000, 10)
        e10 = Leader(10, "Carol", "Secretary", 60000, 40, "Nero")
        e11 = Employee(9, "Fred", "Manager", 60000, 10)
        e12 = Employee(9, "Fred", "Manager", 60000, 10)
        e13 = Employee(9, "Fred", "Manager", 100000, 10)
        e14 = Employee(9, "Fred", "Manager", 70000, 10)
        e2.become_subordinate(e1)
        e3.become_subordinate(e1)
        e4.become_subordinate(e1)
        e5.become_subordinate(e2)
        e6.become_subordinate(e2)
        e7.become_subordinate(e2)
        e8.become_subordinate(e4)
        e9.become_subordinate(e4)
        e10.become_subordinate(e4)
        e11.become_subordinate(e5)
        e12.become_subordinate(e7)
        e13.become_subordinate(e8)
        e14.become_subordinate(e10)
        o = Organization(e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 160000.0, 2])
        Math = root.subdepartments[0]
        Econ = root.subdepartments[1]
        self.assertFun(Math, ["Math", 105000.0, 2])
        self.assertFun(Econ, ["Econ", 70000.0, 2])
        Design = Math.subdepartments[0]
        Ling = Math.subdepartments[1]
        Music = Econ.subdepartments[0]
        Nero = Econ.subdepartments[1]
        self.assertFun(Design, ["Design", 45000.0, 0])
        self.assertFun(Ling, ["Ling", 60000.0, 0])
        self.assertFun(Music, ["Music", 80000.0, 0])
        self.assertFun(Nero, ["Nero", 65000.0, 0])

    def test_multiple_4(self):
        """
        Before:
            e1(CS)
            /       |
        e2(Math)    e3(Econ)
        /  \   \            /       \
        e4(Hr) e5 e6      e7(Ling)  e8
        |   \               |
        e9(Music)  e10      e11(Nero)
        /   \   \
        e12 e13 e14
        After:
            CS
            /\
            Math Econ
            |      |
            HR      Ling
            |       |
            Music      Nero

        """
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "CS")
        e2 = Leader(2, "Dave", "CFO", 150000, 30, "Math")
        e3 = Leader(3, "Ellen", "Head", 70000, 20, "Econ")
        e4 = Leader(4, "Bob", "Assistant", 80000, 20, "Hr")
        e5 = Employee(5, "Gina", "Employee", 30000, 70)
        e6 = Employee(6, "Fred", "Manager", 60000, 10)
        e7 = Leader(7, "Carol", "Secretary", 60000, 40, "Ling")
        e8 = Employee(8, "Carol", "Secretary", 60000, 40)
        e9 = Leader(9, "Fred", "Manager", 60000, 10, "Music")
        e10 = Employee(10, "Carol", "Secretary", 60000, 40)
        e11 = Leader(9, "Fred", "Manager", 60000, 10, "Nero")
        e12 = Employee(9, "Fred", "Manager", 60000, 10)
        e13 = Employee(9, "Fred", "Manager", 100000, 10)
        e14 = Employee(9, "Fred", "Manager", 70000, 10)
        e2.become_subordinate(e1)
        e3.become_subordinate(e1)
        e4.become_subordinate(e2)
        e5.become_subordinate(e2)
        e6.become_subordinate(e2)
        e7.become_subordinate(e3)
        e8.become_subordinate(e3)
        e9.become_subordinate(e4)
        e10.become_subordinate(e4)
        e11.become_subordinate(e7)
        e12.become_subordinate(e9)
        e13.become_subordinate(e9)
        e14.become_subordinate(e9)
        o = Organization(e1)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["CS", 250000.0, 2])
        math = root.subdepartments[0]
        econ = root.subdepartments[1]
        self.assertFun(math, ["Math", 80000.0, 1])
        self.assertFun(econ, ["Econ", 65000.0, 1])
        Hr = math.subdepartments[0]
        Ling = econ.subdepartments[0]
        self.assertFun(Hr, ["Hr", 70000.0, 1])
        self.assertFun(Ling, ["Ling", 60000.0, 1])
        Music = Hr.subdepartments[0]
        Nero = Ling.subdepartments[0]
        self.assertFun(Music, ["Music", 72500.0, 0])
        self.assertFun(Nero, ["Nero", 60000.0, 0])

    def test_nest_type_1(self):
        """
        A(1, A, PositionA, 20000, 10, Company )
        |
        B(2, B, PositionB, 40000, 20)
        |
        C(3, C, PositionC, 90000, 30)
        |
        D(4, D, PositionD, 40000, 40, Department)
        After:
        A(50000, Company)
        |
        D(40000, Department)
        """
        a = Leader(1, "A", "PositionA", 20000, 10, "Company")
        b = Employee(2, "B", "PositionB", 40000, 20)
        c = Employee(3, "C", "PositionC", 90000, 30)
        d = Leader(4, "D", "PositionD", 40000, 40, "Department")
        b.become_subordinate(a)
        c.become_subordinate(b)
        d.become_subordinate(c)
        o = Organization(a)
        dst = create_department_salary_tree(o)
        self.assertFun(dst, ["Company", 50000, 1])
        first_child = dst.subdepartments[0]
        self.assertFun(first_child, ["Department", 40000, 0])

    def test_nest_type_2(self):
        """
            A(1, A, PositionA, 30000, 10, Company)
            |
        B(2, B, Position, 60000, 20)
            /                           |
        C(3, C, PosiiotnC, 30000, 30)   D(D, PositionD, 10000, 40, DepartmentA)
                                        |
                                        E (E, PositionE, 20000, 50, DepartmentB)
        After:
        A(Company, 40000)
        |
        D(DepartmentA, 10000)
        |
        E(DepartmentB, 20000)
        """
        a = Leader(1, "A", "PositionA", 30000, 10, "Company")
        b = Employee(2, "B", "PositionB", 60000, 20)
        c = Employee(3, "C", "PositionC", 30000, 30)
        d = Leader(4, "D", "PositionD", 10000, 40, "DepartmentA")
        e = Leader(5, "E", "PositionE", 20000, 50, "DepartmentB")
        b.become_subordinate(a)
        c.become_subordinate(b)
        d.become_subordinate(b)
        e.become_subordinate(d)
        o = Organization(a)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["Company", 40000, 1])
        first_child = root.subdepartments[0]
        self.assertFun(first_child, ["DepartmentA", 10000, 1])
        second_child = first_child.subdepartments[0]
        self.assertFun(second_child, ["DepartmentB", 20000, 0])

    def test_nest_type_3(self):
        """
                A(1, A, PositionA, 30000, 10, Company)
                |
                B(2, B, PositionB, 60000, 20)
                |
                E(5, E, PositionE, 120000, 50)
                /                                       |
            D(4, PositionD, 30000, 20, DepartmentB)      C(3, PositionC, 40000, 20, DepartmentA)
        After:
            A(70000, Company)
            /|
        D(40000, DepartmentA) C(30000, DepartmentB)
        """
        a = Leader(1, "A", "PositionA", 30000, 10, "Company")
        b = Employee(2, "B", "PositionB", 60000, 20)
        e = Employee(5, "E", "PositionE", 120000, 50)
        d = Leader(4, "D", "PositionD", 30000, 40, "DepartmentB")
        c = Leader(3, "C", "Position3", 40000, 20, "DepartmentA")
        b.become_subordinate(a)
        e.become_subordinate(b)
        c.become_subordinate(e)
        d.become_subordinate(e)
        o = Organization(a)
        root = create_department_salary_tree(o)
        self.assertFun(root, ["Company", 70000, 2])
        first_child = root.subdepartments[0]
        self.assertFun(first_child, ["DepartmentA", 40000, 0])
        second_child = root.subdepartments[1]
        self.assertFun(second_child, ["DepartmentB", 30000, 0])

    def test_nest_type_4(self):
        """
        Before:
                        A(1, 10000, Company)
                         /       \
                B(20000)               C(30000)
                    /       \          /      |
                G(70000, dG)  F(60000, dF)       E(50000, dE)      D(40000, dD)
                |               |               |                   |
            K(110000)       J(100000)           I(90000)            H(80000)
                |           |               |                   |
            O(150000, dO)  N(140000, dN)  M(130000, dM)     L(120000, dL)
        After:
                A(20000, Company)
                /               |               |               \
            D(60000, dD)       E(70000, dE)     F(80000, dF)   G(90000, dG)
            |                   |               |               |
            L(120000, dL)       M(130000, dM)   N(140000, dN)   O(150000, dO)
        """
        a = Leader(1, "", "", 10000, 10, "Company")
        b = Employee(2, "", "", 20000, 20)
        c = Employee(3, "", "", 30000, 30)
        d = Leader(4, "", "", 40000, 40, "DepartmentD")
        e = Leader(5, "", "", 50000, 50, "DepartmentE")
        f = Leader(6, "", "", 60000, 60, "DepartmentF")
        g = Leader(7, "", "", 70000, 70, "DepartmentG")
        h = Employee(8, "", "", 80000, 20)
        i = Employee(9, "", "", 90000, 20)
        j = Employee(10, "", "", 100000, 20)
        k = Employee(11, "", "", 110000, 20)
        l = Leader(12, "", "", 120000, 70, "DepartmentL")
        m = Leader(13, "", "", 130000, 70, "DepartmentM")
        n = Leader(14, "", "", 140000, 70, "DepartmentN")
        o = Leader(15, "", "", 150000, 70, "DepartmentO")
        b.become_subordinate(a)
        c.become_subordinate(a)
        d.become_subordinate(c)
        e.become_subordinate(c)
        f.become_subordinate(b)
        g.become_subordinate(b)
        h.become_subordinate(d)
        i.become_subordinate(e)
        j.become_subordinate(f)
        k.become_subordinate(g)
        l.become_subordinate(h)
        m.become_subordinate(i)
        n.become_subordinate(j)
        o.become_subordinate(k)
        org = Organization(a)
        root = create_department_salary_tree(org)
        self.assertFun(root, ["Company", 20000, 4])
        children = root.subdepartments
        first_child, second_child, third_child, fourth_child = children[0], children[1], children[2], children[3]
        self.assertFun(first_child, ["DepartmentD", 60000, 1])
        self.assertFun(second_child, ["DepartmentE", 70000, 1])
        self.assertFun(third_child, ["DepartmentF", 80000, 1])
        self.assertFun(fourth_child, ["DepartmentG", 90000, 1])
        dl = first_child.subdepartments[0]
        dm = second_child.subdepartments[0]
        dn = third_child.subdepartments[0]
        do = fourth_child.subdepartments[0]
        self.assertFun(dl, ["DepartmentL", 120000, 0])
        self.assertFun(dm, ["DepartmentM", 130000, 0])
        self.assertFun(dn, ["DepartmentN", 140000, 0])
        self.assertFun(do, ["DepartmentO", 150000, 0])


if __name__ == '__main__':
    unittest.main()
