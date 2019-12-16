from flask_restful import Resource, marshal_with

from models.model import DepartmentsModel, EmployeesModel
from service.db import db
from service.fields_structure import departments_structure, employees_structure
from service.parsers import (department_get_parser, department_post_parser,
                             department_put_parser, employer_get_parser,
                             employer_post_parser, employer_put_parser)
from service.fields_check_utils import (all_parameters_is_filled,
                                        item_exists,
                                        value_is_positive,
                                        any_parameter_is_filled,
                                        value_provided, not_wrong_url)


class Departments(Resource):
    @marshal_with(departments_structure)
    def get(self, department_id=None):
        not_wrong_url(department_id)
        args = department_get_parser.parse_args(strict=True)
        if args.get('id'):
            return DepartmentsModel.query.filter(
                DepartmentsModel.id.in_(args['id'])).all()
        return DepartmentsModel.query.all()

    def post(self, department_id=None):
        not_wrong_url(department_id)
        args = department_post_parser.parse_args(strict=True)
        all_parameters_is_filled(args)
        department = DepartmentsModel(**args)
        db.session.add(department)
        db.session.commit()
        return f'New department {department.name} with id {department.id} ' \
               f'was added', 201

    def put(self, department_id=None):
        value_provided(department_id, 'updating')
        args = department_put_parser.parse_args(strict=True)
        any_parameter_is_filled(args)
        department = DepartmentsModel.query.filter_by(id=department_id)
        item_exists(department.first(), 'Department', department_id)
        department.update(filter(lambda x: x is not None, args))
        db.session.commit()
        return f'Department {department.name} with id {department.id} ' \
               f'was updated with data {args}'

    def delete(self, department_id=None):
        value_provided(department_id, 'deleting')
        department = DepartmentsModel.query.filter_by(id=department_id)
        item_exists(department.first(), 'Department', department_id)
        department.delete()
        db.session.commit()
        return f'Department {department_id} was successfully deleted'


class Employees(Resource):

    @marshal_with(employees_structure)
    def get(self, employer_id=None):
        not_wrong_url(employer_id)
        args = employer_get_parser.parse_args(strict=True)
        if args.get('id'):
            return EmployeesModel.query.filter(
                EmployeesModel.id.in_(args['id'])).all()
        return EmployeesModel.query.all()

    def post(self, employer_id=None):
        not_wrong_url(employer_id)
        args = employer_post_parser.parse_args(strict=True)
        all_parameters_is_filled(args)
        employer = EmployeesModel(**args)
        db.session.add(employer)
        db.session.commit()
        return f'New employer {employer.name} with id {employer.id} ' \
               f'was added', 201

    def put(self, employer_id=None):
        value_provided(employer_id, 'updating')
        args = employer_put_parser.parse_args(strict=True)
        any_parameter_is_filled(args)
        employer = EmployeesModel.query.filter_by(id=employer_id)
        item_exists(employer.first(), 'Employer', employer_id)
        employer.update(filter(lambda x: x is not None, args))
        db.session.commit()
        return f'Employer {employer.name} with id {employer.id} ' \
               f'was updated with data {args}'

    def delete(self, employer_id=None):
        value_provided(employer_id, 'deleting')
        employer = EmployeesModel.query.filter_by(id=employer_id)
        item_exists(employer.first(), 'Employer', employer_id)
        employer.delete()
        db.session.commit()
        return f'Department {employer_id} was successfully deleted'
