#Importacion de librerias
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer  # Habilitar IterativeImputer
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer

import mysql.connector
from mysql.connector import errorcode

###Importar conexion
from config import establecer_conexion





def extraer_data(filepath):
    """Función para extraer datos de un archivo CSV."""
    try:
        data = pd.read_csv(filepath)
        print(f"Datos extraídos desde {filepath} con éxito.")
        return data
    except Exception as e:
        print(f"Error al extraer datos: {e}")
        return None
    
#Funcion para transformar datos
def transformar_datos(df):

    df2= df.copy()
    mapeo_edades = {
            'thirty-six': '36', 
            'forty-seven': '47', 
            'fifty-eight': '58', 
            'thirty-six': '36', 
            'fifty-five': '55', 
            'fifty-two': '52', 
            'thirty-one': '31',
            'thirty': '30',
            'twenty-six': '26',
            'thirty-seven': '37', 
            'thirty-two': '32', 
            'twenty-four': '24'
                                    }
    
    #Reemplazar los True por Si y los False por No

    diccionario_mapa = {'True': "Si", 'False': "No", 'Yes' : 'Si', '0' : 'No', '1' : 'Si' }
    

    try:
       
       # Aseguramos que la columna 'attrition' esté como string
        df['Attrition'] = df['Attrition'].astype(str)

        # Reemplazar 'Yes' por 'Si' y 'No' por 'No' (si lo deseas)
        df['Attrition'] = df['Attrition'].replace({'Yes': 'Si', 'No': 'No'})
        # Reemplazo de valores en 'Gender'
        df2['Gender'] = df2['Gender'].replace({0: 'M', 1: 'F'})

        # Convertir 'DailyRate' a numérico
        df2['DailyRate'] = pd.to_numeric(df2['DailyRate'], errors='coerce')

        # Eliminar valores duplicados
        df2 = df2.drop_duplicates()

        # Corregir errores tipográficos en 'MaritalStatus'
        df2['MaritalStatus'] = df2['MaritalStatus'].replace({'Marreid': 'Married'})

        # Eliminar valores negativos en 'DistanceFromHome'
        df2 = df2[df2['DistanceFromHome'] >= 0]

        # Imputo los valores nulos con "unknown"
        df2["MaritalStatus"] = df2["MaritalStatus"].fillna("unknown")

        # Cambio las edades escritas a mano 
        df2['Age'] = df['Age'].replace(mapeo_edades)
        
        # Elimino la palabra Travel
        df2['BusinessTravel'] = df2['BusinessTravel'].replace("travel_", "")

        #Eliminar datos negativos
        df2['DistanceFromHome'] = df2['DistanceFromHome'].apply(lambda x : abs(x))

        #Eliminar columnas
        df2.drop(['employeecount', 'employeenumber','SameAsMonthlyIncome', 'Salary', 'NUMBERCHILDREN',  "Over18", 'YearsInCurrentRole'], axis=1, inplace=True)

        #Limpiar registros que no sen numericos
        df2['HourlyRate'] = df2['HourlyRate'].replace({'Not Available': '-1'})

        #Reemplazar los True por Si y los False por No
        df2["RemoteWork"] = df2["RemoteWork"].map(diccionario_mapa)

        #df1['Remotework'] = df1['RemoteWork'].replace({True: 'Si', False: 'No'})

        ## Limpiar registros que no tenga valor numerico a NaN( Ej: ‘not available’)Cambiarlo a tipo float.
        df2['HourlyRate'] = df2['HourlyRate'].replace({'Not Available': '-1'})

        # Pasamos primero a '40' (object) para que no haya numeros con objects.
        df2['StandardHours'] = df2['StandardHours'].replace('80,0', '40')

        # Lista de columnas con los nombres correctos (asegurar que son minúsculas si ya se hizo el cambio)
        cols = ['TOTALWORKINGYEARS', 'YearsInCurrentRole', 'WORKLIFEBALANCE',  'PerformanceRating']
        # Verificar si las columnas existen en df1 antes de procesarlas
        cols_existentes = [col for col in cols if col in df2.columns]

        if cols_existentes:
            df2[cols_existentes] = df2[cols_existentes].astype(str).replace(',', '.', regex=True).astype(float)
        else:
            print("❌ Error: Algunas columnas no existen en el DataFrame. Verifica los nombres.")

         
           
        if "MonthlyIncome" in df2.columns:
            df2["MonthlyIncome"] = pd.to_numeric(df2["MonthlyIncome"], errors='coerce')
    
            # Crear la columna "yearincome"
            df2["yearincome"] = df2["MonthlyIncome"] * 12
    
            # Eliminar MonthlyIncome solo si existe
            df2.drop("MonthlyIncome", axis=1, inplace=True)
        else:
            print("⚠️ Advertencia: 'MonthlyIncome' no existe en el DataFrame.")

        # Crear nuevamente "monthlyIncome"
            df2["monthlyIncome"] = df2["yearincome"] / 12


        #Cambio variables a minuscula
        df2.columns = df2.columns.str.lower()

        # Guardar el DataFrame en un archivo CSV
        df2.to_csv("data/datos_limpiados.csv", index=False)

        print("✅ Transformación de datos completada")
        return df2
    except Exception as e:
        print(f"❌ Error en la transformación de datos: {e}")
        return None
    
    
## falta enviromentsatisfaccion



def gestion_nulos(df, columnas):

    df4 = df.copy()

       
    try:
        for columna in columnas:
            df4[columna] = df4[columna].fillna("unknown")

        print("✅ Imputación de nulos completada.")
        return df4
    except Exception as e:
        print(f"❌ Error en la imputación de nulos: {e}")
        return None
    
        

def calcular_media_mediana(df, columnas):

    df5= df.copy()

    try: 
        

        media = df5[columnas].mean()

        mediana = df5[columnas].median()

        print(f"La media es {media}. La mediana es {mediana}")

        # añadimos un boxplot creado con Seaborn usando el método 'sns.boxplot()'
        sns.boxplot(x = [columnas], 
            data = df5, 
            width = 0.5, 
            color = "violet")
        

        return df5
    except Exception as e:
        print(f"❌ Error de calculo {e}")
        return None
    
   

def plot_boxplot1(df, column, color="turquoise"):
    """Genera un boxplot para la columna seleccionada."""
    sns.boxplot(x=column, data=df, width=0.5, color=color)
    plt.show()

def plot_boxplot2(df, column, color="violet"):
    """Genera un boxplot para la columna seleccionada."""
    sns.boxplot(y=df[column], data=df, width=0.5, color=color)
    plt.show()

    
    

def imputar_columnas(df, column, method="median"):
    """Imputa valores nulos en una columna usando la mediana, IterativeImputer o KNNImputer."""
    df_copy = df.copy()
    
    if method == "median":
        imputed_value = df[column].median()
        df_copy[column] = df[column].fillna(imputed_value)
    elif method == "iterative":
        imputer = IterativeImputer(max_iter=20, random_state=42)
        df_copy[column] = imputer.fit_transform(df[[column]])
    elif method == "knn":
        imputer = KNNImputer(n_neighbors=5)
        df_copy[column] = imputer.fit_transform(df[[column]])
    
    return df_copy


def imputar_multiples_columas(df, columns, strategy="mean"):
    """Imputa valores nulos en múltiples columnas usando la media."""
    df_copy = df.copy()
    for col in columns:
        imputed_value = df[col].mean() if strategy == "mean" else df[col].median()
        df_copy[col] = df[col].fillna(imputed_value)
    return df_copy


def guardar_csv(df, filename):
    """Guarda el DataFrame en un archivo CSV."""
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Archivo guardado: {filename}")
    except Exception as e:
        print(f"❌ Error al guardar CSV: {e}")


#def dataframes_tablas(df):
    #try:
        # Verificar que las columnas existan en el DataFrame
        #for col in df.columns:
            #if col not in df.columns:
                #print(f"❌ La columna '{col}' no existe en el DataFrame.")
               #return None

        # Convertir DataFrame a lista de listas para MySQL
        #lista_df_empleados = df.values.tolist()

        #print("✅ DataFrames convertidos a listas correctamente.")
        #return lista_df_empleados

    #except Exception as e:
        #print(f"❌ Error inesperado: {e}")
        #return None



def crear_bbdd(cnx, bbdd):
    """Función para crear la base de datos si no existe."""
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {bbdd}")
        print(f"Base de datos '{bbdd}' creada con éxito.")
         
        # Seleccionar la base de datos activa
        cursor.execute(f"USE {bbdd}")
        print(f"Base de datos '{bbdd}' seleccionada.")

    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")

    finally:
        cursor.close()  # Asegúrate de cerrar el cursor

    # Establecer el cursor para crear las tablas (esto debe ir después de la creación de la base de datos)
    mycursor = cnx.cursor()

    # Crear la tabla de empleados
    query_crear_tabla_empleado = """CREATE TABLE IF NOT EXISTS empleado (
        id_empleado INT PRIMARY KEY AUTO_INCREMENT,
        age FLOAT,
        attrition VARCHAR(10),
        distancefromhome INT,        
        education INT, 
        educationfield VARCHAR(20), 
        gender VARCHAR(5),
        maritalstatus VARCHAR(10), 
        totalworkingyears FLOAT,
        yearsatcompany INT,
        numcompaniesworked INT
    )"""
    mycursor.execute(query_crear_tabla_empleado)
    
    # Crear la tabla de puestos
    query_crear_tabla_puesto = """CREATE TABLE IF NOT EXISTS puesto (
        id_puesto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_empleado INT,
        joblevel INT,
        jobrole VARCHAR(100), 
        roledepartament VARCHAR(100),
        department VARCHAR(100),
        businesstravel VARCHAR(20),
        overtime VARCHAR(20),
        remotework VARCHAR(10),
        yearssincelastpromotion INT,
        yearswithcurrmanager INT, 
        trainingtimeslastyear FLOAT, 
        standardhours FLOAT,
        FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado) ON DELETE CASCADE
    )"""
    mycursor.execute(query_crear_tabla_puesto)

     

    #Crear tabla valoraciones

    query_crear_tabla_valoraciones = """CREATE TABLE valoraciones (

    id_puesto INT,
    id_empleado INT,
    environmentsatisfaction INT,
    jobinvolvement INT,
    jobsatisfaction INT,
    relationshipsatisfaction INT,
    worklifebalance FLOAT,
    percentsalaryhike INT,
    PRIMARY KEY (id_empleado, id_puesto),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_puesto) REFERENCES puesto(id_puesto) 
   )
    """ 

    mycursor.execute(query_crear_tabla_valoraciones)


    query_crear_tabla_costes = """CREATE TABLE costes (

    id_puesto INT,
    id_empleado INT,
    hourlyrate FLOAT,
    monthlyrate INT,
    yearincome FLOAT,
    stockoptionlevel FLOAT,
    PRIMARY KEY (id_puesto, id_empleado),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_puesto) REFERENCES puesto(id_puesto)  
    )
    """ 

    mycursor.execute(query_crear_tabla_costes)
    print(mycursor)


    
def load_data(cnx, mycursor, df_empleados, df_puesto, df_valoraciones, df_costes):
    """Carga los datos en la base de datos desde un DataFrame."""
    
    # Convertir DataFrame a lista de listas
    lista_df_empleados = df_empleados.values.tolist()
    lista_df_puesto = df_puesto.values.tolist()
    lista_df_valoraciones = df_valoraciones.values.tolist()
    lista_df_costes = df_costes.values.tolist()

    try:
        # Insertar datos en la tabla empleado
        sql_empleado = """INSERT INTO empleado (age, attrition, distancefromhome, education, educationfield,
                         gender, maritalstatus, totalworkingyears, yearsatcompany, numcompaniesworked) 
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        mycursor.executemany(sql_empleado, lista_df_empleados)
        cnx.commit()
        print("✅ Datos insertados en la tabla empleado con éxito.")

        # Obtener los id_empleado generados para asignarlos a los puestos
        mycursor.execute("SELECT id_empleado FROM empleado")
        empleados_ids = [row[0] for row in mycursor.fetchall()]

        # Asignar el id_empleado correspondiente a cada puesto
        lista_df_puesto_con_id_empleado = []
        for i, puesto in enumerate(lista_df_puesto):
            # Asegurarse de que el índice `i` está dentro del rango de empleados_ids
            if i < len(empleados_ids):
                puesto_con_id_empleado = puesto + [empleados_ids[i]]  # Añadir el id_empleado al puesto
                lista_df_puesto_con_id_empleado.append(puesto_con_id_empleado)
            else:
                print(f"⚠️ No hay más empleados para asignar al puesto en el índice {i}.")
        
        # Insertar datos en la tabla puesto, con el id_empleado ya asignado
        sql_puesto = """INSERT INTO puesto (joblevel, jobrole, roledepartament, department, businesstravel, 
                                          overtime, remotework, yearssincelastpromotion, yearswithcurrmanager, 
                                          trainingtimeslastyear, standardhours, id_empleado)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        mycursor.executemany(sql_puesto, lista_df_puesto_con_id_empleado)
        cnx.commit()
        print("✅ Datos insertados en la tabla puesto con éxito.")
        

        # Obtener los id_puesto generados
        mycursor.execute("SELECT id_puesto, id_empleado FROM puesto")
        puestos_ids = mycursor.fetchall()  # Lista de tuplas (id_puesto, id_empleado)
        
        # Agregar id_empleado e id_puesto a valoraciones
        lista_df_valoraciones_con_ids = []
        for i, valoracion in enumerate(lista_df_valoraciones):
            if i < len(puestos_ids):
                id_puesto, id_empleado = puestos_ids[i]
                valoracion_con_ids = valoracion + [id_empleado, id_puesto]
                lista_df_valoraciones_con_ids.append(valoracion_con_ids)
            else:
                print(f"⚠️ No hay más puestos para asignar en valoraciones en el índice {i}.")

        # Insertar datos en la tabla valoraciones con id_empleado e id_puesto
        sql_valoraciones = """INSERT INTO valoraciones (environmentsatisfaction, jobinvolvement, jobsatisfaction,
                    relationshipsatisfaction, worklifebalance,
                    percentsalaryhike, id_empleado, id_puesto) 
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        mycursor.executemany(sql_valoraciones, lista_df_valoraciones_con_ids)
        cnx.commit()
        print("✅ Datos insertados en la tabla costes con éxito.")


        #Cargar datos tabla costes

         # Obtener los id_puesto generados
        mycursor.execute("SELECT id_puesto, id_empleado FROM puesto")
        puestos_ids = mycursor.fetchall()  # Lista de tuplas (id_puesto, id_empleado)
        
        # Agregar id_empleado e id_puesto a valoraciones
        lista_df_costes_con_ids = []
        for i, coste in enumerate(lista_df_costes):
            if i < len(puestos_ids):
                id_puesto, id_empleado = puestos_ids[i]
                costes_con_ids = coste + [id_empleado, id_puesto]
                lista_df_costes_con_ids.append(costes_con_ids)
            else:
                print(f"⚠️ No hay más puestos para asignar en valoraciones en el índice {i}.")
        # Insertar datos en la tabla valoraciones con id_empleado e id_puesto
        sql_costes = """INSERT INTO costes (hourlyrate, monthlyrate, yearincome, stockoptionlevel, id_puesto, id_empleado) VALUES (%s,%s,%s,%s,%s,%s) """
        mycursor.executemany(sql_costes, lista_df_costes_con_ids)
        cnx.commit()
        print("✅ Datos insertados en la tabla valoraciones con éxito.")
        
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")


    
    



    
        



   
