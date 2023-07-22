import csv
from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

EMPLOYEES_PATH = app.root_path + '/employees.csv'
CUSTOMERS_PATH = app.root_path + '/customers.csv'
LAWNS_PATH = app.root_path + '/lawns.csv'

def read_csv_file(file_path):
    """ Reads data from a CSV file and returns a list of dictionaries."""
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def write_csv_file(file_path, fieldnames, data):
    " Writes data do a CSV file."
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def get_last_lawn_id():
    """Get the ID of the last lawn in the dataset."""
    lawns = read_csv_file(LAWNS_PATH)
    if lawns:
        last_lawn_id = int(lawns[-1]['lawn_id'])
    else:
        last_lawn_id = 0
    return last_lawn_id

def get_last_employee_id():
    """Get the ID of the last employee in the dataset."""
    employees = read_csv_file(EMPLOYEES_PATH)
    if employees:
        last_employee_id = int(employees[-1]['employee_id'])
    else:
        last_employee_id = 0
    return last_employee_id

@app.route('/')
def index():
    """ Renders the index page with basic information and navigation buttons."""
    return render_template("index.html")


@app.route('/employees/', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        pass
    else:
        with open(EMPLOYEES_PATH, 'r') as file:
            reader = csv.DictReader(file)
            employees = list(reader)

        # Sort the employees by start_date in descending order
        employees = sorted(employees, key=lambda e: datetime.datetime.strptime(e.get('start_date', '1900-01-01'), '%Y-%m-%d'), reverse=True)

        return render_template('employees.html', employees=employees)



@app.route('/employees/<employee_id>/', methods=['GET', 'POST'])
def employee(employee_id):
    """ Renders the employee details page for the given employee ID."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    employee = next((e for e in employees if e['employee_id'] == employee_id), None)

    return render_template('employee.html', employee=employee)

@app.route('/customers/', methods=['GET', 'POST'])
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


@app.route('/lawns/', methods=['GET', 'POST'])
def lawns():
    """Renders the lawns page with a list of lawns sorted by size."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lawns = list(reader)

    for lawn in lawns:
        lawn['size'] = int(lawn['size'])

    lawns = sorted(lawns, key=lambda x: x['size'], reverse=True)

    return render_template("lawns.html", lawns=lawns)


@app.route('/lawns/<int:lawn_id>/edit/', methods=['GET', 'POST'])
def lawn(lawn_id):
    """ Renders the lawn details page for the given lawn ID."""
    lawns = read_csv_file(LAWNS_PATH)
    
    lawn = None
    for lawn_data in lawns:
        if lawn_data['lawn_id'] == str(lawn_id):  # Convert lawn_id to a string for comparison
            lawn = lawn_data
            break

    if lawn is None:
        return f"Lawn with ID {lawn_id} not found."

    return render_template("lawn.html", lawn=lawn)


@app.route('/lawns/create/', methods=['GET', 'POST'])
def create_lawn():
    if request.method == 'POST':
        address = request.form['address']
        size_str = request.form['size']
        date_added = request.form['date_added']
        lawn_type = request.form['lawn_type']
        notes = request.form['notes']
        try:
            size = int(size_str)  # Convert size to int only when necessary
        except ValueError:
            size = None  # Or handle the error based on your requirements

        # Generate a new lawn ID
        last_lawn_id = get_last_lawn_id()
        new_lawn_id = last_lawn_id + 1

        new_lawn = {
            'lawn_id': str(new_lawn_id),
            'address': address,
            'size': size,
            'date_added': date_added,
            'lawn_type': lawn_type,
            'notes': notes,
        }

        with open(LAWNS_PATH, 'a', newline='') as csvfile:
            fieldnames = ['lawn_id', 'address', 'size', 'date_added', 'type', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(new_lawn)

        return redirect(url_for('lawns'))

    return render_template('lawn_form.html')

@app.route('/lawns/<int:lawn_id>/edit/', methods=['GET', 'POST'])
def edit_lawn(lawn_id):
    """ Displays form to edit an existing lawn and updates the data in 'lawns.csv', then redirects to the '/lawns/<lawn_id>/' route after successful input."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lawns = list(reader)

    lawn = None
    for l in lawns:
        if l['lawn_id'] == str(lawn_id):
            lawn = l
            break

    if lawn is None:
        return f"Lawn with ID {lawn_id} not found."

    if request.method == 'POST':
        address = request.form['address']
        size_str = request.form['size']
        date_added = request.form['date_added']
        lawn_type = request.form['lawn_type']
        notes = request.form['notes']
        try:
            size = int(size_str)  # Convert size to int only when necessary
        except ValueError:
            size = lawn['size']

        with open(LAWNS_PATH, 'r', newline='') as csvfile:
            fieldnames = ['lawn_id', 'address', 'size', 'date_added', 'type', 'notes']
            rows = list(csv.DictReader(csvfile))
        
        with open(LAWNS_PATH, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row['lawn_id'] == str(lawn_id):
                    row['address'] = address
                    row['size'] = size
                    row['date_added'] = date_added
                    row['type'] = lawn_type
                    row['notes'] = notes
                writer.writerow(row)

        return redirect(url_for('lawn'), lawn_id=lawn_id)
    return render_template('lawn_form.html', lawn=lawn)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/employees/create/', methods=['GET', 'POST'])
def create_employee():
    """ Displays form to create a new employee and adds the data to 'employees.csv', then redirects to the '/employees/' route after successful input."""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        title = request.form['title']
        address = request.form['address']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']

        # Generate a new employee ID
        last_employee_id = get_last_employee_id()
        new_employee_id = last_employee_id + 1

        new_employee = {
            'employee_id': str(new_employee_id),
            'first_name': first_name,
            'last_name': last_name,
            'title': title,
            'address': address,
            'email': email,
            'date_of_birth': date_of_birth,
            'phone': phone,
        }

        with open(EMPLOYEES_PATH, 'a', newline='') as csvfile:
            fieldnames = ['employee_id', 'first_name', 'last_name', 'title', 'address', 'email', 'date_of_birth', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(new_employee)

        return redirect(url_for('employees'))
    return render_template('employee_form.html')


@app.route('/employees/<int:employee_id>/edit/', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Displays form to edit an existing employee and updates the data in 'employees.csv', then redirects to the '/employees/<employee_id>/' route after successful input."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    employee = None
    for emp in employees:
        if emp['employee_id'] == str(employee_id):
            employee = emp
            break

    if employee is None:
        return f"Employee with ID {employee_id} not found."

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        title = request.form['title']

        # Update data in the employees list
        employee['first_name'] = first_name
        employee['last_name'] = last_name
        employee['address'] = address
        employee['email'] = email
        employee['date_of_birth'] = date_of_birth
        employee['phone'] = phone
        employee['title'] = title

        with open(EMPLOYEES_PATH, 'w', newline='') as csvfile:
            fieldnames = ['employee_id', 'first_name', 'last_name', 'address', 'email', 'date_of_birth', 'phone', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)

        return redirect(url_for('employee', employee_id=employee_id))
    return render_template('employee_form.html', employee=employee)

@app.route('/lawns/<int:lawn_id>/delete', methods=['GET', 'POST'])
def delete_lawn(lawn_id):
    """Displays form to delete an existing lawn and updates the data in 'lawns.csv', then redirects to the '/employees/<employee_id>/' route after successful input."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lawns = list(reader)

    lawn = None
    for l in lawns:
        if l['lawn_id'] == str(lawn_id):
            lawn = l
            break

    if lawn is None:
        return f"Lawn with ID {lawn_id} not found."

    if request.method == 'POST':
        lawns = [l for l in lawns if l['lawn_id'] != str(lawn_id)]
        fieldnames = ['lawn_id', 'address', 'size', 'date_added', 'type', 'notes']
        write_csv_file(LAWNS_PATH, fieldnames, lawns)

        return redirect(url_for('lawns'))

    return render_template('lawn_delete.html', lawn=lawn)


if __name__ == "__main__":
    app.run(debug=True)
