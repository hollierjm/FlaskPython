# FlaskPython

This flask app runs off SqlAlchemy, so that when connected to a MySQL service in Kubernetes it can POST employees to the MySQL database through the route "/employees", get all employees in the database through a GET request to the route "/employees", and finally get a specific employee by their EmployeeID by sending a GET request to the route "/employees/{EmployeeID}".

Important Notes:
This app uses Marshmallow iun order to simplify JSON objects into outputable objects by Python. This is done by creating a schema for the Employees class in Marshmallow, and then using that schema to derive a simpler object. There is also a schema that handles multiple Employees objects.

There are several test YAML scripts in this repository including mysql-deployment.YAML, mysql-deployment2.YAML, and pvc.YAML. There is no need to run these scripts as the examples provided by Kubernetes to deploy a MySQL PVC, PV, and Deployment is sufficient (kubectl apply -f https://k8s.io/examples/application/mysql/mysql-pv.yaml and kubectl apply -f https://k8s.io/examples/application/mysql/mysql-deployment.yaml).