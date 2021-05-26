import sqlite3

class User():

    def __init__(self,total):
        self.users = []

    def get_data(self):
        self.database_connection = sqlite3.connect('./database/git_users.db')
        self.cursor = self.database_connection.cursor()
        self.cursor.execute("SELECT * FROM github_users")
        self.users = self.cursor.fetchall()
        self.database_connection.commit()
        self.database_connection.close()
        return self.users
