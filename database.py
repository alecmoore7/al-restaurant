import pymysql

# Uncomment the following line when you start project 3.2:
# from app import app

def get_connection():
    return pymysql.connect(
        host="db.luddy.indiana.edu",
        user="your_username",
        password="your_password",
        database="Your_DB_password",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_lawns():
    '''Returns a list of dictionaries representing all of the lawns data'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM lawns")
            lawns = cursor.fetchall()
    return lawns

def get_lawn(lawn_id):
    '''Takes a lawn_id, returns a single dictionary containing the data for the lawn with that id'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM lawns WHERE id = %s", (lawn_id,))
            lawn = cursor.fetchone()
    return lawn

def add_lawn(lawn):
    '''Takes as input all of the data for a lawn. Inserts a new lawn into the lawns table'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO lawns (address, size, date_added, notes) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (lawn['address'], lawn['size'], lawn['date_added'], lawn['notes']))
        connection.commit()

def update_lawn(lawn_id, lawn):
    '''Takes a lawn_id and data for a lawn. Updates the lawns table with new data for the lawn with lawn_id as its primary key'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE lawns SET address=%s, size=%s, date_added=%s, notes=%s WHERE id=%s"
            cursor.execute(sql, (lawn['address'], lawn['size'], lawn['date_added'], lawn['notes'], lawn_id))
        connection.commit()

def lawn_owner(customer_id, lawn_id):
    '''Adds an entry into the database that the lawn with primary key lawn_id is owned/managed by the customer with customer_id'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO lawn_owners (customer_id, lawn_id) VALUES (%s, %s)"
            cursor.execute(sql, (customer_id, lawn_id))
        connection.commit()

def get_lawns(customer_id):
    '''Returns a list of dictionaries representing all of the lawns owned/managed by the customer with primary key of customer_id'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT l.* FROM lawns l INNER JOIN lawn_owners lo ON l.id=lo.lawn_id WHERE lo.customer_id = %s"
            cursor.execute(sql, (customer_id,))
            lawns = cursor.fetchall()
    return lawns

def get_owner(lawn_id):
    '''Returns a dictionary with the data for the owner of the lawn with primary key lawn_id'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT c.* FROM customers c INNER JOIN lawn_owners lo ON c.id=lo.customer_id WHERE lo.lawn_id = %s"
            cursor.execute(sql, (lawn_id,))
            owner = cursor.fetchone()
    return owner

def get_customers():
    '''Returns a list of dictionaries representing all of the customer data'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
    return customers

def add_customer(customer):
    '''Takes all of the data required for a customer and inserts it into the customers table'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO customers (first_name, last_name, address, email, phone, dob, start_date, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                customer['first_name'], customer['last_name'], customer['address'], customer['email'],
                customer['phone'], customer['dob'], customer['start_date'], customer['title']
            ))
        connection.commit()

def get_employees():
    '''Returns a list of dictionaries representing all of the employees data'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
    return employees

def get_employee(employee_id):
    '''Takes an employee_id, returns a single dictionary containing the data for the employee with that id'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            employee = cursor.fetchone()
    return employee

def add_employee(employee):
    '''Takes as input all of the data for an employee. Inserts a new employee into the employees table'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO employees (first_name, last_name, address, email, phone, dob, start_date, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                employee['first_name'], employee['last_name'], employee['address'], employee['email'],
                employee['phone'], employee['dob'], employee['start_date'], employee['title']
            ))
        connection.commit()

def update_employee(employee_id, employee):
    '''Takes an employee_id and data for an employee. Updates the employees table with new data for the employee with employee_id as its primary key'''
    with get_connection() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE employees SET first_name=%s, last_name=%s, address=%s, email=%s, phone=%s, dob=%s, start_date=%s, title=%s WHERE id=%s"
            cursor.execute(sql, (
                employee['first_name'], employee['last_name'], employee['address'], employee['email'],
                employee['phone'], employee['dob'], employee['start_date'], employee['title'], employee_id
            ))
        connection.commit()

if __name__ == '__main__':
    # add more test code here to make sure all your functions are working correctly
    try:
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
        
    except Exception as e:
        print(e)