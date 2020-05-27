from mysql.connector import errorcode
from functools import wraps
import mysql.connector


def connect_db(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            cnn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='phprest')
            rv = f(cnn, *args, **kwargs)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        else:
            cnn.close()
            return rv

    return wrapper


@connect_db
def query_all(cnn, query):
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query)
    data = []
    for i in cursor:
        data.append(i)

    return data

@connect_db
def query_one(cnn, query):
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchone()

    return data

@connect_db
def insert(cnn, query, values):
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query, values)
    cnn.commit()

    return cursor


# print(query_all('SELECT * FROM users'))
# print(query_one('SELECT * FROM users where username = "test1"'))
# data = {
#     'username': 'test',
#     'password': '$argon2id$v=19$m=102400,t=2,p=8$L+l4tHExPwcCxO+cRK/Viw$DjKX7ZCh34i4PcUVklijYw'
# }
# print(insert('INSERT INTO users (username, password) VALUES (%(username)s, %(password)s)', data))
