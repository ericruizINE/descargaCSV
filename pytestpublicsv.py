import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import re
import os
from PIL import Image
import pytest
import allure
import csv


# Crear la carpeta 'screenshots' si no existe
screenshots_folder = 'screenshots_publi'
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)

def get_next_screenshot_path(folder, base_filename):
    """Genera el siguiente nombre de archivo disponible con un número consecutivo."""
    i = 1
    while True:
        filename = f"{base_filename}_{i:03d}.png"
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            return path
        i += 1

def capture_element_screenshot(driver, element, file_path):
    """
    Captura una captura de pantalla resaltando el elemento específico con un borde.
    """
    # Obtener el tamaño total de la página
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Establecer el tamaño de la ventana al tamaño total de la página
    driver.set_window_size(total_width, total_height)
    # Resaltar el elemento usando JavaScript
    driver.execute_script("arguments[0].style.border='9px solid red'", element)
    
    # Desplazar la página hasta que el elemento esté visible
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Esperar a que el elemento sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of(element)
    )

    # Capturar la pantalla completa
    driver.save_screenshot(file_path)

    # Quitar el borde después de la captura
    driver.execute_script("arguments[0].style.border=''", element)

# Función para leer datos desde el CSV y eliminar el BOM si está presente
def leer_datos_csv(filepath):
    df = pd.read_csv(filepath, encoding='utf-8-sig')

    for index, row in df.iterrows():
        yield row['allure_story'], row['valor'], row['tipo_dato'], row['selector'], row['ruta']

@pytest.fixture
def setup():
    # Configurar el controlador de Chrome
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("Versión chromedriver:", driver.capabilities['browserVersion'])
    driver.maximize_window()

    # URL de la página que deseas validar
    url = 'https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura'
    driver.get(url)

    # Espera a que la página cargue completamente
    driver.implicitly_wait(10)
    
    yield driver  # Retorna el driver para usarlo en las pruebas
    
    driver.quit()  # Asegúrate de cerrar el navegador después de la prueba

@pytest.fixture
def df():
    # Leer el archivo CSV en un DataFrame
    csv_path = '/var/jenkins_home/workspace/Publicacion/Archivos/PRES_2024.csv'
    df = pd.read_csv(csv_path, skiprows=3, nrows=1, header=None, names=[
        "ACTAS_ESPERADAS", "ACTAS_REGISTRADAS", "ACTAS_FUERA_CATALOGO", 
        "ACTAS_CAPTURADAS", "PORCENTAJE_ACTAS_CAPTURADAS", 
        "ACTAS_CONTABILIZADAS", "PORCENTAJE_ACTAS_CONTABILIZADAS", 
        "PORCENTAJE_ACTAS_INCONSISTENCIAS", "ACTAS_NO_CONTABILIZADAS", 
        "LISTA_NOMINAL_ACTAS_CONTABILIZADAS", "TOTAL_VOTOS_C_CS", 
        "TOTAL_VOTOS_S_CS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
    ])

    # Retornar solo las columnas necesarias en un nuevo DataFrame
    selected_columns = df[[
        "ACTAS_ESPERADAS", "ACTAS_CAPTURADAS", "ACTAS_CONTABILIZADAS", "LISTA_NOMINAL_ACTAS_CONTABILIZADAS", "TOTAL_VOTOS_C_CS", "TOTAL_VOTOS_S_CS", "PORCENTAJE_ACTAS_CAPTURADAS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
    ]]

    return selected_columns

@pytest.fixture
def screenshots_folder():
    # Define la ruta de la carpeta donde almacenarás las capturas de pantalla
    return "screenshots_publi"

@pytest.mark.parametrize("allure_story, valor, tipo_dato, selector, ruta", leer_datos_csv('elementos.csv'))
@allure.feature('Validación de datos en sitio de Publicación')
def test_validacion_datos(setup, df, allure_story, valor, tipo_dato, selector, ruta, screenshots_folder):
    """
    Prueba que los valores del encabezado del CSV coincidan con el sitio de publicacion: 
    https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura
    """
    # Aplicar la etiqueta @allure.story dinámicamente
    allure.dynamic.story(allure_story)  # Etiqueta dinámica basada en el CSV

    # Establecer un título dinámico para la prueba
    allure.dynamic.title(allure_story)

    #valor_csv = "{:,.0f}".format(int(df[valor].iloc[0]))
    # Validar el formato según el tipo de dato
    if tipo_dato == 'int':
        valor_csv = "{:,.0f}".format(int(df[valor].iloc[0]))
    elif tipo_dato == 'float':
        valor_csv = "{:,.4f}".format(float(df[valor].iloc[0]))
    else:
        pytest.fail(f"Tipo de dato no reconocido: {tipo_dato}")

    # Convertir el tipo de localizador a su objeto correspondiente de Selenium
    locator_type_obj = eval(selector)
    
    try:
        driver = setup
        elemento = driver.find_element(locator_type_obj, ruta)
        if tipo_dato == 'int':
            valor_en_pagina = elemento.text
        elif tipo_dato == 'float':
            valor_en_pagina2 = elemento.text
            valor_en_pagina = re.sub(r'[^\d.]', '', valor_en_pagina2)
        else:
            pytest.fail(f"Tipo de dato no reconocido: {tipo_dato}")

        file_path = get_next_screenshot_path(screenshots_folder, 'captura_elemento')
        capture_element_screenshot(driver, elemento, file_path)
        
        with allure.step("Comparando los valores de sitio vs csv"):
            if valor_en_pagina == valor_csv:
                allure.attach(
                    f"Los valores coinciden, Sitio: {valor_en_pagina} CSV: {valor_csv}",
                    name="Resultado de la validación",
                    attachment_type=allure.attachment_type.TEXT
                )
                with open(file_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="Captura de pantalla del elemento",
                        attachment_type=allure.attachment_type.PNG
                    )
            else:
                allure.attach(
                    f"Los valores no coinciden, Sitio: {valor_en_pagina} CSV: {valor_csv}",
                    name="Resultado de la validación",
                    attachment_type=allure.attachment_type.TEXT
                )
                with open(file_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="Captura de pantalla del error",
                        attachment_type=allure.attachment_type.PNG
                    )
        # Manejo de excepciones para múltiples validaciones
        resultados_fallidos = []
        try:
            assert valor_en_pagina == valor_csv
        except AssertionError as e:
            resultados_fallidos.append(f"Falló en: {allure_story} - Sitio: {valor_en_pagina} CSV: {valor_csv}")

        if resultados_fallidos:
            pytest.fail(f"Error en validación: {', '.join(resultados_fallidos)}")
            
    except NoSuchElementException:
        # Manejar la excepción si el elemento no se encuentra
        error_message = f"Elemento no encontrado: {selector} - {ruta}"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(error_message)
