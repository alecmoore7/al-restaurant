import pymysql
from flask import Flask, render_template, redirect, url_for, request
import csv  # Used for reading and writing event data via csv.
from os.path import exists 
import html

app = Flask(__name__)

app.config.from_pyfile(app.root_path + '/config_defaults.py')
if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

import database

#Globals for handling csv read/write on server
LAWN_PATH = app.root_path + '/lawns.csv'
LAWN_KEYS = ['address','size','date_added','notes']
CUSTOMER_PATH = app.root_path + '/customers.csv'
CUSTOMER_KEYS = ['name','address','email','dob','phone']
EMPLOYEE_PATH = app.root_path + '/employees.csv'
EMPLOYEE_KEYS = ['first_name', 'last_name', 'address', 'email', 'dob', 'phone', 'start_date', 'title']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lawns/')
def list_lawns():
    lawns = database.get_lawns()
    print(lawns)
    return render_template('lawns.html', lawns=lawns)

@app.route('/employees')
def list_employees():
    employees = database.get_employees()
    print(employees)
    return render_template('employees.html', employees=employees)

@app.route('/customers/')
def list_customers():
    customers = database.get_customers()
    print(customers)
    return render_template('customers.html', customers=customers)


@app.route('/employees/<employee_id>/')
def view_employee(employee_id):
    employee = database.get_employee(employee_id)
    print(employee)
    if employee:
        return render_template('employee.html', employee_id=employee_id, employee=employee)
    else:
        return redirect(url_for('list_employees'))
    
@app.route('/customers/<customer_id>/')
def view_customer(customer_id):
    customer = database.get_customer(customer_id)
    print(customer)
    if customer:
        return render_template('customer.html', customer_id=customer_id, customer=customer)
    else:
        return redirect(url_for('list_customers'))


@app.route('/lawns/<lawn_id>/')
def view_lawn(lawn_id):
    lawn = database.get_lawn(lawn_id)
    customers = database.get_customers()
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        database.assign_lawn_owner(lawn_id, customer_id)
        return render_template('lawn.html', lawn=lawn, customers=customers)
    return redirect(url_for('view_lawn', lawn_id=lawn_id))
    

@app.route('/employee/create', methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']
        start_date = request.form['start_date']
        title = request.form['title']
        database.add_employee(first_name, last_name, address, email, dob, phone, start_date, title)

        return redirect(url_for('list_employees'))
    else:
        return render_template('employee_form.html', employee=None)
    
@app.route('/lawns/create', methods=['GET', 'POST'])
def create_lawn():
    #if we have form data coming in via POST
    if request.method == 'POST':
        address = request.form['address']
        size = request.form['size']
        lawn_type = request.form['date_added']
        date_added =  request.form['lawn_type']
        notes =  request.form['notes']
        database.add_lawn(address, size, date_added, lawn_type, notes)

        return redirect(url_for('list_lawns'))
    else:
        return render_template('lawn_form.html')

@app.route('/employees/<employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = database.get_employee(employee_id)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']
        start_date = request.form['start_date']
        title = request.form['title']

        database.update_employee(employee_id, {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'email': email,
            'dob': dob,
            'phone': phone,
            'start_date': start_date,
            'title': title
        })

        return redirect(url_for('view_employee', employee_id=employee_id)) 
    else:
        return render_template('employee_form.html', employee_id=employee_id, employee=employee)  
        

@app.route('/lawns/<lawn_id>/edit', methods=['GET', 'POST'])
def edit_lawn(lawn_id=None):
    lawn = database.get_lawn(lawn_id)
    if request.method == 'POST':
        address = request.form['address']
        size = request.form['size']
        date_added = request.form['date_added']
        lawn_type = request.form['lawn_type']
        notes = request.form['notes']
        
        database.update_lawn(lawn_id, {
            'address': address,
            'size': size,
            'date_added': date_added,
            'lawn_type': lawn_type,
            'notes': notes
        })

        return redirect(url_for('view_lawn', lawn_id=lawn_id)) 
    else:
        return render_template('lawn_form.html', lawn_id=lawn_id, lawn=lawn)
        
@app.route('/lawn/<lawn_id>/delete', methods=['GET', "POST"])
def delete_lawn(lawn_id=None):
    lawn_id = int(lawn_id)
    delete=request.args.get('delete', None)
    lawns = load_lawns()
    if delete == "1" and lawn_id < len(lawns):
        del lawns[lawn_id]
        database.update_lawn(lawns)
        return redirect(url_for('list_lawns'))  
    else:
        lawn=lawns[lawn_id]
        return render_template('delete_form.html', lawn_id=lawn_id, lawn=lawn)          

if __name__ == '__main__':
    app.run(debug = True)