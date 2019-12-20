from flask_restful import fields


employees_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'date_of_birth': fields.String,
    'salary': fields.Float,
    'department_id': fields.Integer
}

departments_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'employees': fields.Nested(employees_structure)
}
