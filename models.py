import datetime

class Employee:
    def __init__(self, firstname, lastname, profession, email, telephone):
        self.firstname = firstname
        self.lastname = lastname
        self.profession = profession
        self.email = email
        self.telephone = telephone
    
    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.profession}'
    

class Assignment:
    def __init__(self, title, description, location):
        self.title = title
        self.description = description
        self.location = location

    def __str__(self):
        return f'{self.title} - {self.location}'


class DBAssignment(Assignment):
    def __init__(self, id, title, description, location):
        self.id = id
        super().__init__(title, description, location)

    def __str__(self):
        return f'ID: {self.id}, {super().__str__()}'


class DBAssignmentEmployee:
    def __init__(self, assignment, employee):
        self.assignment = assignment
        self.employee = employee

    def __str__(self):
        return f'Assignment: {self.assignment}, Employee: {self.employee}'
