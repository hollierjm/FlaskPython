"Module providing employee service"
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask (__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@127.0.0.1:3306/employees"

db = SQLAlchemy(app)
ma = Marshmallow(app)

"Employee class"
class Employee(db.Model):
    id = db.Column('EmployeeID', db.Integer, primary_key = True)
    first_name = db.Column('FirstName', db.String(25))
    last_name = db.Column('LastName', db.String(25))  
    email_addr = db.Column('EmailAddress', db.String(50))
    country = db.Column('Country', db.Integer)

    def __init__(self, first_name, last_name, email_addr, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email_addr = email_addr
        self.country = country

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('EmployeeID', 'FirstName', 'LastName', 'EmailAddress', 'Country')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

@app.route('/employee', methods=['POST'])
def add_employee():
    first_name = request.json['FirstName']
    last_name = request.json['LastName']
    email_addr = request.json['EmailAddress']
    country = request.json['Country']

    new_employee = Employee(first_name, last_name, email_addr, country)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

@app.route('/employee/<EmployeeID>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

if __name__ == '__main__':
    app.run(debug=True)