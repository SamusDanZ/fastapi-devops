import mysql.connector 
from mysql.connector import Error

def get_database_connection():
    """
    Función para obtener la conexión a la base de datos
    Intenta conectarse al servidor remoto, si falla intenta localhost
    """
    try:
        # Intentar conexión al servidor remoto
        print("Intentando conectar a informatica.iesquevedo.es...")
        database = mysql.connector.connect(
            host='informatica.iesquevedo.es',
            port=3333,
            ssl_disabled=True,
            user='root',
            password='1asir',
            database='danielmm',
            connect_timeout=5
        )
        print("Conectado a servidor remoto OK")
        return database
    except Error as e:
        print(f"No se pudo conectar al servidor remoto: {e}")
        return None

# Intentar establecer conexión al importar el módulo
database = get_database_connection()