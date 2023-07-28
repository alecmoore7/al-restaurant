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
EMPLOYEE_KEYS = ['name','address','title','email','dob','phone','start_date']

@app.route('/')
def index():
    return render_template('index.html')

def load_customers():
    return database.get_customers()

def load_lawns():
    return database.get_lawns()


@app.route('/lawns/')
def list_lawns():
    lawns = load_lawns()
    lawns= sorted(lawns, key=lambda e: e['size'], reverse=True)
    return render_template('lawns.html', lawns=lawns)

@app.route('/employees')
def list_employees():
    employees = database.get_employees()
    print(employees)
    return render_template('employees.html', employees=employees)

@app.route('/customers/')
def list_customers():
    customers = load_customers()
    customers=sorted(customers, key=lambda e: e['name'])
    return render_template('customers.html', customers=customers)


@app.route('/employees/<employee_id>/')
def view_employee(employee_id):
    employee = database.get_employee(employee_id)
    print(employee)
    if employee:
        return render_template('employee.html', employee_id=employee_id, employee=employee)
    else:
        return redirect(url_for('list_employees'))


@app.route('/lawns/<lawn_id>/')
def view_lawn(lawn_id):
    lawn = database.get_lawn(lawn_id)
    if lawn:
        return render_template('lawn.html', lawn_id=lawn_id, lawn=lawn)
    else:
        return redirect(url_for('list_lawns'))

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
        lawn_type = request.form['lawn_type']
        date_added =  request.form['date_added']
        notes =  request.form['notes']
        database.add_lawn(address, size, lawn_type, date_added, notes)

        return redirect(url_for('list_lawns'))
    else:
        return render_template('lawn_form.html')

@app.route('/employees/<employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = database.get_employee(employee_id)
    if request.method== 'POST':
        employee_id = int(employee_id)
        employee[employee_id]['first_name']: request.form['first_name']
        employee[employee_id]['last_name']: request.form['last_name']
        employee[employee_id]['title']: request.form['title']
        employee[employee_id]['address']: request.form['address']
        employee[employee_id]['email']: request.form['email']
        employee[employee_id]['dob']: request.form['dob']
        employee[employee_id]['phone']: request.form['phone']
        employee[employee_id]['start_date']: request.form['start_date']
        employee.append(employee)
            
        database.update_employee(employee_id, employee)

        return redirect(url_for('list_employee', employee_id=employee_id)) 
    else:
        return render_template('employee_form.html', employee_id=employee_id, employee=employee)
    
        

@app.route('/lawns/<lawn_id>/edit', methods=['GET', 'POST'])
def edit_lawn(lawn_id=None):
    lawn = database.get_lawn(lawn_id)
    if lawn:
        if request.method== 'POST':
            lawns = load_lawns()
            lawn_id = int(lawn_id)
            lawns[lawn_id]['address'] = request.form['address']
            lawns[lawn_id]['size'] = request.form['size']
            lawns[lawn_id]['lawn_type'] = request.form['lawn_type']
            lawns[lawn_id]['date_added'] = request.form['date_added']
            lawns[lawn_id]['notes'] = request.form['notes']
            lawns.append(lawn)
        
            database.update_lawn(lawn_id, lawn)

            return redirect(url_for('list_lawn', lawn_id=lawn_id)) 
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