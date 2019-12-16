from flask_restful import reqparse

department_get_parser = reqparse.RequestParser(bundle_errors=True)
department_get_parser.add_argument('id', type=int, location='args')

department_post_parser = reqparse.RequestParser(bundle_errors=True)
department_post_parser.add_argument('name', type=str, location='json')

department_put_parser = reqparse.RequestParser(bundle_errors=True)
department_put_parser.add_argument('name', type=str, location='json')

employer_get_parser = reqparse.RequestParser(bundle_errors=True)
employer_get_parser.add_argument('id', type=int, location='args')
employer_get_parser.add_argument('date_of_birth_start', type=str,
                                 location='args')
employer_get_parser.add_argument('date_of_birth_end', type=str,
                                 location='args')

employer_post_parser = reqparse.RequestParser(bundle_errors=True)
employer_post_parser.add_argument('name', type=str, location='json')
employer_post_parser.add_argument('date_of_birth', type=str, location='json')
employer_post_parser.add_argument('salary', type=float, location='json')
employer_post_parser.add_argument('department_id', type=str, location='json')

employer_put_parser = reqparse.RequestParser(bundle_errors=True)
employer_put_parser.add_argument('name', type=str, location='json')
employer_put_parser.add_argument('date_of_birth', type=str, location='json')
employer_put_parser.add_argument('salary', type=float, location='json')
employer_put_parser.add_argument('department_id', type=str, location='json')
