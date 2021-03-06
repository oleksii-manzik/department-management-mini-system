import os
from flask import Flask
from flask_restful import Api

from dmms.service.db import db, migrate
from dmms.service.config import run_config
from dmms.service.resources import Departments, Employees

MIGRATION_DIR = os.path.join('migrations')

app = Flask(__name__)
app.config.from_object(run_config())
db.init_app(app)

with app.app_context():
    db.create_all()

migrate.init_app(app, db, directory=MIGRATION_DIR)

api = Api(app)
api.add_resource(Departments, '/departments', '/departments/<department_id>')
api.add_resource(Employees, '/employees', '/employees/<employee_id>')

if __name__ == '__main__':
    app.run()
