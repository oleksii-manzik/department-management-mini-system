import unittest
from flask import url_for

from dmms.rest.app import app
from dmms.service.db import db
from dmms.models.model import DepartmentsModel, EmployeesModel


class DepartmentsRestTest(unittest.TestCase):
    """Test Departments API"""
    def setUp(self):
        """Create and fill test tables"""
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        test_department1 = DepartmentsModel(name='Test1')
        test_department2 = DepartmentsModel(name='Test2')
        test_department3 = DepartmentsModel(name='Test3')
        db.session.add_all([test_department1, test_department2,
                            test_department3])
        db.session.commit()

    def tearDown(self):
        """Drop test tables"""
        db.session.remove()
        db.drop_all()

    def test_get_all_departments(self):
        response = app.test_client().get(url_for('departments'))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = [{'id': 1, 'name': 'Test1', 'employees': []},
                              {'id': 2, 'name': 'Test2', 'employees': []},
                              {'id': 3, 'name': 'Test3', 'employees': []}]
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

    def test_get_many_departments(self):
        response = app.test_client().get(
            url_for('departments'), query_string={'id': ['1', '3']})

        actual_result = response.json
        expected_result = [{'id': 1, 'name': 'Test1', 'employees': []},
                           {'id': 3, 'name': 'Test3', 'employees': []}]
        self.assertEqual(actual_result, expected_result)

    def test_get_wrong_url_departments(self):
        response = app.test_client().get(
            url_for('departments', department_id=42))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Page not found'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_post_departments(self):
        response = app.test_client().post(
            url_for('departments'),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test4"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = 'New department Test4 with id 4 was added'
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 201
            self.assertEqual(actual_code, expected_code)

        with self.subTest(name='test_if_really_was_posted'):
            response_was = app.test_client().get(
                url_for('departments'), query_string={'id': ['4']})
            actual_was = response_was.json
            expected_was = [{'id': 4, 'name': 'Test4', 'employees': []}]
            self.assertEqual(actual_was, expected_was)

    def test_post_wrong_url_departments(self):
        response = app.test_client().post(
            url_for('departments', department_id=42),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test4"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Page not found'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_post_all_parameters_is_filled_departments(self):
        response = app.test_client().post(
            url_for('departments'),
            headers={'Content-Type': 'application/json'},
            data='{}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {"message": "You haven't pass these "
                                         "parameters: ['name']"}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 400
            self.assertEqual(actual_code, expected_code)

    def test_put_departments(self):
        response = app.test_client().put(
            url_for('departments', department_id=3),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test3_Edited"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = "Department 3 was updated with data " \
                             "{'name': 'Test3_Edited'}"
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

        with self.subTest('test_if_really_was_updated'):
            response_was = app.test_client().get(
                url_for('departments'), query_string={'id': ['3']})
            actual_was = response_was.json
            expected_was = [{'id': 3, 'name': 'Test3_Edited', 'employees': []}]
            self.assertEqual(actual_was, expected_was)

    def test_put_value_provided_departments(self):
        response = app.test_client().put(
            url_for('departments'),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test3_Edited"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide id for updating'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_put_any_parameter_is_filled_departments(self):
        response = app.test_client().put(
            url_for('departments', department_id=3),
            headers={'Content-Type': 'application/json'},
            data='{}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide at least one '
                                         'value to update'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 400
            self.assertEqual(actual_code, expected_code)

    def test_put_item_exists_departments(self):
        response = app.test_client().put(
            url_for('departments', department_id=42),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test42_Edited"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {"message": "Department 42 doesn't exist"}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_delete_departments(self):
        response = app.test_client().delete(
            url_for('departments', department_id=3))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = 'Department 3 was successfully deleted'
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

        with self.subTest('test_if_really_was_deleted'):
            response_was = app.test_client().get(url_for('departments'))
            actual_was = response_was.json
            expected_was = [{'id': 1, 'name': 'Test1', 'employees': []},
                            {'id': 2, 'name': 'Test2', 'employees': []}]
            self.assertEqual(actual_was, expected_was)

    def test_delete_value_provided_departments(self):
        response = app.test_client().delete(url_for('departments'))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide id for deleting'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_delete_item_exists_departments(self):
        response = app.test_client().delete(
            url_for('departments', department_id=42))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {"message": "Department 42 doesn't exist"}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)


class EmployeesRestTest(unittest.TestCase):
    """Test Employees API"""

    def setUp(self):
        """Create and fill test tables"""
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        test_department1 = DepartmentsModel(name='Test1')
        test_department2 = DepartmentsModel(name='Test2')
        test_employee1 = EmployeesModel(name='Employee1',
                                        date_of_birth='1991-01-09',
                                        salary=2500,
                                        department_id=1)
        test_employee2 = EmployeesModel(name='Employee2',
                                        date_of_birth='1995-07-15',
                                        salary=1500,
                                        department_id=1)
        test_employee3 = EmployeesModel(name='Employee3',
                                        date_of_birth='1981-01-09',
                                        salary=2000,
                                        department_id=2)
        db.session.add_all([test_department1, test_department2,
                            test_employee1, test_employee2, test_employee3])
        db.session.commit()

    def tearDown(self):
        """Drop test tables"""
        db.session.remove()
        db.drop_all()

    def test_get_all_employees(self):
        response = app.test_client().get(url_for('employees'))
        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = [{'id': 1, 'name': 'Employee1',
                               'date_of_birth': '1991-01-09', 'salary': 2500,
                               'department_id': 1},
                              {'id': 2, 'name': 'Employee2',
                               'date_of_birth': '1995-07-15', 'salary': 1500,
                               'department_id': 1},
                              {'id': 3, 'name': 'Employee3',
                               'date_of_birth': '1981-01-09', 'salary': 2000,
                               'department_id': 2}]
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

    def test_get_many_employees(self):
        response = app.test_client().get(
            url_for('employees'), query_string={'id': ['1', '2']})

        actual_result = response.json
        expected_result = [{'id': 1, 'name': 'Employee1',
                            'date_of_birth': '1991-01-09', 'salary': 2500,
                            'department_id': 1},
                           {'id': 2, 'name': 'Employee2',
                            'date_of_birth': '1995-07-15', 'salary': 1500,
                            'department_id': 1}]
        self.assertEqual(actual_result, expected_result)

    def test_get_employees_by_birthday(self):
        with self.subTest('test_different_dates'):
            response_diff = app.test_client().get(
                url_for('employees'),
                query_string={'date_of_birth_start': '1990-01-01',
                              'date_of_birth_end': '2000-01-01'})
            actual_diff = response_diff.json
            expected_diff = [{'id': 1, 'name': 'Employee1',
                              'date_of_birth': '1991-01-09', 'salary': 2500,
                              'department_id': 1},
                             {'id': 2, 'name': 'Employee2',
                              'date_of_birth': '1995-07-15', 'salary': 1500,
                              'department_id': 1}]
            self.assertEqual(actual_diff, expected_diff)

        with self.subTest('test_same_dates'):
            response_same = app.test_client().get(
                url_for('employees'),
                query_string={'date_of_birth_start': '1991-01-09',
                              'date_of_birth_end': '1991-01-09'})
            actual_same = response_same.json
            expected_same = [{'id': 1, 'name': 'Employee1',
                              'date_of_birth': '1991-01-09', 'salary': 2500,
                              'department_id': 1}]
            self.assertEqual(actual_same, expected_same)

    def test_get_wrong_url_employees(self):
        response = app.test_client().get(
            url_for('employees', employee_id=42))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Page not found'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_post_employees(self):
        response = app.test_client().post(
            url_for('employees'),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Employee4", "date_of_birth":"1996-04-05", '
                 '"salary":1000, "department_id": 2}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = 'New employee Employee4 with id 4 was added'
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 201
            self.assertEqual(actual_code, expected_code)

        with self.subTest(name='test_if_really_was_posted'):
            response_was = app.test_client().get(
                url_for('employees'), query_string={'id': ['4']})
            actual_was = response_was.json
            expected_was = [{'id': 4, 'name': 'Employee4',
                             'date_of_birth': '1996-04-05', 'salary': 1000,
                             'department_id': 2}]
            self.assertEqual(actual_was, expected_was)

    def test_post_wrong_url_employees(self):
        response = app.test_client().post(
            url_for('employees', employee_id=42),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Employee4", "date_of_birth":"1996-04-05", '
                 '"salary":1000, "department_id": 2}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Page not found'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_post_all_parameters_is_filled_employees(self):
        response = app.test_client().post(
            url_for('employees'),
            headers={'Content-Type': 'application/json'},
            data='{}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            message_text = "You haven't pass these parameters: ['name', " \
                           "'date_of_birth', 'salary', 'department_id']"
            expected_value = {"message": message_text}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 400
            self.assertEqual(actual_code, expected_code)

    def test_post_salary_is_positive_employees(self):
        response = app.test_client().post(
            url_for('employees'),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Employee4", "date_of_birth":"1996-04-05", '
                 '"salary":-1000, "department_id": 2}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide higher then zero '
                                         'value for salary'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_put_employees(self):
        response = app.test_client().put(
            url_for('employees', employee_id=3),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Employee3_Edited", "salary": 999}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = "Employee 3 was updated with data " \
                             "{'name': 'Employee3_Edited', 'salary': 999.0}"
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

        with self.subTest('test_if_really_was_updated'):
            response_was = app.test_client().get(
                url_for('employees'), query_string={'id': ['3']})
            actual_was = response_was.json
            expected_was = [{'id': 3, 'name': 'Employee3_Edited',
                             'date_of_birth': '1981-01-09', 'salary': 999,
                             'department_id': 2}]
            self.assertEqual(actual_was, expected_was)

    def test_put_value_provided_employees(self):
        response = app.test_client().put(
            url_for('employees'),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Employee3_Edited"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide id for updating'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_put_any_parameter_is_filled_employees(self):
        response = app.test_client().put(
            url_for('employees', employee_id=3),
            headers={'Content-Type': 'application/json'},
            data='{}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide at least one '
                                         'value to update'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 400
            self.assertEqual(actual_code, expected_code)

    def test_put_item_exists_employees(self):
        response = app.test_client().put(
            url_for('employees', employee_id=42),
            headers={'Content-Type': 'application/json'},
            data='{"name": "Test42_Edited"}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {"message": "Employee 42 doesn't exist"}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)

    def test_put_salary_is_positive_employees(self):
        response = app.test_client().put(
            url_for('employees', employee_id=3),
            headers={'Content-Type': 'application/json'},
            data='{"salary": -1000}')

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide higher then zero '
                                         'value for salary'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_delete_employees(self):
        response = app.test_client().delete(
            url_for('employees', employee_id=3))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = 'Employee 3 was successfully deleted'
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 200
            self.assertEqual(actual_code, expected_code)

        with self.subTest('test_if_really_was_deleted'):
            response_was = app.test_client().get(url_for('employees'))
            actual_was = response_was.json
            expected_was = [{'id': 1, 'name': 'Employee1',
                             'date_of_birth': '1991-01-09', 'salary': 2500,
                             'department_id': 1},
                            {'id': 2, 'name': 'Employee2',
                             'date_of_birth': '1995-07-15', 'salary': 1500,
                             'department_id': 1}]
            self.assertEqual(actual_was, expected_was)

    def test_delete_value_provided_employees(self):
        response = app.test_client().delete(url_for('employees'))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {'message': 'Please provide id for deleting'}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 406
            self.assertEqual(actual_code, expected_code)

    def test_delete_item_exists_employees(self):
        response = app.test_client().delete(
            url_for('employees', employee_id=42))

        with self.subTest('test_response_value'):
            actual_value = response.json
            expected_value = {"message": "Employee 42 doesn't exist"}
            self.assertEqual(actual_value, expected_value)

        with self.subTest('test_response_code'):
            actual_code = response.status_code
            expected_code = 404
            self.assertEqual(actual_code, expected_code)
