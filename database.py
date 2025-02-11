import os
import psycopg2
from dotenv import load_dotenv
from models import DBEmployee, DBAssignment, DBEmployeeAssignment

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('DB_HOST is {}'.format(os.environ.get('DB_HOST')))
else:
    raise RuntimeError('Application configuration not found.')

# Function to connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )
    return conn

# Function to initialize the database tables
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('CREATE TABLE if not exists employees ('
                'id SERIAL PRIMARY KEY,'
                'firstname VARCHAR(100),'
                'lastname VARCHAR(100),'
                'profession VARCHAR(100),'
                'email VARCHAR(100) UNIQUE,'
                'telephone VARCHAR(20));'
                )

    cur.execute('CREATE TABLE if not exists assignments ('
                'id SERIAL PRIMARY KEY,'
                'title VARCHAR(100),'
                'description TEXT,'
                'location VARCHAR(100));'
                )

    # Employee-Assignment Relationship Table
    cur.execute('CREATE TABLE if not exists employee_assignments ('
                'employee_id INT NOT NULL,'
                'assignment_id INT NOT NULL,'
                'assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                'PRIMARY KEY (employee_id, assignment_id),'
                'FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,'
                'FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE);'
                )

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully.")

# EMPLOYEE OPERATIONS

def get_employees():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employees;')
    rows = cur.fetchall()
    employees = [DBEmployee(id=row[0], firstname=row[1], lastname=row[2], profession=row[3], email=row[4], telephone=row[5]) for row in rows]
    cur.close()
    conn.close()
    return employees

def get_employee(employee_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employees WHERE id = %s;', (employee_id,))
    row = cur.fetchone()
    if row is None:
        return None
    employee = DBEmployee(id=row[0], firstname=row[1], lastname=row[2], profession=row[3], email=row[4], telephone=row[5])
    cur.close()
    conn.close()
    return employee

def save_employee(employee):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO employees (firstname, lastname, profession, email, telephone) VALUES (%s, %s, %s, %s, %s);',
                (employee.firstname, employee.lastname, employee.profession, employee.email, employee.telephone))
    conn.commit()
    cur.close()
    conn.close()

def edit_employee(employee, employee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE employees SET firstname = %s, lastname = %s, profession = %s, email = %s, telephone = %s WHERE id = %s;',
                (employee.firstname, employee.lastname, employee.profession, employee.email, employee.telephone, employee_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_employee(employee_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employees WHERE id = %s;', (employee_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM employees WHERE id = %s;', (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True

# ASSIGNMENT OPERATIONS

def get_assignments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments;')
    rows = cur.fetchall()
    assignments = [DBAssignment(id=row[0], title=row[1], description=row[2], location=row[3]) for row in rows]
    cur.close()
    conn.close()
    return assignments

def get_assignment(assignment_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments WHERE id = %s;', (assignment_id,))
    row = cur.fetchone()
    if row is None:
        return None
    assignment = DBAssignment(id=row[0], title=row[1], description=row[2], location=row[3])
    cur.close()
    conn.close()
    return assignment

def save_assignment(assignment):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO assignments (title, description, location) VALUES (%s, %s, %s);',
                (assignment.title, assignment.description, assignment.location))
    conn.commit()
    cur.close()
    conn.close()

def edit_assignment(assignment, assignment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE assignments SET title = %s, description = %s, location = %s WHERE id = %s;',
                (assignment.title, assignment.description, assignment.location, assignment_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_assignment(assignment_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments WHERE id = %s;', (assignment_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM assignments WHERE id = %s;', (assignment_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True

# EMPLOYEE-ASSIGNMENT RELATIONSHIP OPERATIONS

def assign_employee_to_assignment(employee_id, assignment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO employee_assignments (employee_id, assignment_id) VALUES (%s, %s);',
                (employee_id, assignment_id))
    conn.commit()
    cur.close()
    conn.close()

def get_assignments_for_employee(employee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT assignments.id, assignments.title, assignments.description, assignments.location '
                'FROM assignments '
                'JOIN employee_assignments ON assignments.id = employee_assignments.assignment_id '
                'WHERE employee_assignments.employee_id = %s;', (employee_id,))
    rows = cur.fetchall()
    assignments = [DBAssignment(id=row[0], title=row[1], description=row[2], location=row[3]) for row in rows]
    cur.close()
    conn.close()
    return assignments

def get_employees_for_assignment(assignment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT employees.id, employees.firstname, employees.lastname, employees.profession, employees.email, employees.telephone '
                'FROM employees '
                'JOIN employee_assignments ON employees.id = employee_assignments.employee_id '
                'WHERE employee_assignments.assignment_id = %s;', (assignment_id,))
    rows = cur.fetchall()
    employees = [DBEmployee(id=row[0], firstname=row[1], lastname=row[2], profession=row[3], email=row[4], telephone=row[5]) for row in rows]
    cur.close()
    conn.close()
    return employees

def remove_employee_from_assignment(employee_id, assignment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM employee_assignments WHERE employee_id = %s AND assignment_id = %s;', (employee_id, assignment_id))
    conn.commit()
    cur.close()
    conn.close()
