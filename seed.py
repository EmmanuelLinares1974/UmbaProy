"""
- Create a script called `[seed.py](http://seed.py)` that populates a SQLite database. By default it should search for the first 150 users from GitHub but the script should accept a param called `total` to customize the number of users.
- The fields required for this users are:
    - username
    - id
    - image url
    - type
    - link to his GitHub profile

"""
import requests
import sqlite3

def insert_database_row(username, id, image, type, link):
    database_connection = ''
    try:
        database_connection = sqlite3.connect('./database/git_users.db')
        cursor = database_connection.cursor()
        print("Connected to SQLite")
        sqlite_insert_with_param = """INSERT INTO github_users
                         (username, id, image, type, link)
                         VALUES (?, ?, ?, ?, ?);"""
        fields = (username, id, image, type, link)
        cursor.execute(sqlite_insert_with_param, fields)
        database_connection.commit()
        print("Python Variables inserted successfully into github_users table")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if database_connection:
            database_connection.close()
            print("The SQLite connection is closed")

def get_git_users(pagination,last_user_id = 0):
    if last_user_id == 0:
        URL      = f"https://api.github.com/users?per_page={pagination}"
    else:
        URL = f"https://api.github.com/users?per_page={pagination}&since={last_user_id}"
    USER     = "EmmanuelLinares1974"
    TOKEN    = "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"
    HEADERS  = {'Authorization':'token %s' % TOKEN, 'Accept': 'application/vnd.github.v3+json'}
    return requests.get(URL, HEADERS)

def get_git_data(total):
    tup = tuple(get_iterations(total))
    print(tup)

    if tup[0] != 0:
        counter = 0
        last_id = 0
        tot_aux = total

        while counter < tup[0]:
            response = get_git_users(100,last_id)
            users_aux_page = response.json()
            if counter == 0:
                users_first_page = users_aux_page
            else:
                users_first_page = users_first_page + users_aux_page
            for user in users_first_page:
                last_id = user['id']
            counter += 1
            tot_aux -= 100

        if tot_aux != 0:
            response = get_git_users(tot_aux, last_id)
            users_aux_page = response.json()

        return users_first_page + users_aux_page

    else:
        #Given number is lower than 100
        response = get_git_users(total)
        users_first_page = response.json()
        return users_first_page

def get_iterations(total):
    return divmod(total,100)

def get_git_users_data(total):
    clean_users = []
    del_tab()
    for user in get_git_data(total):
        clean_user = {}
        clean_user["id"]= user["id"]
        clean_user["username"]= user["login"]
        clean_user["image"]= user["avatar_url"]
        clean_user["type"]= user["type"]
        clean_user["link"]= user["url"]
        clean_users.append(clean_user)
        insert_database_row(clean_user["username"], clean_user["id"], clean_user["image"], clean_user["type"], clean_user["link"])

def get_users(total):
    get_git_users_data(total)
    database_connection = sqlite3.connect('./database/git_users.db')
    cursor = database_connection.cursor()
    cursor.execute("SELECT * FROM github_users")
    usuarios = cursor.fetchall()
    database_connection.commit()
    database_connection.close()
    return usuarios

def del_tab():
    database_connection = sqlite3.connect('./database/git_users.db')
    cursor = database_connection.cursor()
    cursor.execute("DELETE FROM github_users")
    database_connection.commit()
    database_connection.close()