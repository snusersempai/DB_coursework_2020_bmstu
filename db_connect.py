import mysql.connector
def db_connect(us:str, passw:str):
    conn = mysql.connector.connect(user='root', password='root', host='localhost', database='kursach') # Тут вписать необходимую базу данных
    return conn
