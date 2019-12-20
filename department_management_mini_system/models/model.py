from service.db import db


class DepartmentsModel(db.Model):
    """Model for Departments table"""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    employees = db.relationship('EmployeesModel', backref='department')

    def __repr__(self):
        return f'<Department(id={self.id}, name={self.name})>'


class EmployeesModel(db.Model):
    """Model for Employees table"""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('departments.id'))

    def __repr__(self):
        return f'<Employee(id={self.id}, name={self.name}, ' \
               f'date_of_birth={self.date_of_birth}, salary={self.salary},' \
               f'department_id={self.department_id})>'
