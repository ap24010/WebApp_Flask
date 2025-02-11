from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, ReadOnly, Disabled


class EmployeeForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    profession = StringField('Profession', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    submit = SubmitField('Add Employee')

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Assignment')

class EmployeeAssignmentForm(FlaskForm):
    employee = SelectField('Employee', choices=[], validators=[DataRequired()])
    assignment = SelectField('Assignment', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign Employee')