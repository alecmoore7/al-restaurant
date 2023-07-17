import csv
from flask import Flask, render_template

app = Flask(__name__)

EMPLOYEES_PATH = app.root_path+'/employees.csv'
CUSTOMERS_PATH = app.root_path+'customers.csv'
LAWNS_PATH = app.root_path+'/lawns.csv'

@app.route('/')
def index():
    """Renders the index page with basic information and navigation buttons."""
    return render_template("index.html")

@app.route('/employees/')
def employees():
    """Renders the employees page with a list of employees sorted by start date."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        employees = sorted(list(reader), key=lambda x: x['employment_start_date'], reverse=True)
    return render_template("employees.html", employees=employees)

@app.route('/employees/<employee_id>/')
def employee(employee_id):
    """Renders the employee details page for the given employee ID."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        employee = next((emp for emp in reader if emp['employee_id'] == employee_id), None)
    return render_template("employee.html", employee=employee)

@app.route('/customers/')
def customers():
    """Reads customer data from the 'customers.csv' file, sorts it by last name from A to Z, and returns a rendered template."""
    try:
        with open(CUSTOMERS_PATH, 'r') as file:
            reader = csv.DictReader(file)
            customers = sorted(reader, key=lambda row: row['name'].split()[-1])
    except Exception as e:
        print(e)
        customers = []
    
    return render_template('customers.html', customers=customers)

@app.route('/lawns/')
def lawns():
    """Renders the lawns page with a list of lawns sorted by size."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lawns = sorted(list(reader), key=lambda x: int(x['size']), reverse=True)
    return render_template("lawns.html", lawns=lawns)

@app.route('/lawns/<lawn_id>/')
def lawn(lawn_id):
    """Renders the lawn details page for the given lawn ID."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lawn = next((l for l in reader if l['id'] == lawn_id), None)
    return render_template("lawn.html", lawn=lawn)

if __name__ == "__main__":
    app.run(debug=True)
