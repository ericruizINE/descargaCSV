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
    
archivo_zip1 = os.path.join(f"{directorio_destino}/20240603_2005_PREP.zip")  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
    zip_ref.extractall(directorio_destino)

print(f'Archivo ZIP "{archivo_zip1}" descomprimido exitosamente en "{directorio_destino}"')

@pytest.mark.parametrize("archivo_zip", [
    "20240603_2005_PREP.zip",
    # Agrega aquí más nombres de archivos si quieres probar varios
])
def test_descomprimir_archivo(archivo_zip, directorio_destino):
    """
    Prueba la descompresión de un archivo ZIP.

    Args:
        archivo_zip: Nombre del archivo ZIP a descomprimir.
        directorio_destino: Directorio donde se descomprimirá el archivo.
    """

    archivo_zip1 = os.path.join(f"{directorio_destino}/{archivo_zip}")

    with allure.step("Descomprimiendo archivo ZIP"):
        with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
            zip_ref.extractall(directorio_destino)

    # Verificar si la descompresión fue exitosa
    archivo_descomprimido = os.path.join(directorio_destino, "nombre_archivo_descomprimido")  # Adapta el nombre según el contenido del ZIP
    assert os.path.exists(archivo_descomprimido), f"El archivo {archivo_descomprimido} no se descomprimió correctamente"

    # Agregar información al reporte de Allure
    allure.attach(archivo_zip1, name="Archivo ZIP", attachment_type=allure.attachment_type.ZIP)
    allure.attach(f"El archivo ZIP {archivo_zip1} se descomprimió exitosamente en {directorio_destino}", name="Resultado")
    
    # Archivos CSV a adjuntar
    archivos_csv = ["PRES_2024.csv", "PRES_CANDIDATURAS_2024.csv"]

    for archivo in archivos_csv:
        ruta_completa = os.path.join(directorio_destino, archivo)
        if os.path.exists(ruta_completa):
            # Adjuntar el archivo CSV al reporte
            allure.attach.file(ruta_completa, name=f"Archivo CSV: {archivo}", attachment_type=allure.attachment_type.CSV)

            # Opcional: Crear un resumen del CSV
            df = pd.read_csv(ruta_completa)
            resumen = f"Resumen de {archivo}:\n"
            resumen += f"  Número de filas: {len(df)}\n"
            resumen += f"  Número de columnas: {len(df.columns)}\n"
            allure.attach(resumen, name=f"Resumen de {archivo}", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(f"El archivo CSV {archivo} no se encontró en el directorio de destino.", name="Error", attachment_type=allure.attachment_type.TEXT)