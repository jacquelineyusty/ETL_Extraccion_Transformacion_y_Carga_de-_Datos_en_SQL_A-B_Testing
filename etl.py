#%%

import os
import pandas as pd
from config import establecer_conexion
from etl_funciones import  extraer_data, transformar_datos, gestion_nulos, plot_boxplot1, guardar_csv, imputar_columnas, imputar_multiples_columas, crear_bbdd, load_data

def main():
        
    try:
        
        # Verificar si el archivo CSV existe
        file_path = 'data/HR_RAW_DATA.csv'
        if not os.path.exists(file_path):
            print(f"El archivo {file_path} no existe.")
            return

        # Extraer los datos del archivo CSV
        print("Extrayendo datos del CSV...")
        data = extraer_data(file_path)

        if data is not None:
            # Transformar los datos (limpieza, formateo, etc.)
            print("Transformando datos...")
            transformed_data = transformar_datos(data)


        # Verificar si el archivo CSV existe
        file_path2 = 'data/datos_limpiados.csv'
        if not os.path.exists(file_path2):
            print(f"El archivo {file_path2} no existe.")
            return

        # Extraer los datos del archivo CSV limpio
        print("Extrayendo datos del CSV...")
        data_clean = extraer_data(file_path2)

        if data_clean is not None:
            # Gestión de nulos
            print("🔄 Iniciando la gestión de nulos...")
            nulos_data = gestion_nulos(data_clean,['department', 'educationfield', 'roledepartament'])  # Llamada a la función gestión_nulos()
            print("✅ Gestión de nulos completada con éxito.")

            #Verificar Outliers
            print("🔄 Iniciando outliers...")
            outliers1 = plot_boxplot1(data_clean,"totalworkingyears" )  # Llamada a la función gestión_nulos()
            print("✅ Verificación de Outliers de la columna Totalworkingyears exitoso")

            #Imputación de columnas
            print("🔄 Iniciando imputación con la mediana...")
            columnas_generales = imputar_columnas(data_clean,[ "totalworkingyears",'yearincome'])  # Llamada a la función gestión_nulos()
            print("✅  Imputación de columnas generales con éxito.")

            #Imputación de columnas complejas
            print("🔄 Iniciando imputación con la media...")
            columnas_complejas = imputar_multiples_columas(data_clean,['performancerating', 'standardhours', 'worklifebalance'])  # Llamada a la función gestión_nulos()
            print("✅  Imputación de columnas complejas con éxito.")

            # Guardar CSV solo una vez al final
            #guardar_csv(data_clean, "data/df_nulos_gestionados2.csv")

            #Creación de listas para BBDD
            print("🔄 Iniciando creación de listas...")

            # Ruta del archivo CSV
            archivo_csv = "data/df_nulos_gestionados.csv"

            # Cargar el archivo CSV en un DataFrame
            df = pd.read_csv(archivo_csv)

            # Columnas para cada DataFrame 
            columnas_empleados1 = df[['age', 'attrition', 'distancefromhome', 'education', 'educationfield', 
                       'gender', 'maritalstatus',  'totalworkingyears', 
                      'yearsatcompany', 'numcompaniesworked']]

            columnas_valoraciones1 =df[['environmentsatisfaction', 'jobinvolvement', 'jobsatisfaction',
                    'relationshipsatisfaction', 'worklifebalance',
                    'percentsalaryhike']]

            columnas_puesto1 = df[['joblevel', 'jobrole', 'roledepartament', 'department', 'businesstravel', 'overtime',  
                   'remotework', 'yearssincelastpromotion', 'yearswithcurrmanager', 
                   'trainingtimeslastyear', 'standardhours']]

            columnas_costes1 = df[[ 'hourlyrate', 'monthlyrate', 'yearincome', 'stockoptionlevel']]#'monthlyincome'

            #dataframes_tablas(columnas_empleados1, columnas_valoraciones1)       
            #print("✅ Creación de listas para BBDD con éxito.")

            # Establecer la conexión a MySQL
            print("🔄 Conectando a la base de datos...")

            # Establecer la conexión primero
            cnx = establecer_conexion()  

            # Comprobar si la conexión fue exitosa
            if not cnx:
                print("❌ No se pudo establecer la conexión a la base de datos.")
                return

            # Crear el cursor después de que la conexión se haya establecido
            mycursor = cnx.cursor()

            # Crear base de datos y tablas
            print("🔄 Creando base de datos y tablas si no existen...")
            crear_bbdd(cnx, "keeptalentprueba")  # Crear base de datos
            print("✅ Base de datos y tablas creadas correctamente.")
            

             # Llamada a la función para cargar solo los datos de empleados
            print("🔄 Cargando datos de empleados en la base de datos...")
            load_data(cnx, mycursor, columnas_empleados1,columnas_puesto1,columnas_valoraciones1,columnas_costes1)
            print("✅ Carga de todas las tablas con exito.")
            cnx.close()
            print("Conexión cerrada correctamente.")
 
        
    except Exception as e:
        
            print(f"❌ Error en el proceso ETL: {e}")


if __name__ == "__main__":
    main()

            



            
            
            
            
      
        
   
# %%
