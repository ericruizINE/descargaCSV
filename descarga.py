import requests
import zipfile
import os
import pytest
import allure
import pandas as pd

url = 'https://prep2024.ine.mx/publicacion/nacional/assets/20240603_2005_PREP.zip'
nombre_archivo = '20240603_2005_PREP.zip'
directorio_destino = '/var/jenkins_home/workspace/Publicacion/Archivos'  # Carpeta donde se van a extraer los archivos
ruta_completa = os.path.join(directorio_destino, nombre_archivo)

# Crear la carpeta de destino si no existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Realizar la petición GET al servidor
respuesta = requests.get(url)

# Verificar si la descarga fue exitosa (código 200)
if respuesta.status_code == 200:
    # Guardar el contenido descargado en un archivo local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)
    print(f'Descarga exitosa: {ruta_completa}')
else:
    print(f'Error al descargar: {respuesta.status_code}')
    
# archivo_zip1 = os.path.join(f"{directorio_destino}/20240603_2005_PREP.zip")  # Nombre del archivo ZIP a descomprimir
# # Descomprimir el archivo ZIP
# with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
#     zip_ref.extractall(directorio_destino)

# print(f'Archivo ZIP "{archivo_zip1}" descomprimido exitosamente en "{directorio_destino}"')

@pytest.fixture
def directorio_destino():
    return "/var/jenkins_home/workspace/Publicacion/Archivos"

@pytest.mark.parametrize("archivo_zip, archivos_esperados", [
    ("20240603_2005_PREP.zip", ["PRES_2024.csv", "PRES_CANDIDATURAS_2024.csv"]),
    # Agrega aquí más tuplas (archivo_zip, archivos_esperados) si quieres probar varios
])
@allure.feature('Descarga de CSV Presidencia')  
@allure.story('Descompresion de CSV')  
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_descomprimir_archivo(archivo_zip, archivos_esperados, directorio_destino):
    """
    Prueba la descompresión de un archivo ZIP y la existencia de archivos CSV.

    Args:
        archivo_zip: Nombre del archivo ZIP a descomprimir.
        archivos_esperados: Lista de nombres de archivos CSV esperados tras la descompresión.
        directorio_destino: Directorio donde se descomprimirá el archivo.
    """
    archivo_zip_path = os.path.join(directorio_destino, archivo_zip)

    with allure.step("Descomprimiendo archivo ZIP"):
        with zipfile.ZipFile(archivo_zip_path, 'r') as zip_ref:
            # Crear una carpeta temporal para descomprimir
            carpeta_temporal = os.path.join(directorio_destino, archivo_zip.replace(".zip", ""))
            zip_ref.extractall(carpeta_temporal)

    # Verificar y adjuntar los archivos descomprimidos
    for archivo in archivos_esperados:
        ruta_completa = os.path.join(carpeta_temporal, archivo)
        if os.path.exists(ruta_completa):
            allure.attach.file(ruta_completa, name=f"Archivo CSV: {archivo}", attachment_type=allure.attachment_type.CSV)
            
            # Opcional: Crear un resumen del CSV
            with allure.step(f"Generando resumen para {archivo}"):
                df = pd.read_csv(ruta_completa)
                resumen = f"Resumen de {archivo}:\n  Número de filas: {len(df)}\n  Número de columnas: {len(df.columns)}"
                allure.attach(resumen, name=f"Resumen de {archivo}", attachment_type=allure.attachment_type.TEXT)
        else:
            pytest.fail(f"El archivo CSV {archivo} no se encontró en el directorio de destino.")

    # Adjuntar la información de éxito general
    allure.attach(f"El archivo ZIP {archivo_zip} se descomprimió exitosamente en {carpeta_temporal}", 
                  name="Resultado de descompresión", attachment_type=allure.attachment_type.TEXT)