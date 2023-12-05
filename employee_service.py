"Module providing employee service"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Rubytiger5021@127.0.0.1:3306/employees"

db = SQLAlchemy(app)

"Employee class"
class Employee(db.Model):
    id = db.Column('EmployeeID', db.Integer, primary_key = True)
    first_name = db.Column('FirstName', db.String(25), unique=False, nullable=False)
    last_name = db.Column('LastName', db.String(25), unique=False, nullable=False)  
    email_addr = db.Column('EmailAddress', db.String(50), unique=False, nullable=False)
    country = db.Column('Country', db.Integer, unique=False, nullable=False)

    def __init__(self, first_name, last_name, email_addr, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email_addr = email_addr
        self.country = country

with app.app_context():    
    db.create_all()
