import unittest
from organization_hierarchy import *
from a2_test import employee_eq


class TestHighestRating(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "Pa", 100, 10)
        self.e2 = Employee(2, "B", "Pb", 100, 20)
        self.e3 = Employee(3, "C", "Pc", 100, 30)

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "Pa", 100, 10)
        self.e2 = Employee(2, "B", "Pb", 100, 20)
        self.e3 = Employee(3, "C", "Pc", 100, 30)

    def test_simple(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.assertTrue(employee_eq(self.e1.get_highest_rated_subordinate(), self.e3),
                        "e3 has the highest rating amont e1's direct children")

    def test_simple2(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.assertTrue(employee_eq(self.e1.get_highest_rated_subordinate(), self.e2),
                        "e2 is the only direct child of e1")
        self.e1.add_subordinate(Employee(5, "a", "a", 1, 1))
        self.assertTrue(employee_eq(self.e1.get_highest_rated_subordinate(), self.e2),
                        "e2 is still the highest rating one among e1'direct children")

    def test_simple3(self):
        self.e3.rating = 20
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e1.add_subordinate(Employee(5, "a", "a", 1, 20))
        self.assertTrue(employee_eq(self.e1.get_highest_rated_subordinate(), self.e2),
                        "Return the one with lowest eid in case of the tie")


class TestObtain(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def test_obtain_handout(self):
        """
        Before:
             e1
            / \
           e2  e3
               /\
            e4  e5
        After:
            e1
            / \
           e2 e4
           / |
         e3  e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e2.obtain_subordinates([3, 5])
        self.assertIsNone(act.get_superior(), "You should return the Head of the Organization")
        subs = act.get_direct_subordinates()
        exp_eids = [2, 4]
        act_eids = [temp.eid for temp in subs]
        self.assertListEqual(exp_eids, act_eids, "You should only have two children under the head of the organization")
        exp_eids2 = [3, 5]
        act_eids2 = [temp.eid for temp in subs[0].get_direct_subordinates()]
        self.assertListEqual(exp_eids2, act_eids2, "You should obtain children to the proper tree")
        self.assertTrue(subs[1].get_direct_subordinates() == [], "You should move the chilren from the oringinal tree")

    def test_obtain_linear(self):
        """
        Before:
        e1
        |
        e2
        |
        e3
        |
        e4
        |
        e5
        After:
         e1
         / |
        e2  e3
            |
            e4
            |
            e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e4)
        act = self.e1.obtain_subordinates([2])
        act_subs = act.get_direct_subordinates()
        act_eids = [temp.eid for temp in act_subs]
        self.assertListEqual(act_eids, [2, 3], "The children of e2 should point to e1")
        self.assertTrue(act_subs[0].get_direct_subordinates() == [], "There should be no children under e2 at now")
        self.assertTrue(all([employee_eq([self.e4, self.e5][i], act_subs[1].get_all_subordinates()[i]) for i in range(0, len(act_subs[1].get_direct_subordinates()))]), "e4 and e5 should remain under e3")

    def test_obtain_internal(self):
        """
        Before:
             e1
             |
            e2
            /|
           e3 e4
             / |
            e5 e6
            |
            e7
        After:
            e1
            / |
           e2  e3
         / \   /|
        e6 e7 e4 e5
        """
        e1 = Employee(1, "A", "PositionA", 100, 10)
        e2 = Employee(2, "B", "PositionB", 100, 20)
        e3 = Employee(3, "C", "PositionC", 100, 30)
        e4 = Employee(4, "D", "PositionD", 100, 40)
        e5 = Employee(5, "E", "PositionE", 100, 50)
        e6 = Employee(6, "F", "PositionF", 100, 60)
        e7 = Employee(7, "G", "PositionG", 100, 70)
        e2.become_subordinate(e1)
        e3.become_subordinate(e2)
        e4.become_subordinate(e2)
        e5.become_subordinate(e4)
        e6.become_subordinate(e4)
        e7.become_subordinate(e5)
        act = e1.obtain_subordinates([3])
        act = act.get_direct_subordinates()[1].obtain_subordinates([4, 5])
        self.assertTrue(act.eid == 1, "e1 should remain as the head")
        self.assertTrue(len(act.get_direct_subordinates()) == 2, "You moved e3 under e1")
        new_e2 = act.get_direct_subordinates()[0]
        new_e3 = act.get_direct_subordinates()[1]
        self.assertTrue(len(new_e2.get_direct_subordinates()) == 2, "You should only have two children under e2 now")
        self.assertListEqual([temp.eid for temp in new_e2.get_direct_subordinates()], [6, 7],
                             "Now e6 and e7 should be the children under e2")
        self.assertTrue(len(new_e3.get_direct_subordinates()) == 2, "You should have two children under e3 now")
        self.assertListEqual([temp.eid for temp in new_e3.get_direct_subordinates()], [4, 5],
                             "Now e4 and e5 should be the children under e3")

    def test_obtain_internal2(self):
        """
        Before:
             e1
             |
            e2
            /|
           e3 e4
             / |
            e5 e6
            |
            e7
        After:
                  e1
            /   |  \ \  \
           e2  e3 e4 e5 e6
                     |
                     e7
        """
        e1 = Employee(1, "A", "PositionA", 100, 10)
        e2 = Employee(2, "B", "PositionB", 100, 20)
        e3 = Employee(3, "C", "PositionC", 100, 30)
        e4 = Employee(4, "D", "PositionD", 100, 40)
        e5 = Employee(5, "E", "PositionE", 100, 50)
        e6 = Employee(6, "F", "PositionF", 100, 60)
        e7 = Employee(7, "G", "PositionG", 100, 70)
        e2.become_subordinate(e1)
        e3.become_subordinate(e2)
        e4.become_subordinate(e2)
        e5.become_subordinate(e4)
        e6.become_subordinate(e4)
        e7.become_subordinate(e5)
        act = e1.obtain_subordinates([4, 2])
        self.assertTrue(act.eid == 1, "e1 should remain as the head")
        self.assertTrue(len(act.get_direct_subordinates()) == 5)
        new_e5 = act.get_direct_subordinates()[3]
        self.assertTrue(len(new_e5.get_direct_subordinates()) == 1, "You should only have two children under e2 now")
        self.assertListEqual([temp.eid for temp in new_e5.get_direct_subordinates()], [7],
                             "Now e6 and e7 should be the children under e2")

    def test_obtain_move_head(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e3
            / | | \
          e1 e2 e4 e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e3.obtain_subordinates([1])
        self.assertTrue(act.eid == 3, "e3 should be the new head")
        self.assertTrue(len(act.get_direct_subordinates()) == 4, "Both e1 and e3 now should be the child of e3")
        self.assertListEqual([temp.eid for temp in act.get_direct_subordinates()], [1, 2, 4, 5],
                             "This is the correct order of the children under e3")

    def test_obtain_move_head2(self):
        """
        Before:
                            e1
                           / \
                          e2  e3
                              /\
                           e4  e5
        After:
                     e2
                     |
                     e3
                    / |
                   e4 e5
                       |
                       e1
        """
        self.e2.rating = 30
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e5.obtain_subordinates([1])
        self.assertTrue(act.eid == 2, "e2 has the same rating with e3 but e2's eid is lower so that it should be the new head of the orgainzation")
        act_sub = act.get_direct_subordinates()
        self.assertTrue(len(act_sub) == 1 and act_sub[0].eid == 3, "e2 should only have one children which is e3")
        self.assertTrue(employee_eq(act_sub[0], self.e3))
        e3_subs = act_sub[0].get_direct_subordinates()
        self.assertListEqual([temp.eid for temp in e3_subs], [4, 5], "You should let 4 and 5 remain under the e3")
        self.assertTrue(len(e3_subs[-1].get_direct_subordinates()) == 1 and employee_eq(self.e1, e3_subs[-1].get_direct_subordinates()[-1]))

    def test_obtain_move_head3(self):
        """
        Before:
                            e1
                           / \
                          e2  e3
                              /\
                           e4  e5
        After:
                     e3
                    / |
                   e4 e5
                      /|
                    e1 e2
        """
        self.e2.rating = 30
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e5.obtain_subordinates([1, 2])
        self.assertTrue(act.eid == 3, "In this case e3 should be the new head of the organization")
        act_sub = act.get_direct_subordinates()
        self.assertTrue(len(act_sub) == 2 and [temp.eid for temp in act_sub] == [4, 5],
                        "Both e4 and e5 should remain as the children of e3")
        e5_subs = act_sub[-1].get_direct_subordinates()
        self.assertListEqual([temp.eid for temp in e5_subs], [1, 2], "You should let 1 and 2 become the children pf e5")

    def test_obtain_move_head4(self):
        """
        Before:
                            e1
                           / \
                          e2  e3
                              /\
                           e4  e5
        After:
                        e4
                        |
                        e5
                      /| \
                    e1 e2 e3
        """
        self.e2.rating = 30
        self.e4.rating = 50
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e5.obtain_subordinates([1, 2, 3])
        self.assertTrue(act.eid == 4, "In this case e4 should be the new head of the organization")
        act_sub = act.get_direct_subordinates()
        self.assertTrue(len(act_sub) == 1 and employee_eq(act_sub[0], self.e5), "In this case e5 is the only child of e4")
        self.assertListEqual([temp.eid for temp in act_sub[0].get_direct_subordinates()], [1, 2, 3],
                             "At the case e5 is the head of the organization now every one is the direct child of it")

    def test_obtain_move_head5(self):
        """
               Before:
                                   e1
                                  / \
                                 e2  e3
                                     /\
                                  e4  e5
               After:
                               e5
                             /| \ \
                           e1 e2 e3 e4
               """
        self.e2.rating = 30
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        act = self.e5.obtain_subordinates([1, 2, 3])
        self.assertTrue(act.eid == 5, "In this case e5 should be the new head of the organization")
        act_sub = act.get_direct_subordinates()
        self.assertTrue(len(act_sub) == 4 and [temp.eid for temp in act_sub] == [1, 2, 3, 4],
                        "At the case e5 is the head of the organization now every one is the direct child of it")
        self.assertTrue(
            all([temp.get_superior().eid == 5 and temp.get_direct_subordinates() == [] for temp in act_sub]))


class TestFire(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def test_fire_single_head(self):
        org = Organization(self.e1)
        org.fire_employee(self.e1.eid)
        self.assertIsNone(org.get_head())

    def test_fire_handout(self):
        """
                Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
                After:
                    e1
                    / \ \
                   e2 e4 e5

                """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_employee(self.e3.eid)
        self.assertIsNone(org.get_employee(self.e3.eid), "You should not have e3 in the organization")
        self.assertTrue(len(org.get_head().get_direct_subordinates()) == 3,
                        "You should obtain e4 and e5 as e1's direct children")
        self.assertListEqual([temp.eid for temp in org.get_head().get_direct_subordinates()], [2, 4, 5])

    def test_fire_leaf(self):
        """
                Before:
                             e1
                            / \
                           e2  e3
                               /\
                            e4  e5
                After:
                      e1
                     / \
                    e2  e3
                        |
                        e5
                """
        self.e1.rating = 30
        self.e4.rating = 10
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_employee(self.e4.eid)
        self.assertIsNone(org.get_employee(self.e4.eid), "You should not have e4 in the organization")
        self.assertTrue(len(org.get_head().get_direct_subordinates()) == 2,
                        "You should obtain e4 and e5 as e1's direct children")
        self.assertListEqual([temp.eid for temp in org.get_head().get_direct_subordinates()], [2, 3])
        new_e3 = org.get_head().get_direct_subordinates()[1]
        self.assertTrue(len(new_e3.get_direct_subordinates()) == 1)
        self.assertTrue(employee_eq(new_e3.get_direct_subordinates()[0], self.e5))

    def test_fire_linear(self):
        """
        Before:
        e1
        |
        e2
        |
        e3
        |
        e4
        |
        e5
        After:
        e1
        |
        e2
        |
        e4
        |
        e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e4)
        org = Organization(self.e1)
        org.fire_employee(self.e3.eid)
        self.assertIsNone(org.get_employee(self.e3.eid), "You should move the e3 from the organization")
        child = org.get_head().get_direct_subordinates()
        self.assertTrue(len(child) == 1, "You are not moving any direct child under e1")
        self.assertListEqual([temp.eid for temp in child[0].get_direct_subordinates()], [4],
                             "The first child of e2 has to be e4")

    def test_fire_internal(self):
        """
        Before:
             e1
             |
            e2
            /|
           e3 e4
             / |
            e5 e6
            |
            e7
        After:
            e1
             |
            e2
            /| \
           e3 e5 e6
              |
              e7
        """
        e1 = Employee(1, "A", "PositionA", 100, 10)
        e2 = Employee(2, "B", "PositionB", 100, 20)
        e3 = Employee(3, "C", "PositionC", 100, 30)
        e4 = Employee(4, "D", "PositionD", 100, 40)
        e5 = Employee(5, "E", "PositionE", 100, 50)
        e6 = Employee(6, "F", "PositionF", 100, 60)
        e7 = Employee(7, "G", "PositionG", 100, 70)
        e2.become_subordinate(e1)
        e3.become_subordinate(e2)
        e4.become_subordinate(e2)
        e5.become_subordinate(e4)
        e6.become_subordinate(e4)
        e7.become_subordinate(e5)
        org = Organization(e1)
        org.fire_employee(e4.eid)
        self.assertIsNone(org.get_employee(e4.eid))
        act = org.get_head()
        self.assertTrue(act.eid == 1, "e1 should remain as the head")
        self.assertTrue(len(act.get_direct_subordinates()) == 1, "e2 should still under e1")
        new_e2 = act.get_direct_subordinates()[0]
        self.assertTrue(len(new_e2.get_direct_subordinates()) == 3, "You should move e5 and e6 under e2")
        self.assertListEqual([temp.eid for temp in new_e2.get_direct_subordinates()], [3, 5, 6],
                             "Now e6 and e7 should be the children under e2")

    def test_fire_head(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e3
             | | \
          e2 e4 e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_employee(self.e1.eid)
        self.assertIsNone(org.get_employee(self.e1.eid))
        act = org.get_head()
        self.assertTrue(act.eid == 3, "e3 should be the new head")
        self.assertTrue(len(act.get_direct_subordinates()) == 3)
        self.assertListEqual([temp.eid for temp in act.get_direct_subordinates()], [2, 4, 5],
                             "This is the correct order of the children under e3")


class TestFireLowest(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def test_fire_lowest_single(self):
        org = Organization(self.e1)
        org.fire_lowest_rated_employee()
        self.assertIsNone(org.get_head())

    def test_fire_lowest(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e3
             | | \
          e2 e4 e5
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_lowest_rated_employee()
        self.assertIsNone(org.get_employee(self.e1.eid))
        act = org.get_head()
        self.assertTrue(act.eid == 3, "e3 should be the new head")
        self.assertTrue(len(act.get_direct_subordinates()) == 3)
        self.assertListEqual([temp.eid for temp in act.get_direct_subordinates()], [2, 4, 5],
                             "This is the correct order of the children under e3")

    def test_fire_lowest2(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e1
             | | \
          e2 e4 e5
        """
        self.e1.rating = 30
        self.e3.rating = 10
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_lowest_rated_employee()
        self.assertIsNone(org.get_employee(self.e3.eid), "You should not have e3 in the organization")
        self.assertTrue(len(org.get_head().get_direct_subordinates()) == 3,
                        "You should obtain e4 and e5 as e1's direct children")
        self.assertListEqual([temp.eid for temp in org.get_head().get_direct_subordinates()], [2, 4, 5])

    def test_fire_lowest3(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e1
             | | \
          e2 e4 e5
        """
        self.e1.rating = 30
        self.e3.rating = 10
        self.e4.rating = 10
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_lowest_rated_employee()
        self.assertIsNone(org.get_employee(self.e3.eid), "You should not have e3 in the organization")
        self.assertTrue(len(org.get_head().get_direct_subordinates()) == 3,
                        "You should obtain e4 and e5 as e1's direct children")
        self.assertListEqual([temp.eid for temp in org.get_head().get_direct_subordinates()], [2, 4, 5])

    def test_fire_lowest4(self):
        """
        Before:
                     e1
                    / \
                   e2  e3
                       /\
                    e4  e5
        After:
              e1
             / \
            e2  e3
                |
                e5
        """
        self.e1.rating = 30
        self.e4.rating = 10
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_lowest_rated_employee()
        self.assertIsNone(org.get_employee(self.e4.eid), "You should not have e4 in the organization")
        self.assertTrue(len(org.get_head().get_direct_subordinates()) == 2,
                        "You should obtain e4 and e5 as e1's direct children")
        self.assertListEqual([temp.eid for temp in org.get_head().get_direct_subordinates()], [2, 3])
        new_e3 = org.get_head().get_direct_subordinates()[1]
        self.assertTrue(len(new_e3.get_direct_subordinates()) == 1)
        self.assertTrue(employee_eq(new_e3.get_direct_subordinates()[0], self.e5))

    def test_fire_lowest5(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e2)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e4)
        org = Organization(self.e1)
        for i in range(1, 7):
            if i == 6:
                self.assertIsNone(org.get_head())
            else:
                org.fire_lowest_rated_employee()
                self.assertIsNone(org.get_employee(i))


class TestFireUnderRating(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def tearDown(self) -> None:
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e2 = Employee(2, "B", "PositionB", 100, 20)
        self.e3 = Employee(3, "C", "PositionC", 100, 30)
        self.e4 = Employee(4, "D", "PositionD", 100, 40)
        self.e5 = Employee(5, "E", "PositionE", 100, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def test_single(self):
        org = Organization(self.e1)
        org.fire_under_rating(100)
        self.assertIsNone(org.get_head())

    def test_fire_none(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_under_rating(10)
        head = org.get_head()
        self.assertTrue(head.eid == 1, "The head should remain as e1")
        children = head.get_direct_subordinates()
        self.assertTrue(len(children) == 2 and [temp.eid for temp in children] == [2, 3])
        e2 = children[0]
        self.assertTrue(e2.get_direct_subordinates() == [])
        e3 = children[1]
        e3_children = e3.get_direct_subordinates()
        self.assertTrue(len(e3_children) == 2 and [temp.eid for temp in e3_children] == [4, 5])

    def test_fire_all(self):
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e3)
        org = Organization(self.e1)
        org.fire_under_rating(100)
        head = org.get_head()
        self.assertIsNone(head)


class TestSwap(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "Company")
        self.e2 = Employee(2, "B", "PositionB", 200, 20)
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e4 = Employee(4, "D", "PositionD", 400, 40)
        self.e5 = Employee(5, "E", "PositionE", 500, 50)
        def assertFun(employee, data, checkLeader):
            eid, name, position, salary, rating, department = data[0], data[1], data[2], data[3], data[4], data[5]
            self.assertEqual(eid, employee.eid)
            self.assertEqual(name, employee.name)
            self.assertEqual(position, employee.position)
            self.assertEqual(salary, employee.salary)
            self.assertEqual(rating, employee.rating)
            self.assertEqual(checkLeader, isinstance(employee, Leader))
            self.assertEqual(department, employee.get_department_name())
        self.assertFun = assertFun
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def tearDown(self) -> None:
        self.e1 = Leader(1, "A", "PositionA", 100, 10, "Company")
        self.e2 = Employee(2, "B", "PositionB", 200, 20)
        self.e3 = Employee(3, "C", "PositionC", 300, 30)
        self.e4 = Employee(4, "D", "PositionD", 400, 40)
        self.e5 = Employee(5, "E", "PositionE", 500, 50)
        self.employees = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def test_basic(self):
        """
        Before:
            e2(2, B, PositionB, 100, 20, Company)
            |
            e1(1, A, PositionA, 100, 10)
        After:
            e2(2, B, PositionB, 100, 20, Company)
            |
            e1(1, A, PositionA, 100, 10)
        """
        self.e2 = Leader(2, "B", "PositionB", 100, 20, "Company")
        self.e1 = Employee(1, "A", "PositionA", 100, 10)
        self.e1.become_subordinate(self.e2)
        o = Organization(self.e2)
        o.promote_employee(self.e1.eid)
        head = o.get_head()
        self.assertFun(head, [2, "B", "PositionB", 100, 20, "Company"], True)
        self.assertEqual(1, len(head.get_direct_subordinates()))
        first_child = head.get_direct_subordinates()[0]
        self.assertFun(first_child, [1, "A", "PositionA", 100, 10, "Company"], False)
        self.assertEqual([], first_child.get_direct_subordinates())

    def test_linear(self):
        """
        Before:
            e1(1, A, PositionA, 100, 20, "Company")
            |
            e2(2, B, PositionB, 200, 20)
        After:
            e2(2, B, PositionA, 100, 20, "Company")
            |
            e1(1, A, PositionB, 200, 20)
        """
        self.e1.rating = 20
        self.e2.become_subordinate(self.e1)
        org = Organization(self.e1)
        org.promote_employee(self.e2.eid)
        head = org.get_head()
        self.assertFun(head, [2, "B", "PositionA", 100, 20, "Company"], True)
        self.assertEqual(1, len(head.get_direct_subordinates()))
        first_child = head.get_direct_subordinates()[0]
        self.assertFun(first_child, [1, "A", "PositionB", 200, 20, "Company"], False)
        self.assertEqual([], first_child.get_direct_subordinates())

    def test_linear2(self):
        """
        Before:
            e1(1, A, PositionA, 100, 10, "Company")
            |
            e2(2, B, PositionB, 200, 20)
            |
            e3(3, C, PositionC, 300, 30)
        After:
            e3(3, C, PositionA, 100, 30, "Company")
            |
            e1(1, A, PositionB, 200, 10)
            |
            e2(2, B, PositionC, 300, 20)
        """
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        org = Organization(self.e1)
        org.promote_employee(self.e3.eid)
        head = org.get_head()
        self.assertFun(head, [3, "C", "PositionA", 100, 30, "Company"], True)
        self.assertEqual(len(head.get_direct_subordinates()), 1)
        first_child = head.get_direct_subordinates()[0]
        self.assertFun(first_child, [1, "A", "PositionB", 200, 10, "Company"], False)
        self.assertEqual(1, len(first_child.get_direct_subordinates()))
        second_child = first_child.get_direct_subordinates()[0]
        self.assertFun(second_child, [2, "B", "PositionC", 300, 20, "Company"], False)
        self.assertEqual([], second_child.get_direct_subordinates())

    def test_linear3(self):
        """
        Before:
            e1(1, A, PositionA, 100, 30, "Company")
            |
            e2(2, B, PositionB, 200, 20)
            |
            e3(3, C, PositionC, 300, 30)
        After:
            e1(1, A, PositionA, 100, 30, "Company")
            |
            e3(3, C, PositionB, 200, 30)
            |
            e2(2, B, PositionC, 300, 20)
        """
        self.e1.rating = 40
        self.e3.become_subordinate(self.e2)
        self.e2.become_subordinate(self.e1)
        org = Organization(self.e1)
        org.promote_employee(self.e3.eid)
        head = org.get_head()
        self.assertFun(head, [1, "A", "PositionA", 100, 40, "Company"], True)
        self.assertEqual(1, len(head.get_direct_subordinates()))
        first_child = head.get_direct_subordinates()[0]
        self.assertFun(first_child, [3, "C", "PositionB", 200, 30, "Company"], False)
        self.assertEqual(1, len(first_child.get_direct_subordinates()))
        second_child = first_child.get_direct_subordinates()[0]
        self.assertFun(second_child, [2, "B", "PositionC", 300, 20, "Company"], False)
        self.assertEqual([], second_child.get_direct_subordinates())

    def test_child(self):
        """
        Before:
            e1(1, A, PositionA, 100, 10, "Company")
            /   |
        e2(2, B, PositionB, 200, 20)  e3(3, C, PositionC, 300, 300, 30)
        After:
        e2(2, B, PositionA, 100, 20, "Company")
            /   |
        e1(1, A, PositionB, 200, 10)  e3(3, C, PositionC, 300, 300, 30)
        """
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        org = Organization(self.e1)
        org.promote_employee(self.e2.eid)
        head = org.get_head()
        self.assertFun(head, [2, "B", "PositionA", 100, 20, "Company"], True)
        self.assertEqual(len(head.get_direct_subordinates()), 2)
        first_child = head.get_direct_subordinates()[0]
        self.assertFun(first_child, [1, "A", "PositionB", 200, 10, "Company"], False)
        self.assertEqual(0, len(first_child.get_direct_subordinates()))
        second_child = head.get_direct_subordinates()[1]
        self.assertFun(second_child, [3, "C", "PositionC", 300, 30, "Company"], False)
        self.assertEqual([], second_child.get_direct_subordinates())

    def test_child2(self):
        """
        Before:
                e1(1, A, PositionA, 100, 60, Company)
        /                               |
        e2(2, B, PositionB, 200, 20)  e3(3, C, PositionC, 300, 50, Deparment)
                                        |
                                        e4(4, D, PositionD, 400, 40, SubDepartment)
                                        /                           |
                                    e5(5, E, PositionE, 500, 50)  e6(6, F, PositionF, 600, 60)
        After:
            e1(1, A, PositionA, 100, 50, Company)
        /                               |
        e2(2, B, PositionB, 200, 20)  e5(5, E, PositionC, 300, 50, Deparment)
                                        |
                                        e3(3, C, PositionD, 400, 30, SubDepartment)
                                        /                       \
                                e4(4, D, PositionE, 500, 40)    e6(6, F, PositionF, 600, 60)
        """
        self.e1.rating = 60
        self.e3 = Leader(3, "C", "PositionC", 300, 30, "Department")
        self.e4 = Leader(4, "D", "PositionD", 400, 40, "SubDepartment")
        self.e2.become_subordinate(self.e1)
        self.e3.become_subordinate(self.e1)
        self.e4.become_subordinate(self.e3)
        self.e5.become_subordinate(self.e4)
        e6 = Employee(6, "F", "PositionF", 600, 60)
        e6.become_subordinate(self.e4)
        org = Organization(self.e1)
        org.promote_employee(self.e5.eid)
        head = org.get_head()
        self.assertFun(head, [1, "A", "PositionA", 100, 60, "Company"], True)
        children = head.get_direct_subordinates()
        self.assertEqual(2, len(children))
        self.assertFun(children[0], [2, "B", "PositionB", 200, 20, "Company"], False)
        self.assertFun(children[1], [5, "E", "PositionC", 300, 50, "Department"], True)
        e5_child = children[1].get_direct_subordinates()
        self.assertFun(e5_child[0], [3, "C", "PositionD", 400, 30, "SubDepartment"], True)
        self.assertTrue(len(e5_child) == 1)
        e3_child = e5_child[0].get_direct_subordinates()
        self.assertTrue(len(e3_child) == 2)
        self.assertFun(e3_child[0], [4, "D", "PositionE", 500, 40, "SubDepartment"], False)
        self.assertFun(e3_child[1], [6, "F", "PositionF", 600, 60, "SubDepartment"], False)
        self.assertTrue(len(e3_child[0].get_direct_subordinates()) == 0)
        self.assertTrue(len(e3_child[1].get_direct_subordinates()) == 0)

    def test_handout(self):
        """
        Before:
                e1(1, Alice, CEO, 250000, 20, Some Corp)
                |
                e2(10, Holly, Head, 46000, 50, "Tech")
                |
                e3(12, Ivan, PM, 50000, 60)
                /                                   \
            e4(11, Joe, Programmer, 60000, 90)      e5 (13, Kevin, Programmer, 40000, 80)
        After:
                e4(11, Joe, CEO, 250000, 90, Some Corp)
                |
                e1(1, Alice, Head, 46000, 20, "Tech")
                |
                e2(10, Holly, PM, 50000, 50)
                /                                   \
            e3(12, Ivan, Programmer, 60000, 60)      e5 (13, Kevin, Programmer, 40000, 80)
        """
        e1 = Leader(1, "Alice", "CEO", 250000, 20, "Some Corp")
        e2 = Leader(10, "Holly", "Head", 46000, 50, "Tech")
        e3 = Employee(12, "Ivan", "PM", 50000, 60)
        e4 = Employee(11, "Joe", "Programmer", 60000, 90)
        e5 = Employee(13, "Kevin", "Programmer", 40000, 80)
        e2.become_subordinate(e1)
        e3.become_subordinate(e2)
        e4.become_subordinate(e3)
        e5.become_subordinate(e3)
        org = Organization(e1)
        org.promote_employee(e4.eid)
        head = org.get_head()
        self.assertTrue(head.eid == 11)
        self.assertFun(head, [11, "Joe", "CEO", 250000, 90, "Some Corp"], True)
        e4_child = head.get_direct_subordinates()
        self.assertTrue(len(e4_child) == 1)
        self.assertFun(e4_child[0], [1, "Alice", "Head", 46000, 20, "Tech"], True)
        e1_child = e4_child[0].get_direct_subordinates()
        self.assertTrue(len(e1_child) == 1)
        self.assertFun(e1_child[0], [10, "Holly", "PM", 50000, 50, "Tech"], False)
        e2_child = e1_child[0].get_direct_subordinates()
        self.assertTrue(len(e2_child) == 2)
        self.assertFun(e2_child[0], [12, "Ivan", "Programmer", 60000, 60, "Tech"], False)
        self.assertFun(e2_child[1], [13, "Kevin", "Programmer", 40000, 80, "Tech"], False)
        self.assertTrue(len(e2_child[0].get_direct_subordinates()) == 0)
        self.assertTrue(len(e2_child[1].get_direct_subordinates()) == 0)


if __name__ == '__main__':
    unittest.main()
