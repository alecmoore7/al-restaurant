import pymysql
from app import app

def get_connection():
    return pymysql.connect(host=app.config['DB_HOST'],
                           user=app.config['DB_USER'],
                           password=app.config['DB_PASS'],
                           database=app.config['DB_DATABASE'],
                           cursorclass=pymysql.cursors.DictCursor)

def get_lawns():
    '''Returns a list of dictionaries representing all of the lawns data'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM lawns")
            return cursor.fetchall()

def get_lawn_with_owner(lawn_id):
    '''Takes a lawn_id, returns a dictionary containing the data for the lawn with that id and its owner'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT l.*, c.id AS customer_id, c.first_name, c.last_name FROM lawns l LEFT JOIN lawn_owners lo ON l.id=lo.lawn_id LEFT JOIN customers c ON lo.customer_id=c.id WHERE l.id = %s", (lawn_id,))
            return cursor.fetchone()

def get_lawns_with_owners():
    '''Returns a list of dictionaries representing all lawns with their respective owners'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT l.*, c.id AS customer_id, c.first_name, c.last_name FROM lawns l LEFT JOIN lawn_owners lo ON l.id=lo.lawn_id LEFT JOIN customers c ON lo.customer_id=c.id ORDER BY l.address")
            lawns = cursor.fetchall()

            # Group the lawns by their IDs and aggregate owners if there are multiple owners for a single lawn
            lawns_dict = {}
            for lawn in lawns:
                lawn_id = lawn['id']
                if lawn_id not in lawns_dict:
                    lawns_dict[lawn_id] = {
                        'id': lawn_id,
                        'address': lawn['address'],
                        'size': lawn['size'],
                        'date_added': lawn['date_added'],
                        'lawn_type': lawn['lawn_type'],
                        'notes': lawn['notes'],
                        'owners': []
                    }
                if lawn['customer_id']:
                    lawns_dict[lawn_id]['owners'].append({
                        'id': lawn['customer_id'],
                        'first_name': lawn['first_name'],
                        'last_name': lawn['last_name']
                    })

            return list(lawns_dict.values())



def get_lawn(lawn_id):
    '''Takes a lawn_id, returns a single dictionary containing the data for the lawn with that id'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM lawns WHERE id = %s", (lawn_id,))
            return cursor.fetchone()

def add_lawn(address, size, title, date_added, notes):
    '''Takes as input all of the data for a lawn. Inserts a new lawn into the lawns table'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO lawns (address, size, date_added, notes) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (address, size, title, date_added, notes))
        conn.commit()

def update_lawn(lawn_id, lawn):
    '''Takes a lawn_id and data for a lawn. Updates the lawns table with new data for the lawn with lawn_id as its primary key'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "UPDATE lawns SET address=%s, size=%s, date_added=%s, notes=%s WHERE id=%s"
            cursor.execute(sql, (lawn['address'], lawn['size'], lawn['date_added'], lawn['notes'], lawn_id))
        conn.commit()

def lawn_owner(customer_id, lawn_id):
    '''Adds an entry into the database that the lawn with primary key lawn_id is owned/managed by the customer with customer_id'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO lawn_owners (customer_id, lawn_id) VALUES (%s, %s)"
            cursor.execute(sql, (customer_id, lawn_id))
        conn.commit()

def get_lawns_customers(customer_id):
    '''Returns a list of dictionaries representing all of the lawns owned/managed by the customer with primary key of customer_id'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT l.* FROM lawns l INNER JOIN lawn_owners lo ON l.id=lo.lawn_id WHERE lo.customer_id = %s", (customer_id))
            return cursor.fetchall()

def get_owner(lawn_id):
    '''Returns a dictionary with the data for the owner of the lawn with primary key lawn_id'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT c.* FROM customers c INNER JOIN lawn_owners lo ON c.id=lo.customer_id WHERE lo.lawn_id = %s", (lawn_id))
            return cursor.fetchone()

def get_customers():
    '''Returns a list of dictionaries representing all of the customer data'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM customers")
            return cursor.fetchall()

def add_customer(first_name, last_name, address, email, dob, phone):
    '''Takes all of the data required for a customer and inserts it into the customers table'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO customers (first_name, last_name, address, email, dob, phone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (first_name, last_name, address, email, dob, phone))
        conn.commit()

def get_employees():
    '''Returns a list of dictionaries representing all of the employees data'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employees ORDER BY last_name")
            return cursor.fetchall()

def get_employee(employee_id):
    '''Takes an employee_id, returns a single dictionary containing the data for the employee with that id'''
    conn =  get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            return cursor.fetchone()

def add_employee(first_name, last_name, address, email, dob, phone, start_date, title):
    '''Takes as input all of the data for an employee. Inserts a new employee into the employees table'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO employees (first_name, last_name, address, email, dob, phone, start_date, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (first_name, last_name, address, email, dob, phone, start_date, title))
        conn.commit()

def update_employee(employee_id, employee):
    '''Takes an employee_id and data for an employee. Updates the employees table with new data for the employee with employee_id as its primary key'''
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "UPDATE employees SET first_name=%s, last_name=%s, title=%s, address=%s, email=%s, phone=%s, dob=%s, start_date=%s WHERE id=%s"
            cursor.execute(sql, (employee['first_name'], employee['last_name'], employee['title'], employee['address'], employee['email'],employee['phone'], employee['dob'], employee['start_date'], employee_id))
        conn.commit()



if __name__ == '__main__':
    # add more test code here to make sure all your functions are working correctly
    print(f'All lawns: {get_lawns()}')
    print(f'Trip info for lawn_id 1: {get_lawn(1)}')

    add_lawn({
        "address": "100 N College Ave Bloomington, IN",
        "size": 12500,
        "date_added": "2023-04-22",
        "notes": "Downtown lot"
    })
    print(f'All lawns: {get_lawns()}')
    
    print(f'All Employees: {get_employees()}')
    print(f'All Customers: {get_customers()}')

    add_customer({
        "first_name": "Tom",
        "last_name": "Sawyer",
        "address": "101 E Sam Clemons Dr Bloomington, IN",
        "email": "tsawyer@twain.com",
        "phone": "812-905-165",
        "dob": "1970-04-01",
        "start_date": "2010-05-15",
        "title": "Owner"
    })
    print(f'All Customers: {get_customers()}')
    
    print(f"The owner of lawn with lawn_id 1: {get_owner(1)}")
        