from flask_restful import fields


departments_structure = {
    'department_id': fields.Integer(attribute='id'),
    'department_name': fields.String(attribute='name')
}

employees_structure = {
    'id': fields.Integer(attribute='employer_id'),
    'name': fields.String(attribute='employer_name'),
    'date_of_birth': fields.DateTime,
    'salary': fields.Float,
    'department_id': fields.Integer
}
