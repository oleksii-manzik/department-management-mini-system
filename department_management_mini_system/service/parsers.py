from flask_restful import reqparse

department_get_parser = reqparse.RequestParser(bundle_errors=True)
department_get_parser.add_argument('id', type=int, location='args',
                                   action='append')
department_get_parser.add_argument('name', type=str, location='args')

department_post_parser = reqparse.RequestParser(bundle_errors=True)
department_post_parser.add_argument('name', type=str, location='json')

department_put_parser = reqparse.RequestParser(bundle_errors=True)
department_put_parser.add_argument('name', type=str, location='json')

employee_get_parser = reqparse.RequestParser(bundle_errors=True)
employee_get_parser.add_argument('id', type=int, location='args',
                                 action='append')
employee_get_parser.add_argument('date_of_birth_start', type=str,
                                 location='args')
employee_get_parser.add_argument('date_of_birth_end', type=str,
                                 location='args')

employee_post_parser = reqparse.RequestParser(bundle_errors=True)
employee_post_parser.add_argument('name', type=str, location='json')
employee_post_parser.add_argument('date_of_birth', type=str, location='json')
employee_post_parser.add_argument('salary', type=float, location='json')
employee_post_parser.add_argument('department_id', type=int, location='json')

employee_put_parser = reqparse.RequestParser(bundle_errors=True)
employee_put_parser.add_argument('name', type=str, location='json')
employee_put_parser.add_argument('date_of_birth', type=str, location='json')
employee_put_parser.add_argument('salary', type=float, location='json')
employee_put_parser.add_argument('department_id', type=int, location='json')
