from flask import Flask, render_template, request, redirect, url_for
from forms import EmployeeForm, AssignmentForm, EmployeeAssignmentForm
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
import secrets
from models import Employee, Assignment, DBAssignmentEmployee
from database import (init_db, get_employees, get_employee, save_employee, edit_employee, delete_employee,
                      get_assignments, get_assignment, save_assignment, edit_assignment, delete_assignment,
                      get_employee_assignments, assign_employee_to_assignment, delete_employee_assignment)

app = Flask(__name__)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.secret_key = secrets.token_urlsafe(16)

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

### EMPLOYEES ROUTES ###

@app.route('/employees')
def show_employees():
    employees = get_employees()
    return render_template('employees/employees.html', employees=employees)

@app.route('/employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = Employee(form.firstname.data, form.lastname.data, form.profession.data, form.email.data, form.telephone.data)
        save_employee(employee)
        return redirect(url_for('show_employees'))
    return render_template('employees/employee_form.html', form=form)

@app.route('/employee/<int:id>', methods=['GET', 'POST'])
def edit_employee_route(id):
    employee = get_employee(id)
    if not employee:
        return redirect(url_for('show_employees', message="Employee not found"))
    
    form = EmployeeForm(obj=employee)
    if request.method == 'POST' and form.validate_on_submit():
        edit_employee(id, form.firstname.data, form.lastname.data, form.profession.data, form.email.data, form.telephone.data)
        return redirect(url_for('show_employees', message="Employee updated successfully"))
    
    return render_template('employees/employee_form.html', form=form)

@app.route('/delete_employee/<int:id>')
def delete_employee_route(id):
    delete_employee(id)
    return redirect(url_for('show_employees', message="Employee deleted"))

### ASSIGNMENTS ROUTES ###

@app.route('/assignments')
def show_assignments():
    assignments = get_assignments()
    return render_template('assignments/assignments.html', assignments=assignments)

@app.route('/assignment', methods=['GET', 'POST'])
def add_assignment():
    form = AssignmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        assignment = Assignment(form.title.data, form.description.data, form.location.data)
        save_assignment(assignment)
        return redirect(url_for('show_assignments'))
    return render_template('assignments/assignment_form.html', form=form)

@app.route('/assignment/<int:id>', methods=['GET', 'POST'])
def edit_assignment_route(id):
    assignment = get_assignment(id)
    if not assignment:
        return redirect(url_for('show_assignments', message="Assignment not found"))

    form = AssignmentForm(obj=assignment)
    if request.method == 'POST' and form.validate_on_submit():
        edit_assignment(id, form.title.data, form.description.data, form.location.data)
        return redirect(url_for('show_assignments', message="Assignment updated successfully"))
    
    return render_template('assignments/assignment_form.html', form=form)

@app.route('/delete_assignment/<int:id>')
def delete_assignment_route(id):
    delete_assignment(id)
    return redirect(url_for('show_assignments', message="Assignment deleted"))

### EMPLOYEE-ASSIGNMENT ROUTES ###

@app.route('/employee-assignments')
def show_employee_assignments():
    employee_assignments = get_employee_assignments()
    return render_template('employee_assignments/employee_assignments.html', employee_assignments=employee_assignments)

@app.route('/assign-employee', methods=['GET', 'POST'])
def assign_employee():
    form = EmployeeAssignmentForm()
    form.employee.choices = [(emp.id, emp.firstname + ' ' + emp.lastname) for emp in get_employees()]
    form.assignment.choices = [(assgn.id, assgn.title) for assgn in get_assignments()]
    
    if request.method == 'POST' and form.validate_on_submit():
        assign_employee_to_assignment(form.employee.data, form.assignment.data)
        return redirect(url_for('show_employee_assignments'))
    
    return render_template('employee_assignments/assign_employee.html', form=form)

@app.route('/delete_employee_assignment/<int:id>')
def delete_employee_assignment_route(id):
    result = delete_employee_assignment(id)  
    if result:
        message = "Assignment removed from employee successfully"
    else:
        message = "Failed to remove assignment or it does not exist"

    return redirect(url_for('show_employee_assignments', message=message))

if __name__ == '__main__':
    app.run(debug=True)
