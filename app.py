"Module providing employee service"
import os
from flask import Flask, request, jsonify
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#app.config["MYSQL_DATABASE_USER"] = "root"
#app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
#app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
#app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
#app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@mysql:3306/employees"

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

#Create schema to display the Employee object
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email_addr', 'country')

employee_schema = EmployeeSchema() #singular Employee
employees_schema = EmployeeSchema(many=True) #multiple Employees

@app.route('/')
def display_peoplesuite():
    return 'Displaying PeopleSuite'

#Create new employee from JSON request and add to table
@app.route('/employee', methods=['POST'])
def add_employee():
    try:
        first_name = request.json['FirstName']
        last_name = request.json['LastName']
        email_addr = request.json['EmailAddress']
        country = request.json['Country']

        new_employee = Employee(first_name, last_name, email_addr, country)
        db.session.add(new_employee)
        db.session.commit()

        return employee_schema.jsonify(new_employee)
    except:
        return employee_schema.jsonify(new_employee)

#Return all Employees in table
@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

#Return employee with specified EmployeeID if possible
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

if __name__ == '__main__':
    app.run(host="0.0.0.0")