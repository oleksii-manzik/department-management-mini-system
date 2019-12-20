from flask_restful import Resource, marshal_with

from models.model import DepartmentsModel, EmployeesModel
from sqlalchemy.exc import IntegrityError
from service.db import db
from service.fields_structure import departments_structure, employees_structure
from service.parsers import (department_get_parser, department_post_parser,
                             department_put_parser, employee_get_parser,
                             employee_post_parser, employee_put_parser)
from service.fields_check_utils import (all_parameters_is_filled,
                                        item_exists,
                                        value_is_positive,
                                        any_parameter_is_filled,
                                        value_provided, not_wrong_url)


class Departments(Resource):
    """API for Departments CRUD operations"""
    @marshal_with(departments_structure)
    def get(self, department_id=None):
        """Get all departments or some departments by id or name"""
        # check if user didn't use /departments/<department_id> link
        # if used - invokes abort
        not_wrong_url(department_id)
        args = department_get_parser.parse_args(strict=True)
        if args.get('id'):
            return DepartmentsModel.query.filter(
                DepartmentsModel.id.in_(args['id'])).all()
        if args.get('name'):
            return DepartmentsModel.query.filter(
                DepartmentsModel.name == args['name']).first()
        return DepartmentsModel.query.all(), 200

    def post(self, department_id=None):
        """Create new department"""
        # check if user didn't use /departments/<department_id> link
        # if used - invokes abort
        not_wrong_url(department_id)
        args = department_post_parser.parse_args(strict=True)
        # check if user has passed all parameters
        # if hasn't - invokes abort
        all_parameters_is_filled(args)
        department = DepartmentsModel(**args)
        db.session.add(department)
        db.session.commit()
        return f'New department {department.name} with id {department.id} ' \
               f'was added', 201

    def put(self, department_id=None):
        """Edit department"""
        value_provided(department_id, 'updating')
        args = department_put_parser.parse_args(strict=True)
        any_parameter_is_filled(args)
        department = DepartmentsModel.query.filter_by(id=department_id)
        item_exists(department.first(), 'Department', department_id)
        update_data = {k: v for k, v in args.items() if v}
        department.update(update_data)
        db.session.commit()
        return f'Department {department_id} was updated ' \
               f'with data {update_data}', 200

    def delete(self, department_id=None):
        """Delete department"""
        value_provided(department_id, 'deleting')
        department = DepartmentsModel.query.filter_by(id=department_id)
        item_exists(department.first(), 'Department', department_id)
        try:
            department.delete()
        except IntegrityError:
            return "Department wasn't deleted. Please delete employees " \
                   "from this department first", 500
        db.session.commit()
        return f'Department {department_id} was successfully deleted', 200


class Employees(Resource):
    """API for Employees CRUD operations"""
    @marshal_with(employees_structure)
    def get(self, employee_id=None):
        """Get all employees or some employees by id or birthday range"""
        # check if user didn't use /employee/<employee_id> link
        # if used - invokes abort
        not_wrong_url(employee_id)
        args = employee_get_parser.parse_args(strict=True)
        # construct id filter
        if args['id']:
            id_filter = EmployeesModel.id.in_(args['id'])
        else:
            id_filter = True
        # construct date_of_birth_start filter
        if args['date_of_birth_start']:
            bd_start = args['date_of_birth_start']
            bd_start_filter = EmployeesModel.date_of_birth >= bd_start
        else:
            bd_start_filter = True
        # construct date_of_birth_end filter
        if args['date_of_birth_end']:
            bd_end = args['date_of_birth_end']
            bd_end_filter = EmployeesModel.date_of_birth <= bd_end
        else:
            bd_end_filter = True
        return EmployeesModel.query.filter(
            id_filter, bd_start_filter, bd_end_filter).all(), 200

    def post(self, employee_id=None):
        """Create new employee"""
        # check if user didn't use /employees/<employee_id> link
        # if used - invokes abort
        not_wrong_url(employee_id)
        args = employee_post_parser.parse_args(strict=True)
        # check if user has passed all parameters
        # if hasn't - invokes abort
        all_parameters_is_filled(args)
        # check if salary is positive number
        # if not - invokes abort
        value_is_positive(['salary'], args)
        employee = EmployeesModel(**args)
        db.session.add(employee)
        db.session.commit()
        return f'New employee {employee.name} with id {employee.id} ' \
               f'was added', 201

    def put(self, employee_id=None):
        """Edit employee"""
        # check if user provided employee_id
        value_provided(employee_id, 'updating')
        args = employee_put_parser.parse_args(strict=True)
        any_parameter_is_filled(args)
        value_is_positive(['salary'], args)
        employee = EmployeesModel.query.filter_by(id=employee_id)
        item_exists(employee.first(), 'Employee', employee_id)
        update_data = {k: v for k, v in args.items() if v}
        employee.update(update_data)
        db.session.commit()
        return f'Employee {employee_id} was updated with ' \
               f'data {update_data}', 200

    def delete(self, employee_id=None):
        """Delete employee"""
        # check if user provided employee_id
        value_provided(employee_id, 'deleting')
        employee = EmployeesModel.query.filter_by(id=employee_id)
        item_exists(employee.first(), 'Employee', employee_id)
        employee.delete()
        db.session.commit()
        return f'Employee {employee_id} was successfully deleted', 200
