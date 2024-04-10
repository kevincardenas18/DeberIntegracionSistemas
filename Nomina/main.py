import pandas as pd
import mysql.connector

# Configuración de la conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'database': 'nomina',
    'user': 'root',
    'password': 'MySQL_Password1'
}

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Consulta para verificar la existencia de la tabla
check_table_query = "SHOW TABLES LIKE 'trabajadores'"

# Ejecutar la consulta
cursor.execute(check_table_query)

# Obtener el resultado de la consulta
result = cursor.fetchone()

# Si la tabla existe, borrarla
if result:
    drop_table_query = "DROP TABLE trabajadores"
    cursor.execute(drop_table_query)
    print("La tabla 'trabajadores' ha sido borrada.")
else:
    print("La tabla 'trabajadores' no existe.")
# Definición de la tabla
create_table_query = """

CREATE TABLE IF NOT EXISTS trabajadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Apellido_Paterno VARCHAR(255),
    Apellido_Materno VARCHAR(255),
    Nombres VARCHAR(255),
    Remuneracion_Minima FLOAT,
    FechaIngreso VARCHAR(255)
)
"""

# Ejecutar la consulta para crear la tabla
cursor.execute(create_table_query)



# Ruta del archivo CSV
csv_file_path = 'D:/Universidad/Noveno Semestre/Integracion de Sistemas/Porgreso 1/Proyectos/SistemaNomina/Nomina/csv/listadoTrabajadores.csv'

# Lectura del archivo CSV usando pandas
data = pd.read_csv(csv_file_path)

# Manejar los valores NaN
data = data.fillna('')  # Reemplazar NaN con una cadena vacía

# Iterar sobre cada fila del DataFrame y guardar los registros en la base de datos
for index, row in data.iterrows():
    insert_query = """
    INSERT INTO trabajadores (Apellido_Paterno, Apellido_Materno, Nombres, Remuneracion_Minima, FechaIngreso)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (row['Apellido_Paterno'], row['Apellido_Materno'], row['Nombres'], row['Remuneracion_Minima'], row['FechaIngreso']))

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()