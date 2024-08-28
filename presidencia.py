import pandas as pd
import numpy as np
from rich import print
import re
import datetime

def registrar_hora():
    ahora = datetime.datetime.now()
    hora_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    print("Hora de ejecución:", hora_formateada)

file_path = '/var/jenkins_home/workspace/Publicacion/Archivos/PRES_2024.csv'
df = pd.read_csv(file_path, skiprows=4, delimiter=',', low_memory=False)  # Cambia ';' por el delimitador correcto
df1 = pd.read_csv(file_path, skiprows=3, nrows=1, header=None, names=["ACTAS_ESPERADAS","ACTAS_REGISTRADAS","ACTAS_FUERA_CATALOGO","ACTAS_CAPTURADAS","PORCENTAJE_ACTAS_CAPTURADAS","ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_INCONSISTENCIAS","ACTAS_NO_CONTABILIZADAS","LISTA_NOMINAL_ACTAS_CONTABILIZADAS","TOTAL_VOTOS_C_CS","TOTAL_VOTOS_S_CS","PORCENTAJE_PARTICIPACION_CIUDADANA"])

# Mapeo de las columnas datos
CONTABILIZADA = 'CONTABILIZADA'
OBSERVACIONES = 'OBSERVACIONES'
LISTA_NOMINAL = 'LISTA_NOMINAL'
TOTAL_VOTOS_CALCULADO = 'TOTAL_VOTOS_CALCULADO'
TIPO_CASILLA = 'TIPO_CASILLA'

# Mapeo de las columnas conteos
ACTAS_ESPERADAS = 'ACTAS_ESPERADAS'
ACTAS_REGISTRADAS = 'ACTAS_REGISTRADAS'
ACTAS_FUERA_CATALOGO = 'ACTAS_FUERA_CATALOGO'
ACTAS_CAPTURADAS = 'ACTAS_CAPTURADAS'
PORCENTAJE_ACTAS_CAPTURADAS = 'PORCENTAJE_ACTAS_CAPTURADAS'
ACTAS_CONTABILIZADAS = 'ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_CONTABILIZADAS = 'PORCENTAJE_ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_INCONSISTENCIAS = 'PORCENTAJE_ACTAS_INCONSISTENCIAS'
ACTAS_NO_CONTABILIZADAS = 'ACTAS_NO_CONTABILIZADAS'
LISTA_NOMINAL_ACTAS_CONTABILIZADAS = 'LISTA_NOMINAL_ACTAS_CONTABILIZADAS'
TOTAL_VOTOS_C_CS = 'TOTAL_VOTOS_C_CS'
TOTAL_VOTOS_S_CS = 'TOTAL_VOTOS_S_CS'
PORCENTAJE_PARTICIPACION_CIUDADANA = 'PORCENTAJE_PARTICIPACION_CIUDADANA'

# Función para limpiar los valores
def limpiar_valor(valor):
    # Usar regex para extraer solo el contenido entre corchetes y comillas simples
    if isinstance(valor, str):
        # Extrae el contenido entre comillas simples
        return ', '.join(re.findall(r"'([^']*)'", valor))
    return valor
# Aplicar la limpieza a la columna
df[OBSERVACIONES] = df[OBSERVACIONES].apply(limpiar_valor)

# Filtros para realizar conteos y enviarlos como parametros
valores_especificos = ['1']
valores_especificos2 = ['2']
valores_especificos3 = ['0']
valores_especificos4 = ['0','1','2']
valores_especificos5 = ['0','1']
valores_especificos6 = [
    'Todos los campos ilegibles',
    'Sin dato',
    'Ilegible',
    'Todos los campos vacíos',
    'Ilegible, Sin dato',
    'Excede Lista Nominal',
    'Excede Lista Nominal, Sin dato',
    'Excede Lista Nominal, Ilegible',
    'Excede Lista Nominal, Ilegible, Sin dato'
]

if CONTABILIZADA in df.columns:
    filtro = df[CONTABILIZADA].isin(valores_especificos)
    df_filtrado = df[filtro]

if CONTABILIZADA in df.columns:
    filtro2 = df[CONTABILIZADA].isin(valores_especificos2)
    df_filtrado2 = df[filtro2]

if CONTABILIZADA in df.columns:
    filtro3 = df[CONTABILIZADA].isin(valores_especificos3)
    df_filtrado3 = df[filtro3]

if CONTABILIZADA in df.columns:
    filtro4 = df[CONTABILIZADA].isin(valores_especificos4)
    df_filtrado4 = df[filtro4]

if CONTABILIZADA in df.columns:
    filtro5 = df[CONTABILIZADA].isin(valores_especificos5)
    df_filtrado5 = df[filtro5]

if OBSERVACIONES in df.columns:
    filtro6 = df[OBSERVACIONES].isin(valores_especificos6)
    df_filtrado6 = df[filtro6]

if CONTABILIZADA in df.columns and LISTA_NOMINAL in df.columns:
    df_filtrado7 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado7[LISTA_NOMINAL] = pd.to_numeric(df_filtrado[LISTA_NOMINAL], errors='coerce')
    
if CONTABILIZADA in df.columns and TOTAL_VOTOS_CALCULADO in df.columns:
    df_filtrado8 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado8[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado[TOTAL_VOTOS_CALCULADO], errors='coerce')

if TOTAL_VOTOS_CALCULADO in df.columns and TIPO_CASILLA in df.columns:
    #df_filtrado9 = df[df[TIPO_CASILLA] != 'S'].copy()
    df_filtrado9 = df[(df[CONTABILIZADA].isin(['1','2'])) & (df[TIPO_CASILLA] != 'S')].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado9[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado9[TOTAL_VOTOS_CALCULADO], errors='coerce')

    value_counts = df_filtrado[CONTABILIZADA].value_counts()
    value_counts1 = df_filtrado2[CONTABILIZADA].value_counts()
    value_counts2 = df_filtrado3[CONTABILIZADA].value_counts()
    value_counts3 = df_filtrado4[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts3 = [value_counts3]
    value_counts4 = df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts4 = [value_counts4]
    value_counts5 = (df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts5 = pd.Series(value_counts5)
    value_counts5 = value_counts5.apply(lambda x: int(x * 10000) / 10000)
    value_counts6 = (df_filtrado[CONTABILIZADA].value_counts() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts6 = pd.Series(value_counts6)
    value_counts6 = value_counts6.apply(lambda x: int(x * 10000) / 10000)
    value_counts7 = (df_filtrado6[OBSERVACIONES].value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts7 = pd.Series(value_counts7)
    value_counts7 = value_counts7.apply(lambda x: int(x * 10000) / 10000)
    value_counts8 = df_filtrado7[LISTA_NOMINAL].sum()
    value_counts8 = [value_counts8]
    value_counts9 = (df_filtrado8[TOTAL_VOTOS_CALCULADO].sum() * 100) / value_counts8
    value_counts9 = pd.Series(value_counts9)
    value_counts9 = value_counts9.apply(lambda x: int(x * 10000) / 10000)
    value_counts10 = df_filtrado8[TOTAL_VOTOS_CALCULADO].sum()
    value_counts10 = [value_counts10]
    value_counts11 = df_filtrado9[TOTAL_VOTOS_CALCULADO].sum()
    value_counts11 = [value_counts11]
    #print(value_counts11)

print("VALIDACION DE CSV DE PRESIDENCIA, REALIZANDO CONTEOS CON LOS DATOS Y VALIDANDO CON EL PRIMER ENCABEZADO")

registrar_hora()
print("Archivo:", file_path)

print("1.- ACTAS_ESPERADAS:", df1[ACTAS_ESPERADAS].values)

if np.array_equal(value_counts3, df1[ACTAS_REGISTRADAS].values):
    print("[green]2.- Los valores de ACTAS_REGISTRADAS coinciden:[/green]", df1[ACTAS_REGISTRADAS].values)
else:
    print("[red]2.- Los valores de ACTAS_REGISTRADAS no coinciden.[/red]", df1[ACTAS_REGISTRADAS].values, "vs", value_counts3)

if np.array_equal(value_counts1, df1[ACTAS_FUERA_CATALOGO].values):
    print("[green]3.- Los valores de ACTAS_FUERA_CATALOGO coinciden:[/green]", df1[ACTAS_FUERA_CATALOGO].values)
else:
    print("[red]3.- Los valores de ACTAS_FUERA_CATALOGO no coinciden.[/red]", df1[ACTAS_FUERA_CATALOGO].values)
    print(value_counts1)

if np.array_equal(value_counts4, df1[ACTAS_CAPTURADAS].values):
    print("[green]4.- Los valores de ACTAS_CAPTURADAS coinciden:[/green]", df1[ACTAS_CAPTURADAS].values)
else:
    print("[red]4.- Los valores de ACTAS_REGISTRADAS no coinciden.[/red]", df1[ACTAS_CAPTURADAS].values, "vs", value_counts4)

if np.array_equal(value_counts5, df1[PORCENTAJE_ACTAS_CAPTURADAS].values):
    print("[green]5.- Los valores de PORCENTAJE_ACTAS_CAPTURADAS coinciden:[/green]", df1[PORCENTAJE_ACTAS_CAPTURADAS].values)
else:
    print("[red]5.- Los valores de ACTAS_REGISTRADAS no coinciden.[/red]", df1[ACTAS_CAPTURADAS].values, "vs", value_counts5)

if np.array_equal(value_counts, df1[ACTAS_CONTABILIZADAS].values):
    print("[green]6.- Los valores de ACTAS_CONTABILIZADAS coinciden:[/green]", df1[ACTAS_CONTABILIZADAS].values)
else:
    print("[red]6.- Los valores de ACTAS_CONTABILIZADAS no coinciden.[/red]", df1[ACTAS_CONTABILIZADAS].values)
    print(value_counts)

if np.array_equal(value_counts6, df1[PORCENTAJE_ACTAS_CONTABILIZADAS].values):
    print("[green]7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coinciden:[/green]", df1[PORCENTAJE_ACTAS_CONTABILIZADAS].values)
else:
    print("[red]7.- Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS no coinciden.[/red]", df1[PORCENTAJE_ACTAS_CONTABILIZADAS].values)
    print(value_counts6)

if np.array_equal(value_counts7, df1[PORCENTAJE_ACTAS_INCONSISTENCIAS].values):
    print("[green]8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coinciden:[/green]", df1[PORCENTAJE_ACTAS_INCONSISTENCIAS].values)
else:
    print("[red]8.- Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS no coinciden.[/red]", df1[PORCENTAJE_ACTAS_INCONSISTENCIAS].values, "vs", value_counts7)

if np.array_equal(value_counts2, df1[ACTAS_NO_CONTABILIZADAS].values):
    print("[green]9.- Los valores de ACTAS_NO_CONTABILIZADAS coinciden:[/green]", df1[ACTAS_NO_CONTABILIZADAS].values)
else:
    print("[red]9.- Los valores de ACTAS_NO_CONTABILIZADAS no coinciden.[/red]", df1[ACTAS_NO_CONTABILIZADAS].values)
    print(value_counts2)

if np.array_equal(value_counts8, df1[LISTA_NOMINAL_ACTAS_CONTABILIZADAS].values):
    print("[green]10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coinciden:[/green]", df1[LISTA_NOMINAL_ACTAS_CONTABILIZADAS].values)
else:
    print("[red]10.- Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS no coinciden.[/red]", df1[LISTA_NOMINAL_ACTAS_CONTABILIZADAS].values)
    print(value_counts8)

if np.array_equal(value_counts10, df1[TOTAL_VOTOS_C_CS].values):
    print("[green]11.- Los valores de TOTAL_VOTOS_C_CS coinciden:[/green]", df1[TOTAL_VOTOS_C_CS].values)
else:
    print("[red]11.- Los valores de TOTAL_VOTOS_C_CS no coinciden.[/red]", df1[TOTAL_VOTOS_C_CS].values)
    print(value_counts10)

if np.array_equal(value_counts11, df1[TOTAL_VOTOS_S_CS].values):
    print("[green]12.- Los valores de TOTAL_VOTOS_S_CS coinciden:[/green]", df1[TOTAL_VOTOS_S_CS].values)
else:
    print("[red]12.- Los valores de TOTAL_VOTOS_S_CS no coinciden.[/red]", df1[TOTAL_VOTOS_S_CS].values)
    print(value_counts11)

if np.array_equal(value_counts9, df1[PORCENTAJE_PARTICIPACION_CIUDADANA].values):
    print("[green]13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coinciden:[/green]", df1[PORCENTAJE_PARTICIPACION_CIUDADANA].values)
else:
    print("[red]13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA no coinciden.[/red]", df1[PORCENTAJE_PARTICIPACION_CIUDADANA].values)
    print(value_counts9)
