"Module providing employee service"
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@mysql:3306/employeedb"

db = SQLAlchemy(app)
ma = Marshmallow(app)

"Employee class"
class Employees(db.Model):
    id = db.Column('EmployeeID', db.Integer, primary_key = True)
    first_name = db.Column('FirstName', db.String(25))
    last_name = db.Column('LastName', db.String(25))
    email_addr = db.Column('EmailAddress', db.String(50))
    country = db.Column('Country', db.String(2))
    
    def __init__(self, first_name, last_name, email_addr, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email_addr = email_addr
        self.country = country

#Create schema to display the Employee object
class EmployeesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email_addr', 'country')

employee_schema = EmployeesSchema() #singular Employee
employees_schema = EmployeesSchema(many=True) #multiple Employees

@app.route('/')
def display_peoplesuite():
    return 'Displaying PeopleSuite'

#Create new employee from JSON request and add to table
@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        first_name = request.json['FirstName']
        last_name = request.json['LastName']
        email_addr = request.json['EmailAddress']
        country = request.json['Country']

        new_employee = Employees(first_name, last_name, email_addr, country)
        db.session.add(new_employee)
        db.session.commit()

        return employee_schema.jsonify(new_employee), 200
    except Exception as e:
        return e

#Return all Employees in table
@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        all_employees = Employees.query.all()
        result = employees_schema.dump(all_employees)
        return jsonify(result), 200
    except Exception as e:
        return e

#Return employee with specified EmployeeID if possible
@app.route('/employees/<id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employees.query.get(id)
        return employee_schema.jsonify(employee), 200
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run(host="0.0.0.0")