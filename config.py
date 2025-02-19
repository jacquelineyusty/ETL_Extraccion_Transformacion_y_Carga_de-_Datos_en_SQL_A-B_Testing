import mysql.connector
from mysql.connector import errorcode

def establecer_conexion(database=None):
    """Función para establecer la conexión a la base de datos"""
    cnx = None
    config = {
        'user': 'root',
        'password': 'AlumnaAdalab',
        'host': '127.0.0.1',
        'raise_on_warnings': True
    }

    if database:  # Solo agregar el parámetro 'database' si se especifica
        config['database'] = database

    try:
        cnx = mysql.connector.connect(**config)
        print(f"Conexión exitosa con la base de datos {database if database else 'MySQL'}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Problema con tu nombre de usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Error: La base de datos {database} no existe.")
        else:
            print(f"Error desconocido: {err}")

    return cnx
