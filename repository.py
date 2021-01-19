from random import random
from sqlite3.dbapi2 import Error, IntegrityError
from database.db_handler import dbHandler
import model
import sys

class Repo:

    db = dbHandler()

    def close(self):
        self.db.close()

    def commit(self):
        self.db.commit()

    def addToIntermediates(self, table_name, values):
        try:
            self.db.insert_no_commit('''INSERT INTO ? VALUES (?, ?);''',
            (table_name, values))
        except:
            raise Error
    
    def addManyToIntermediates(self, table_name, values):
        try:
            self.db.insert_many_no_commit('''INSERT INTO ? VALUES (?, ?);''',
            (table_name, values))
        except:
            raise Error

    def deleteRow(self, table_name, values):
        try:
            self.db.insert_or_update('''DELETE FROM ? WHERE ? = ?;''',
            (table_name, values))
        except:
            raise IntegrityError


class AuthRepo(Repo):

    def login(self, username):
        query = '''SELECT ROWID, * FROM Authentication WHERE username = ?;'''
        result = self.db.select(query, (username,))
        return result[0]

    def register(self, username, password, role):
        query = '''INSERT VALUES (?, ?, ?) INTO Authentication;'''
        try:
            self.db.insert_or_update(query, (username, password, role))
            return 'success'
        except:
            return 'error'

class AdminRepo(Repo):

    years = ['HS3', 'HS2', 'HS1', 'MS3', 'MS2', 'MS1']

    def getAllDirections(self):
        query = '''SELECT year, name FROM Direction
                        ORDER BY year;'''
        result = self.db.select_no_params(query)
        directions = model.Direction.directions_to_dict(result)

        return directions

    def getDirection(self, year):
        query = '''SELECT year, name FROM Direction
                        WHERE year = ?
                        ORDER BY year;'''
        result = self.db.select(query, (year,))
        directions = model.Direction.directions_to_dict(result)

        return directions

    def getAllSubjects(self):
        subjects = {}
        query = '''SELECT d.name, s.name FROM Direction d
                        INNER JOIN DirectionSubjects ds ON d.id = ds.direction
                        INNER JOIN Subjects s ON s.name = ds.subject
                        WHERE d.year = ?
                        ORDER BY d.name;'''
        for year in self.years:
            result = self.db.select(query, (year,))
            subjects[year] = model.Subject.subjects_to_dict(result)

        return subjects
    
    def getAllTeachers(self):
        query = '''SELECT * FROM Teachers'''
        result = self.db.select_no_params(query)
        response = model.Teacher.teachers_to_dict(result)

        return response


    def getAllClasses(self):
        classes = {}
        query = '''SELECT d.name, s.name FROM Direction d 
                        INNER JOIN DirectionSubjects ds ON d.id = ds.direction
                        INNER JOIN Subjects s ON s.name = ds.subject
                        WHERE year = ?
                        ORDER BY d.name;'''
        for year in self.years:
            result = self.db.select(query, (year,))
            classes[year] = model.Class.classes_to_dict(result)

        return classes

    def addDirection(self, data):

        insert_direction_query = '''INSERT INTO Direction VALUES (NULL, ?, ?);'''        
        try:
            self.db.insert_or_update(insert_direction_query, (data['name'], data['year']))
        except:
            return 'error'


    def addSubject(self, data):
        
        insert_class_query = '''INSERT INTO Subjects VALUES ?;'''

        try:
            self.db.insert_no_commit(insert_class_query, (data['name'],))

            tables = []
            tables.append({'name': 'DirectionSubjects',
                        'data': (data['direction'], data['name']),
                        'many': False})

            for table in tables: 
                if table['many']:
                    self.addManyToIntermediates(table['name'], table['data'])
                    continue
                self.addToIntermediates(table['name'], table['data'])
            self.commit()
        except:
            return 'error'

        

    def addClass(self, data):

        insert_class_query = '''INSERT INTO Classes VALUES ?;'''
        get_id_query = '''SELECT max(id) FROM Classes;'''
        
        try:
            self.db.insert_no_commit(insert_class_query, ('NULL',))
            class_id = self.db.select_no_params(get_id_query)

            tables = []
            tables.append({'name': 'YearsClasses',
                        'data': (data['year'], class_id),
                        'many': False})
            tables.append({'name': 'ClassStudents',
                        'data': (data['students'], [class_id]*len(data['students'])),
                        'many': True})
            tables.append({'name': 'TeachersClasses',
                        'data': (data['teacher'], class_id),
                        'many': False})
            tables.append({'name': 'SubjectClasses',
                        'data': (data['subjects'], [class_id]*len(data['subjects'])),
                        'many': True})

            for table in tables: 
                if table['many']:
                    self.addManyToIntermediates(table['name'], table['data'])
                    continue
                self.addToIntermediates(table['name'], table['data'])
            self.commit()
            return True
        except:
            return False

    def addTeacher(self, data):
        
        insert_teacher_query = '''INSERT INTO Teachers VALUES (?, ?, ?, ?, ?);'''
        insert_auth_query = '''INSERT INTO Authentication VALUES (?, ?, ?);'''

        username, password = model.User.generate_credentials(data['firstname'], data['lastname'])

        try:
            self.db.insert_no_commit(insert_teacher_query, (data['firstname'], data['lastname'], username, data['phone'], data['email']))
            self.db.insert_or_update(insert_auth_query, (username, password, 'teacher'))
            return [username, password]
        except:
            return False
    
    def addStudent(self, data):
        
        insert_teacher_query = '''INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?);'''
        insert_auth_query = '''INSERT INTO Authentication VALUES (?, ?, ?);'''

        username, password = model.User.generate_credentials(data['firstname'], data['lastname'])

        try:
            self.db.insert_no_commit(insert_teacher_query, (data['firstname'], data['lastname'], username, data['year'], data['direction'], data['phone'], data['email']))
            self.db.insert_or_update(insert_auth_query, (username, password, 'student'))
            self.addToIntermediates('YearsStudents', (data['year'], username))
            return [username, password]
        except:
            return False

    def deleteClass(self, data):

        # ****** TO DO ******
        id = data['id']

        try:
            self.deleteRow('Classes', id)
            return True
        except:
            return False
