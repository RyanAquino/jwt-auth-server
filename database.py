"""
Custom Database Module utilizing native SQL Connector for querying data
"""
from mysql.connector import errorcode
from functools import wraps
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER
import mysql.connector


def connect_db(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            cnn = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
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
    """
    Query bulk data

    :param cnn: connection returned from decorator
    :param query: query statement
    :return: result from query statement
    """
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query)
    data = []
    for i in cursor:
        data.append(i)

    return data


@connect_db
def query_one(cnn, query):
    """
    Query the first result

    :param cnn: connection returned from decorator
    :param query: query statement
    :return: returns single
    """
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchone()

    return data


@connect_db
def insert(cnn, query, values):
    """
    Insert data into Database

    :param cnn: connection returned from decorator
    :param query: query statement
    :param values: values to be inserted
    :return: data inserted
    """
    cursor = cnn.cursor(dictionary=True)
    cursor.execute(query, values)
    cnn.commit()

    return cursor
