import pymysql
# Uncomment the following line when you start project 3.2:
from app import app

def get_connection():
    return pymysql.connect(host=app.config['DB_HOST'],
                           user=app.config['DB_USER'],
                           password=app.config['DB_PASS'],
                           database=app.config['DB_DATABASE'],
                           cursorclass=pymysql.cursors.DictCursor)

def get_lawns():
    '''Returns a list of dictionaries representing all of the lawns data'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM lawns")
            lawns = cursor.fetchall()
        return lawns
    except Exception as e:
        print("Error: ", e)
        return []


def get_lawn(lawn_id):
    '''Takes a lawn_id, returns a single dictionary containing the data for the lawn with that id'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM lawns WHERE id = %s", (lawn_id,))
            lawn = cursor.fetchone()
    except Exception as e:
        print("Error: ", e)
        lawn = None
    finally:
        connection.close()
    return lawn

def add_lawn(lawn):
    '''Takes as input all of the data for a lawn. Inserts a new lawn into the lawns table'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO lawns (address, size, date_added, notes) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (lawn['address'], lawn['size'], lawn['date_added'], lawn['notes']))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()


def update_lawn(lawn_id, lawn):
    '''Takes a lawn_id and data for a lawn. Updates the lawns table with new data for the lawn with lawn_id as its primary key'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE lawns SET address=%s, size=%s, date_added=%s, notes=%s WHERE id=%s"
            cursor.execute(sql, (lawn['address'], lawn['size'], lawn['date_added'], lawn['notes'], lawn_id))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()

def lawn_owner(customer_id, lawn_id):
    '''Adds an entry into the database that the lawn with primary key lawn_id is owned/managed by the customer with customer_id'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO lawn_owners (customer_id, lawn_id) VALUES (%s, %s)"
            cursor.execute(sql, (customer_id, lawn_id))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()

def get_lawns_customers(customer_id):
    '''Returns a list of dictionaries representing all of the lawns owned/managed by the customer with primary key of customer_id'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT l.* FROM lawns l INNER JOIN lawn_owners lo ON l.id=lo.lawn_id WHERE lo.customer_id = %s", (customer_id))
            lawns = cursor.fetchall()
        return lawns
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()

def get_owner(lawn_id):
    '''Returns a dictionary with the data for the owner of the lawn with primary key lawn_id'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT c.* FROM customers c INNER JOIN lawn_owners lo ON c.id=lo.customer_id WHERE lo.lawn_id = %s", (lawn_id))
            owner = cursor.fetchone()
    except Exception as e:
        print ("error: ", e)
        owner = None
    finally:
        connection.close
    return owner
    

def get_customers():
    '''Returns a list of dictionaries representing all of the customer data'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
        return customers
    except Exception as e:
        print("Error:", e)
        return []

def add_customer(customer):
    '''Takes all of the data required for a customer and inserts it into the customers table'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO customers (name, address, email, dob, phone) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (customer['name'], customer['address'], customer['email'], customer['dob'],customer['phone']))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()

def get_employees():
    '''Returns a list of dictionaries representing all of the employees data'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
        return employees
    except Exception as e:
        print("Error: ", e)
        return []


def get_employee(employee_id):
    '''Takes an employee_id, returns a single dictionary containing the data for the employee with that id'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            employee = cursor.fetchone()
    except Exception as e:
        print("Error: ", e)
        employee = None
    finally:
        connection.close()
    return employee

def add_employee(employee):
    '''Takes as input all of the data for an employee. Inserts a new employee into the employees table'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO employees (first_name, last_name, title, address, email, phone, dob, start_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (employee['first_name'], employee['last_name'], employee['title'], employee['address'], employee['email'],employee['phone'], employee['dob'], employee['start_date']))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()

def update_employee(employee_id, employee):
    '''Takes an employee_id and data for an employee. Updates the employees table with new data for the employee with employee_id as its primary key'''
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE employees SET first_name=%s, last_name=%s, title=%s, address=%s, email=%s, phone=%s, dob=%s, start_date=%s WHERE id=%s"
            cursor.execute(sql, (employee['first_name'], employee['last_name'], employee['title'], employee['address'], employee['email'],employee['phone'], employee['dob'], employee['start_date'], employee_id))
        connection.commit()
    except Exception as e:
        print("Error: ", e)
    finally:
        connection.close()
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