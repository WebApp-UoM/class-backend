import sqlite3
from sqlite3.dbapi2 import IntegrityError

class dbHandler:

    db_path = 'database/database.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def select(self, query, args):
        c = self.conn.cursor()
        c.execute(query, args)
        return c.fetchall()

    def select_no_params(self, query):
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()

    def insert_or_update(self, query, args):
        try:
            self.conn.cursor().execute(query, args)
        except IntegrityError:
            raise IntegrityError
        finally:
            self.conn.commit()

    def insert_no_commit(self, query, args):
        try:
            self.conn.cursor().execute(query, args)
        except IntegrityError:
            raise IntegrityError

    def insert_many_no_commit(self, query, args):
        try:
            self.conn.cursor().executemany(query, args)
        except IntegrityError:
            raise IntegrityError
    
    def get_last_id(self):
        c = self.conn.cursor()
        c.execute('''SELECT last_insert_rowid();''')
        return c.fetchone()

    def commit(self):
        self.conn.commit()

    @staticmethod
    def close(self):
        self.conn.close()
