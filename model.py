from os import stat
import random
import sys

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def to_dict(self):
        user = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username
        }
        return user

    @classmethod
    def from_dict(cls, data):
        return cls(data['ROWID'], data['username'], data['password'])

    @staticmethod
    def generate_credentials(firstname, lastname):
        chars ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+}{"
    
        username = firstname[0:3] + lastname [0:3]
        password = ""

        for i in range(9):
            if i < 5:
                username += random.randint(0,9)
            password += random.choice(chars)
        return username, password

class Direction:
    def __init__(self, name, subjects):
        self.name = name
        self.subjects = subjects

    def to_dict(self):
        direction = {
            'name': self.name,
            'subjects': self.subjects
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['subjects'])

    @staticmethod
    def directions_to_dict(data):
        format = {}
        if len(data) > 0:
            print(data[0], file=sys.stderr)

            for row in data:
                if row[0] not in format:
                    format[row[0]] = []
                format[row[0]].append(row[1])
        return format

class Subject:

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def to_dict(self):
        subject = {
            'name': self.name,
            'year': self.year
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['year'])

    @staticmethod
    def subjects_to_dict(data):
        format = {}
        if len(data) > 0:
            for row in data:
                if row[0] not in format:
                    format[row[0]] = []
                format[row[0]].append(row[1])
        return format
        

class Class:
    def __init__(self, year, teacher, students, subject):
        self.year = year
        self.teacher = teacher
        self.students = students
        self.subject = subject

    def to_dict(self):
        subject = {
            'year': self.year,
            'teacher': self.teacher,
            'students': self.students,
            'subject': self.subject

        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['year'], data['teacher'], data['students'], data['subject'])

    @staticmethod
    def classes_to_dict(data):
        format = {}
        return format

class Teacher():
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def set_username(self, username):
        self.username = username

    @classmethod
    def from_dict(cls, data):
        print(data, file=sys.stderr)
        return cls(data['firstname'], data['lastname'], data['email'])
    
    @staticmethod
    def teachers_to_dict(data):
        teachers = []
        user = ['firstname', 'lastname', 'username', 'email', 'phone']
        for row in data:
            teacher = {}
            for attr in user:
                teacher[attr] = row[attr]
            teachers.append(teacher)
        return teachers

class Members:
    def to_dict(self):
        subject = {
            'admin': self.admin,
            'teachers': self.teachers,
            'students': self.students
        }
