import csv
from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/')
def index():
    """ Renders the index page with basic information and navigation buttons."""
    return render_template("index.html")


@app.route('/employees/')
def employees():
    """ Renders the employees page with a list of employees sorted by start date."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        employees = sorted(list(reader), key=lambda x: x['employment_start_date'], reverse=True)
    return render_template("employees.html", employees=employees)


@app.route('/employees/<employee_id>/')
def employee(employee_id):
    """ Renders the employee details page for the given employee ID."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
    for emp in reader:
            if emp['employee_id'] == employee_id:
                employee = emp
                break
    else:
            employee = None
            
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
    """ Renders the lawn details page for the given lawn ID."""
    lawns = read_csv_file(LAWNS_PATH)
    for lawn in lawns:
        if lawn['id'] == lawn_id:
            break
        else:
            lawn = None
    return render_template("lawn.html", lawn=lawn)


@app.route('/lawns/create/', methods=['GET', 'POST'])
def create_lawn():
    """ Displays form to create a new lawn and adds the data to 'lawns.csv', then redirects to the '/lawns/' route after successful input."""
    if request.method == 'POST':
        address = request.form['address']
        size = request.form['size']
        date_added = request.form['date_added']
        lawn_type = request.form['type']
        notes = request.form['notes']

        with open(LAWNS_PATH, 'a', newline='') as csvfile:
            fieldnames = ['address', 'size', 'date_added', 'type', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'address': address, 'size': size, 'date_added': date_added, 'type': lawn_type, 'notes': notes})

        return redirect(url_for('lawn'))
    return render_template('lawn_form.html')

@app.route('/lawns/<int:lawn_id>/edit/', methods=['GET', 'POST'])
def edit_lawn(lawn_id):
    """ Displays form to edit an existing lawn and updates the data in 'lawns.csv', then redirects to the '/lawns/<lawn_id>/' route after successful input."""
    with open(LAWNS_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for lawn in reader:
            if lawn['id'] == lawn_id:
                break
        else:
            lawn = None

    if lawn is None:
        return f"Lawn with ID {lawn_id} not found."

    if request.method == 'POST':
        address = request.form['address']
        size = request.form['size']
        date_added = request.form['date_added']
        lawn_type = request.form['type']
        notes = request.form['notes']

        with open(LAWNS_PATH, 'r', newline='') as csvfile:
            fieldnames = ['id', 'address', 'size', 'date_added', 'type', 'notes']
            rows = list(csv.DictReader(csvfile))
        
        with open(LAWNS_PATH, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row['id'] == lawn_id:
                    row['address'] = address
                    row['size'] = size
                    row['date_added'] = date_added
                    row['type'] = lawn_type
                    row['notes'] = notes
                writer.writerow(row)

        return redirect(url_for('lawn', lawn_id=lawn_id))
    return render_template('lawn_form.html', lawn=lawn)

@app.route('/employees/create/', methods=['GET', 'POST'])
def create_employee():
    """ Displays form to create a new employee and adds the data to 'employees.csv', then redirects to the '/employees/' route after successful input."""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        title = request.form['title']

        with open(EMPLOYEES_PATH, 'a', newline='') as csvfile:
            fieldnames = ['first_name', 'last_name', 'address', 'email', 'date_of_birth', 'phone', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'first_name': first_name,
                'last_name': last_name,
                'address': address,
                'email': email,
                'date_of_birth': date_of_birth,
                'phone': phone,
                'title': title
            })

        return redirect(url_for('employees'))
    return render_template('employee_form.html')


@app.route('/employees/<int:employee_id>/edit/', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Displays form to edit an existing employee and updates the data in 'employees.csv', then redirects to the '/employees/<employee_id>/' route after successful input."""
    with open(EMPLOYEES_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for emp in reader:
            if emp['employee_id'] == employee_id:
                break
        else:
            emp = None

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
        if l['id'] == str(lawn_id):
            lawn = l
            break

    if lawn is None:
        return f"Lawn with ID {lawn_id} not found."

    if request.method == 'POST':
        lawns = [l for l in lawns if l['id'] != str(lawn_id)]
        fieldnames = ['id', 'address', 'size', 'date_added', 'type', 'notes']
        write_csv_file(LAWNS_PATH, fieldnames, lawns)

        return redirect(url_for('lawns'))

    return render_template('lawn_delete.html', lawn=lawn)


if __name__ == "__main__":
    app.run(debug=True)
