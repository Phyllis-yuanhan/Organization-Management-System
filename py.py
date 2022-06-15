"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO

# TODO: === TASK 1 ===
# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([1, 3, 10], [2, 9, 12])
    [1, 2, 3, 9, 10, 12]
    >>> merge([1], [0])
    [0, 1]
    >>> merge([1, 3, 10], [2, 9, 12, 100])
    [1, 2, 3, 9, 10, 12, 100]
    >>> merge([1], [0, 2, 4])
    [0, 1, 2, 4]
    """
    a_lst = []
    lst = lst1 + lst2
    while len(lst) != 0:
        a_lst.append(lst.pop(lst.index(min(lst))))
    return a_lst

    # TODO Task 1: Complete the merge() function.


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []
        # TODO Task 1: Complete the __init__ method.

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        if isinstance(other, Employee):
            return self.eid < other.eid
        else:
            return False
        # TODO Task 1: Complete the __lt__ method.

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        return self._subordinates
        # TODO Task 1: Complete the get_direct_subordinates method.

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        if len(self.get_direct_subordinates()) == 0:
            return []
        else:
            lst = []
            for employees in self.get_direct_subordinates():
                new = employees.get_all_subordinates()
                lst = merge(lst, new)
            return merge(lst, self.get_direct_subordinates())

        # TODO Task 1: Complete the get_all_subordinates method.

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        if self.get_superior() is None:
            return self
        else:
            boss = self.get_superior().get_organization_head()
            return boss
        # TODO Task 1: Complete the get_organization_head method.

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        return self._superior
        # TODO Task 1: Complete the get_superior method.

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        if superior is None:
            if self._superior is not None:
                self._superior._subordinates.remove(self)
                self._superior = None
        else:
            if self._superior is not None:
                self._superior.remove_subordinate_id(self.eid)
            self._superior = superior
            self._superior._subordinates = merge([self],
                                                 self._superior._subordinates)

        # TODO Task 1: Complete the become_subordinate method.

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e3.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> len(e2.get_direct_subordinates()) == 1
        True
        >>> e1.get_superior() is e2
        True
        """
        employee = self.get_employee(eid)
        self._subordinates.remove(employee)

        # TODO Task 1: Complete the remove_subordinate_id method.

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        self._subordinates.append(subordinate)
        # TODO Task 1: Complete the add_subordinate method.

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        if self.eid == eid:
            return self
        else:
            employee = None
            for item in self.get_all_subordinates():
                if item.eid == eid:
                    employee = item
            return employee
        # TODO Task 1: Complete the get_employee method.

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        lst = []
        for people in self.get_all_subordinates():
            if people.salary > amount:
                lst = merge(lst, [people])
        if self.salary > amount:
            lst = merge(lst, [self])
        return lst
        # TODO Task 1: Complete the get_employees_paid_more_than method.

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1. Write their headers and bodies below.
    def get_closest_common_superior(self, eid: int) -> Optional[Employee]:
        """Return the closest common superior of self and employee with the
        given <eid>
        If one of the two employees is the superior of the other one, return the
        superior.
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "p", "Worker", 20000, 60)
        >>> e1.become_subordinate(e2)
        >>> e4.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e2.get_closest_common_superior(1) is e2
        True
        >>> e3.get_closest_common_superior(1) is e3
        True
        >>> e1.get_closest_common_superior(4) is e2
        True
        """
        e1 = self.get_organization_head().get_employee(eid)
        if self in e1.get_all_subordinates():
            return e1
        elif e1 in self.get_all_subordinates():
            return self
        else:
            head = self.get_superior()
            while e1 not in head.get_all_subordinates():
                head = head.get_superior()
            return head

    def get_higher_paid_employees(self) -> List[Employee]:
        """Get a list of Employees that have a higher salary than this Employee
        in this Employee's organization.
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        >>> e1.get_higher_paid_employees() == more_than_10000
        True
        """
        the_head = self.get_organization_head()
        return the_head.get_employees_paid_more_than(self.salary)

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        >>> e2.get_department_name()
        'Department'
        """
        if isinstance(self, Leader):
            raise NotImplementedError
        else:
            if self._superior is not None:
                return self._superior.get_department_name()
            else:
                return ''
        # TODO Task 2: Complete the get_department_name method.

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department'
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        string = self.position
        head = self._superior
        if isinstance(self, Leader):
            string += ', ' + self.get_department_name()
        if head is None:
            return string
        else:
            while head != self.get_organization_head():
                if head.get_department_name() != '':
                    string += ', ' + head.get_department_name()
                head = head._superior
            if isinstance(self.get_organization_head(), Leader):
                string += ', ' + self.get_organization_head().\
                    get_department_name()
            return string

        # TODO Task 2: Complete the get_position_in_hierarchy method.

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        if self.get_department_name() == '':
            return None
        if isinstance(self, Leader):
            return self
        else:
            return self._superior.get_department_leader()
        # TODO Task 3: Complete the get_department_leader method.

    def change_department_leader(self) -> Optional[Leader]:
        """Make self the leader of the department
        nothing happens if this employee does not belong to any department
        or he is a leader
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.change_department_leader().name
        'Bigg Boss'
        """
        if self.get_department_name() == '':
            return None
        elif isinstance(self, Leader):
            return self
        else:
            l1 = Leader(self.eid, self.name, self.position, self.salary,
                        self.rating, self.get_department_name())
            old = self.get_department_leader()
            old_superior = old._superior
            if old_superior is not None:
                old_superior.remove_subordinate_id(old.eid)
            l1.become_subordinate(old_superior)
            l2 = Employee(old.eid, old.name, old.position,
                          old.salary, old.rating)
            if self._superior == old:
                old.remove_subordinate_id(self.eid)
            else:
                self._superior.remove_subordinate_id(self.eid)
            lst1 = []
            for x in old._subordinates:
                lst1.append(x)
            for a in lst1:
                a.become_subordinate(l2)
            lst = []
            for i in self._subordinates:
                lst.append(i)
            for e in lst:
                e.become_subordinate(l1)
            l2.become_subordinate(l1)

            return l1.get_organization_head()

    def become_leader(self, department_name: str) -> Leader:
        """Create a new department and let this employee (or leader) be the
        leader of this new department
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.become_leader('lll').get_department_name()
        'lll'
        """
        if isinstance(self, Leader):
            raise NotImplementedError
        else:
            l1 = Leader(self.eid, self.name, self.position, self.salary,
                        self.rating, department_name)
            for i in self._subordinates:
                i.become_subordinate(l1)
            l1.become_subordinate(self._superior)
            return l1

    def become_employee(self) -> Employee:
        """Make this Leader no longer a leader instead of an Employee
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e2.become_employee().get_department_name()
        'Company'
        >>> e1.get_department_name()
        'Company'
        """
        e1 = Employee(self.eid, self.name, self.position,
                      self.salary, self.rating)
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
        lst = []
        for i in self.get_direct_subordinates():
            lst.append(i)
        for a in lst:
            a.become_subordinate(e1)
        e1.become_subordinate(self._superior)
        return e1

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 3.

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        lst1 = self.get_direct_subordinates()
        lst2 = []
        for e in lst1:
            lst2.append(e.rating)
        return lst1[lst2.index(max(lst2))]

        # TODO Task 4: Complete the get_highest_rated_subordinate method.

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        if not isinstance(self, Leader) and isinstance(self._superior, Leader):
            new_leader = Leader(self.eid, self.name, self._superior.position,
                                self._superior.salary, self.rating,
                                self.get_department_name())
            new_sub = Employee(self._superior.eid, self._superior.name,
                               self.position, self.salary,
                               self._superior.rating)

        elif not isinstance(self, Leader) and not\
                isinstance(self._superior, Leader):
            new_leader = Employee(self.eid, self.name, self._superior.position,
                                  self._superior.salary, self.rating)
            new_sub = Employee(self._superior.eid, self._superior.name,
                               self.position, self.salary,
                               self._superior.rating)

        elif isinstance(self, Leader) and isinstance(self._superior, Leader):
            new_leader = Leader(self.eid, self.name, self._superior.position,
                                self._superior.salary, self.rating,
                                self._superior.get_department_name())
            new_sub = Leader(self._superior.eid, self._superior.name,
                             self.position, self.salary,
                             self._superior.rating, self.get_department_name())

        else:
            # isinstance(self, Leader) and isinstance(self._superior, Employee)
            new_leader = Employee(self.eid, self.name, self._superior.position,
                                  self._superior.salary, self.rating)
            new_sub = Leader(self._superior.eid, self._superior.name,
                             self.position, self.salary,
                             self._superior.rating, self.get_department_name())
        new_sub.become_subordinate(new_leader)
        new_leader.become_subordinate(self._superior._superior)
        lst = []
        for x in self._subordinates:
            lst.append(x)
        for i in lst:
            i.become_subordinate(new_sub)
        self._superior.remove_subordinate_id(self.eid)
        ll = []
        for b in self._superior.get_direct_subordinates():
            ll.append(b)
        for a in ll:
            a.become_subordinate(new_leader)
        if self._superior._superior is not None:
            self._superior._superior.remove_subordinate_id(self._superior.eid)
        return new_leader

        # TODO Task 4: Complete the swap_up method.

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 4.
    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """Set the employees with IDs in ids as subordinates of self.

        If those employees have subordinates, the superior of those subordinates
        becomes the employee's original superior.

        Pre-condition: self's id is not in ids.
        """
        if not ids:
            return self.get_organization_head()
        for i in ids:
            if self.get_organization_head().eid == i:
                employee = self.get_organization_head()
                new_head = employee.get_highest_rated_subordinate()
                new_head._superior = None
                lst = []
                for a in employee.get_direct_subordinates():
                    lst.append(a)
                lst.remove(new_head)
                for ppl in lst:
                    ppl.become_subordinate(new_head)
                employee.become_subordinate(self)
                employee._subordinates = []
            else:
                employee1 = self.get_organization_head().get_employee(i)
                lst = []
                for a in employee1.get_direct_subordinates():
                    lst.append(a)
                for ppl in lst:
                    ppl.become_subordinate(employee1._superior)
                employee1.become_subordinate(self)
                employee1._subordinates = []
        return self.get_organization_head()


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        if head is None:
            self._head = None
        else:
            self._head = head
        # TODO Task 1: Complete the __init__ method.

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        if self._head is None:
            return None
        elif eid == self._head.eid:
            return self._head
        else:
            for people in self._head.get_all_subordinates():
                if people.eid == eid:
                    return people
            return None
        # TODO Task 1: Complete the get_employee method.

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        if superior_id is None:
            if self._head is None:
                self._head = employee
            else:
                self._head.become_subordinate(employee)
                self._head = employee
        elif superior_id == self._head.eid:
            employee.become_subordinate(self._head)
        else:
            ppl = self._head.get_employee(superior_id)
            if ppl is not None:
                employee.become_subordinate(ppl)
        # TODO Task 1: Complete the add_employee method.

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        >>> o.get_average_salary("a")
        0
        """
        if self._head is None:
            return 0
        if position is None:
            total = self._head.salary
            for ppl in self._head.get_all_subordinates():
                total += ppl.salary
            return total/(len(self._head.get_all_subordinates()) + 1)
        else:
            if self._head.position == position:
                total = self._head.salary
                number = 1
            else:
                total = 0
                number = 0
            for ppl in self._head.get_all_subordinates():
                if ppl.position == position:
                    total += ppl.salary
                    number += 1
            if total == 0:
                return 0
            else:
                return total / number
        # TODO Task 1: Complete the get_average_salary method.

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1.

    def get_next_free_id(self) -> int:
        """Return the next free id number.
        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.add_employee(e3, 2)
        >>> o.get_next_free_id()
        4
        """
        if self._head is None:
            return 1
        else:
            all_id = [self._head.eid]
            all_employee = self._head.get_all_subordinates()
            for people in all_employee:
                all_id = merge(all_id, [people.eid])
            idd = 1
            while idd in all_id:
                idd += 1
            return idd

    def get_employees_with_position(self, position: str) -> List[Employee]:
        """Return a list of employees with the position named <position>
        in order of increasing eid.
        >>> o = Organization()
        >>> e1 = Employee(3, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Employee(1, "Bigg Boss", "Worker", 10000, 60)
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.add_employee(e3, 2)
        >>> o.get_employees_with_position("Worker")[0].name
        'Bigg Boss'
        >>> o.get_employees_with_position("Worker")[1].name
        'Emma Ployee'
        """
        if self._head is None:
            return []
        else:
            lst = []
            for people in self._head.get_all_subordinates():
                if people.position == position:
                    lst = merge(lst, [people])
            if self._head.position == position:
                return merge(lst, [self._head])
            else:
                return lst

    def get_head(self) -> Optional[Employee]:
        """Return the head of this organization.
        >>> o = Organization()
        >>> o.get_head() is None
        True
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_head() is e1
        True
        """
        return self._head

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3.
    def set_head(self, employee: Employee = None) -> None:
        """Let the employee become the head of this organization.
        """
        if employee is None:
            self._head = None
        else:
            self._head = employee
            employee.become_subordinate(None)

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4.
    def fire_employee(self, eid: int) -> None:
        """Fire the employee with ID eid from self.current_organization.

        Pre-condition: there is an employee with the eid <eid> in
        this organization.
        """
        employee = self.get_employee(eid)
        if employee.get_superior() is None:
            if not employee.get_direct_subordinates():
                self.set_head()
            else:
                x = employee.get_highest_rated_subordinate()
                self.set_head(x)
                lst = []
                for i in employee.get_direct_subordinates():
                    lst.append(i)
                for a in lst:
                    a.become_subordinate(x)
        else:
            lst = []
            for i in employee.get_direct_subordinates():
                lst.append(i.eid)
            employee.get_superior().obtain_subordinates(lst)
            employee.get_superior().remove_subordinate_id(eid)

    def fire_lowest_rated_employee(self) -> None:
        """Fire the lowest rated employee in this organization.

        If two employees have the same rating, the one with the lowest id
        is fired.
        """
        # employee = self._head
        # head_rating = self._head.rating
        # for i in self._head.get_all_subordinates():
        #     rate = i.rating
        #     if rate < head_rating:
        #         head_rating = rate
        #         employee = i
        #     elif rate == head_rating:
        #         if i.eid < self._head.eid:
        #             employee = i
        #     else:
        #         pass
        # self.fire_employee(employee.eid)
        lst = merge([self.get_head()], self.get_head().get_all_subordinates())
        lst1 = []
        for i in lst:
            lst1.append(i.rating)
        eid = lst[lst1.index(min(lst1))].eid
        self.fire_employee(eid)

    def fire_under_rating(self, rating: int) -> None:
        """Fire all employees with a rating below rating.

        Employees should be fired in order of increasing rating: the lowest
        rated employees are to be removed first. Break ties in order of eid.
        """

        lst = merge([self.get_head()], self.get_head().get_all_subordinates())
        lst1 = []
        for i in lst:
            lst1.append(i.rating)
        while len(lst1) != 0 and min(lst1) < rating:
            self.fire_lowest_rated_employee()
            lst1.remove(min(lst1))

    def promote_employee(self, eid: int) -> None:
        """Promote the employee with the eid <eid> in this organization
        until they have a superior with a higher rating than them or until they
        are the head of the organization.

        Precondition: There is an employee in this organization with
        eid <eid>.
        """
        employee = self.get_employee(eid)
        while employee.get_superior() is not None and employee.get_superior().\
                rating <= employee.rating:
            employee = employee.swap_up()
        if employee.get_superior() is None:
            self.set_head(employee)

# === TASK 2: Leader ===
# TODO: Complete the Leader class and its methods according to their docstrings.
#       You will also need to revisit Organization and Employee to implement
#       additional methods.
#       Go through client_code.py to find additional methods that you must
#       implement.
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

        # TODO Task 2: Complete the __init__ method.

    def get_department_employees(self) -> List[Employee]:
        """Return a list of employees in self's department.
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, 'department')
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_department_employees() == [e1, e2, e3]
        True
        """
        return merge(self.get_all_subordinates(), [self])

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    #       There may also be Employee methods that you'll need to override.
    def get_department_name(self) -> str:
        """Return the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.
        """
        return self._department_name
    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3. If there are no methods there, consider if you need to
    #       override any of the Task 3 Employee methods.

    def change_department(self, department_name: str) -> None:
        """Change self's department name.
        """
        self._department_name = department_name

    def become_leader(self, department_name: str) -> Leader:
        """Create a new department and let this leader be the leader of this new department
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.become_leader('lll').get_department_name()
        'lll'
        """
        self.change_department(department_name)
        return self
    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4. If there are no methods there, consider if you need to
    #       override any of the Task 4 Employee methods.


# === TASK 5 ===
# TODO: Complete the create_department_salary_tree() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    if not isinstance(organization.get_head(), Leader):
        return None
    head = organization.get_head()
    department = head.get_department_name()
    lst = []
    salary = head.salary
    for i in head.get_all_subordinates():
        if i.get_department_name() == department:
            lst.append(i)
            salary += i.salary
    average = salary / (len(lst) + 1)
    tree = DepartmentSalaryTree(department, average, [])

    leaders = []
    for i in head.get_direct_subordinates():
        leaders = merge(_find_closest_leader(i), leaders)
    for leader in leaders:
        new_or = Organization(leader)
        new_tree = create_department_salary_tree(new_or)
        if new_tree is not None:
            tree.subdepartments.append(new_tree)
    return tree
    # TODO Task 5: Complete the create_department_salary_tree function.


def _find_closest_leader(emp: Employee) -> List[Leader]:
    """Find the closest leader after emp.
    """
    if isinstance(emp, Leader):
        return [emp]
    else:
        lst = []
        for i in emp.get_direct_subordinates():
            lst = merge(_find_closest_leader(i), lst)
        return lst

# === TASK 6 ===
# TODO: Complete the create_organization_from_file() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    dic1 = {}
    dic2 = {}
    org = Organization()
    line = file.readline()
    while line != '':
        lst = line.split(',')
        if len(lst) == 7:
            eid = int(lst[0])
            salary = int(lst[3])
            rating = int(lst[4])
            superior_id = lst[5]
            ll = Leader(eid, lst[1], lst[2], salary, rating, lst[6])
            if superior_id == '':
                org.add_employee(ll)
            elif superior_id != '' and int(superior_id) not in dic1:
                dic1[int(superior_id)] = [ll]
                dic2[eid] = ll
            elif superior_id != '' and int(superior_id) in dic1:
                dic1[int(superior_id)].append(ll)
                dic2[eid] = ll
        else:
            eid = int(lst[0])
            salary = int(lst[3])
            rating = int(lst[4])
            superior_id = lst[5]
            ee = Employee(eid, lst[1], lst[2], salary, rating)
            if superior_id == '':
                org.add_employee(ee)
            elif superior_id != '' and int(superior_id) not in dic1:
                dic1[int(superior_id)] = [ee]
                dic2[eid] = ee
            elif superior_id != '' and int(superior_id) in dic1:
                dic1[int(superior_id)].append(ee)
                dic2[eid] = ee
        line = file.readline()
    dic2[org.get_head().eid] = org.get_head()
    for i in dic1:
        for item in dic1[i]:
            item.become_subordinate(dic2[i])
    return org

    # TODO Task 6: Complete the create_organization_from_file function.


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
