import base64
import os
import mysql.connector


# Configuración de la conexión a la base de datos
config = {
  'host': 'localhost',
  'user': 'root',
  'password': '',
  'database': 'soundloop',
}

def connect_to_database():
    connection = mysql.connector.connect(**config)

    return connection


# Users functions
def get_all_users(connection):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "username": row[4],
            "password_hash": row[5]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def get_user_by_user_id(connection, user_id):
    json_data = []
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "username": row[4],
            "password_hash": row[5]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def insert_user(connection, user_data):
    try:    
        cursor = connection.cursor()
        query = "INSERT INTO users (name, surname, email, username, password_hash) VALUES (%s, %s, %s, %s, %s)"
        data = (user_data.name, user_data.surname, user_data.email, user_data.username, user_data.password_hash)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False
    

def get_user_by_name(connection, name):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "username": row[4],
            "password_hash": row[5]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def delete_user_by_id(connection, user_id):
    try:    
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id=%s"
        data = (user_id,)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False

# Soundloops functions
def get_soundLoops(connection, user_id):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loops WHERE user_id=%s", (user_id,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "user_id": row[2]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def insert_soundloop(connection, loop_name, user_id):
    try:    
        cursor = connection.cursor()
        query = "INSERT INTO loops (name, user_id) VALUES (%s, %s)"
        data = (loop_name, user_id)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False
    
def delete_soundLoop(connection, loop_id):
    try:    
        cursor = connection.cursor()
        query = "DELETE FROM loops WHERE id=%s"
        data = (loop_id,)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False
    
def get_soundLoop_by_name(connection, name, user_id):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loops WHERE name=%s AND user_id=%s", (name, user_id,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "user_id": row[2]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def get_soundLoop_by_id(connection, loop_id, user_id):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loops WHERE id=%s AND user_id=%s", (loop_id, user_id,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "name": row[1],
            "user_id": row[2]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def update_soundLoop_name(connection, sound_loop_data):
    try:    
        cursor = connection.cursor()
        query = "UPDATE loops SET name=%s WHERE id=%s AND user_id=%s"
        data = (sound_loop_data.name, sound_loop_data.id, sound_loop_data.user_id)
        cursor.execute(query, data)
        connection.commit()
        return True
    except mysql.connector.Error as error:
        connection.rollback() 
        return False
    finally:
        cursor.close()



# Sounds functions
def get_sound(connection, loop_id, user_id):
    json_data = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sounds WHERE loop_id=%s AND user_id=%s", (loop_id, user_id,))
    result = cursor.fetchall()

    for row in result:
        json_row = {
            "id": row[0],
            "sound_data": base64.b64encode(row[1]).decode('utf-8'),
            "loop_id": row[2],
            "user_id": row[3]
        }
        json_data.append(json_row)
        
    cursor.close()
    return json_data

def insert_sound(connection, blob, user_id, loop_id):
    try:    
        cursor = connection.cursor()
        query = "INSERT INTO sounds (sound_data, loop_id, user_id) VALUES (%s, %s, %s)"
        data = (blob, loop_id, user_id)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False

def delete_sound_from_template(connection, user_id, loop_id):
    try:    
        cursor = connection.cursor()
        query = "DELETE FROM sounds WHERE loop_id=%s AND user_id=%s"
        data = (loop_id, user_id,)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        return False

def close_connection(connection):
    connection.close()


# Other functions
def create_user_dir(user):
    user_dir = 'users'
    user_dir_name = f'{user[0]['id']}_{user[0]['name']}'
    user_dir_path = os.path.join(user_dir, user_dir_name)

    try:
        os.makedirs(user_dir_path)
        return True
    except FileExistsError:
        return False
    
def create_soundLoop_dir(loop, user):
    user_dir = f'users/{user[0]['id']}_{user[0]['name']}'
    soundloop_dir_name = f'{loop[0]['id']}_{loop[0]['name']}'
    soundloop_dir_path = os.path.join(user_dir, soundloop_dir_name)

    try:
        os.makedirs(soundloop_dir_path)
        return True
    except FileExistsError:
        return False