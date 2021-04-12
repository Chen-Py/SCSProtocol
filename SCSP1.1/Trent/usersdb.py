import sqlite3

class UsersDataBase:
    def __init__(self):
        self.database = sqlite3.connect('users.db', check_same_thread = False)
        self.c = self.database.cursor()

        try:
            self.c.execute("""create table users
                (name text primary key,
                N text,
                e text)""")
        except:
            pass

    def insert(self, name, N, e):
        name = str(name)
        N = str(N)
        e = str(e)
        try:
            self.c.execute('insert into users values(?, ?, ?)', (name, N, e))
            self.database.commit()
        except:
            return False
        else:
            return True

    def select(self, name):
        try:
            self.c.execute('select N, e from users where name = ?', (name, ))
            N, e = self.c.fetchone()
            N = int(N)
            e = int(e)
        except:
            return None
        else:
            return N, e

    def has(self, name):
        if self.select(name) != None:
            return True
        else: return False

    def modify(self, name, N, e):
        name = str(name)
        N = str(N)
        m = str(e)
        try:
            if not self.has(name):return False
            self.c.execute('update users set N = ?, e = ? where name = ?', (N, e, name))
            self.database.commit()
        except:
            return False
        else:
            return True

    def delete(self, name):
        name = str(name)
        try:
            if not self.has(name):return False
            self.c.execute('delete from users where name = ?', (name, ))
            self.database.commit()
        except:
            return False
        else:
            return True

    def close(self):
        self.database.commit()
        self.database.close()
        pass
'''
db = UsersDataBase()
print(db.select('Chen_Py'))
print(db.has('Chen_Py'))
print(db.modify('Chen_Py', 312, 333))
print(db.select('Chen_Py'))
print(db.delete('Chen_Py'))
print(db.has("Chen_Py"))
print(db.select('Chen_Py'))
'''