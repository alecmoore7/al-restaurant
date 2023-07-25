from flask import Flask, render_template, redirect, url_for, request
import csv  # Used for reading and writing event data via csv.
from os.path import exists 


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
EMPLOYEE_KEYS = ['name','address','email','dob','phone','start_date','title']

def get_lawns():
    #create new list to hold the dictionaries
    return database.get_lawns()

def set_lawns(lawns):
    database.set_lawns(lawns)

def get_customers():
    #create new list to hold the dictionaries
    return database.get_customers()

def set_customers(customers):
    database.set_customers(customers)

def get_employees():
    #create new list to hold the dictionaries
    return database.get_employees()

def set_employees(employees):
    database.set_employees(employees)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lawns/')
def list_lawns():
    lawns = get_lawns()
    lawns= sorted(lawns, key=lambda e: e['size'], reverse=True)
    return render_template('lawns.html', lawns=lawns)

@app.route('/employees/')
def list_employees():
    employees = get_employees()
    employees= sorted(employees, key=lambda e: e['start_date'])
    return render_template('employees.html', employees=employees)

@app.route('/customers/')
def list_customers():
    customers = get_customers()
    customers=sorted(customers, key=lambda e: e['name'])
    return render_template('customers.html', customers=customers)

@app.route('/employees/<employee_id>/')
def view_employee(employee_id=None):
    if employee_id:
        #grab employee_id from route and convert to int so we can use it as an index
        employee_id = int(employee_id)
        employees = get_employees()

        return render_template('employee.html', employee_id=employee_id, employee=employees[employee_id])
    else:
        return redirect(url_for('list_employees'))

@app.route('/lawns/<lawn_id>/')
def view_lawn(lawn_id=None):
    if lawn_id:
        #grab lawn_id from route and convert to int so we can use it as an index
        lawn_id = int(lawn_id)
        lawns = get_lawns()
        return render_template('lawn.html', lawn_id=lawn_id, lawn=lawns[lawn_id])
    else:
        return redirect(url_for('list_lawns'))

@app.route('/lawns/create', methods=['GET', 'POST'])
def create_lawn():
    #if we have form data coming in via POST
    if request.method == 'POST':
        #grab the full lawns data and make a new empty dictionary for the incoming data
        lawns = get_lawns()
        lawn = {}
        # grab the form data coming in and store in the new dict
        lawn['name'] = request.form['name']
        lawn['pet_type'] = request.form['pet_type']
        lawn['level'] = request.form['level']
        lawn['start_date'] = request.form['start_date']
        lawn['start_time'] = request.form['start_time']
        lawn['duration'] = request.form['duration']
        lawn['length'] = request.form['length']
        lawn['trainer'] = request.form['trainer']
        lawn['desc'] = request.form['desc']
        #add the new dict to our lawns data
        lawns.append(lawn)
        
        # Make sure events are sorted by date.
        lawns = sorted(lawns, key=lambda e: e['start_date'])

        # Write data back out to csv.
        set_lawns(lawns)

        # Return to the list of events.
        return redirect(url_for('list_lawns'))
    else:
        return render_template('lawn_form.html')

@app.route('/lawns/<lawn_id>/edit', methods=['GET', 'POST'])
def edit_lawn(lawn_id=None):
    #if we have form data coming in via POST
    if request.method== 'POST':
        #grab the full lawns data
       lawns = get_lawns() 
       lawn_id=int(lawn_id)
        # grab the form data coming in and replace values in lawns data
       lawns[lawn_id]['name'] = request.form['name']
       lawns[lawn_id]['pet_type'] = request.form['pet_type']
       lawns[lawn_id]['level'] = request.form['level']
       lawns[lawn_id]['start_date'] = request.form['start_date']
       lawns[lawn_id]['start_time'] = request.form['start_time']
       lawns[lawn_id]['duration'] = request.form['duration']
       lawns[lawn_id]['length'] = request.form['length']
       lawns[lawn_id]['desc'] = request.form['desc']
       lawns[lawn_id]['trainer'] = request.form['trainer']
       #save the modified lawns list of dictionaries
       set_lawns(lawns)
       #redirect to the lawn page 
       return redirect(url_for('view_lawn', lawn_id=lawn_id)) 
    else:
        #no form data, show the basic edit form with lawn data passed in
        lawn_id = int(lawn_id)
        lawns = get_lawns()
        lawn=lawns[lawn_id]
        return render_template('lawn_form.html', lawn_id=lawn_id, lawn=lawn)
        
@app.route('/lawn/<lawn_id>/delete', methods=['GET', "POST"])
def delete_lawn(lawn_id=None):
    lawn_id = int(lawn_id)
    delete=request.args.get('delete', None)
    lawns = get_lawns()
    if delete == "1" and lawn_id < len(lawns):
        del lawns[lawn_id]
        set_lawns(lawns)
        return redirect(url_for('list_lawns'))  
    else:
        lawn=lawns[lawn_id]
        return render_template('delete_form.html', lawn_id=lawn_id, lawn=lawn)          

if __name__ == '__main__':
    app.run(debug = True)