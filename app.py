# Copyright © 2023, Indiana University
# BSD 3-Clause License

import csv 

from flask import Flask, render_template


app = Flask(__name__)

EMPLOYEES_PATH = app.root_path + '/employees.csv'
CUSTOMERS_PATH = app.root_path + '/customers.csv'
LAWNS_PATH = app.root_path + '/lawns.csv'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/employees/')
def employees():
    # Read the employee data from the CSV file
    with open('employees.csv', 'r') as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    # Sort the employees by start_date in descending order
    employees = sorted(employees, key=lambda e: e['start_date'], reverse=True)

    return render_template('employees.html', employees=employees)

@app.route('/employees/<employee_id>/')
def employee(employee_id):
    # Read the employee data from the CSV file
    with open('employees.csv', 'r') as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    # Find the employee with the matching employee_id
    employee = next((e for e in employees if e['employee_id'] == employee_id), None)

    return render_template('employee.html', employee=employee)

@app.route('/customers/')
def customers():
    # Read customer data from CSV file and store it in a list of dictionaries
    with open('customers.csv', 'r') as file:
        reader = csv.DictReader(file)

    customers = sorted(reader, key=lambda c: c['last_name'])

    return render_template('customers.html', customers=customers)

@app.route('/lawns/')
def lawns():
    # Read lawn data from CSV file and store it in a list of dictionaries
    with open('lawns.csv', 'r') as file:
        reader = csv.DictReader(file)

    lawns = sorted(reader, key=lambda l: int(l['size']), reverse=True)

    return render_template('lawns.html', lawns=lawns)

@app.route('/lawns/<int:lawn_id>/')
def lawn(lawn_id):
    # Read the specific lawn data from the CSV file based on the lawn_id
    with open('lawns.csv', 'r') as file:
        reader = csv.DictReader(file)
        lawn = next((l for l in reader if int(l['id']) == lawn_id), None)

    return render_template('lawn.html', lawn=lawn)

if __name__ == "__main__":
    app.run(debug=True)
