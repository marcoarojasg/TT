from flask import Flask, jsonify
import json
import random
import string
import plotly.express as px

app = Flask(__name__)

""" Genera una dirección de correo electrónico aleatoria.
    Parámetros:    Ninguno
    Devoluciones:    str: una dirección de correo electrónico generada aleatoriamente.    """
def generar_correo():
    usuario = ''.join(random.choices(string.ascii_lowercase, k=8))
    dominio = random.choice(['@gmail.com', '@hotmail.com'])
    return usuario + dominio

"""    Genera una contraseña aleatoria de longitud aleatoria entre 6 y 10 caracteres utilizando una combinación de letras y dígitos.    """
def generar_contrasena():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 10)))

"""    Esta función genera un registro aleatorio llamando a las funciones 'generar_correo' y 'generar_contrasena' para crear un correo electrónico y una contraseña. Luego devuelve un diccionario que contiene el correo electrónico y la contraseña.    """
def generar_registro():
    correo = generar_correo()
    contrasena = generar_contrasena()
    return {"email": correo, "clave": contrasena}

"""    Genera un JSON con un número determinado de registros.
    :param num_registros: el número de registros a generar.
    :return: una lista de registros generados.    """
def generar_json(num_registros):
    registros = [generar_registro() for _ in range(num_registros)]
    return registros

"""    Analiza los datos proporcionados para contar las apariciones de dominios de correo electrónico y la cantidad de contraseñas con más de 8 caracteres.
    Parámetros:
    datos (lista): una lista de diccionarios que representan los datos que se van a analizar. Cada diccionario debe contener claves de 'correo electrónico' y 'clave'.
    Devoluciones:
    tupla: una tupla que contiene las ocurrencias de dominio y el recuento de contraseñas con más de 8 caracteres.    """
def analisis_datos(data):
    dominios = {'@gmail.com': 0, '@hotmail.com': 0}
    claves_mas_8_caracteres = 0

    for registro in data:
        dominio = registro['email'].split('@')[1]
        if dominio in dominios:
            dominios[dominio] += 1
        if len(registro['clave']) > 8:
            claves_mas_8_caracteres += 1

    return dominios, claves_mas_8_caracteres

"""    Genera gráficos circulares y de barras basados ​​en los dominios proporcionados y el recuento de contraseñas con más de 8 caracteres.    """
def generar_graficos(dominios, claves_mas_8_caracteres):
    fig_dominios = px.pie(names=list(dominios.keys()), values=list(dominios.values()), title='Dominios de Correo')
    fig_claves = px.bar(x=['Claves > 8 caracteres'], y=[claves_mas_8_caracteres], title='Claves > 8 Caracteres')

    return fig_dominios, fig_claves

"""    Ruta para generar registros con una cantidad específica de registros y guardarlos en un archivo JSON.    """
@app.route('/generar_registros', methods=['GET'])
def generar_registros():
    num_registros = 500000
    registros = generar_json(num_registros)
    
    with open("registros_aleatorios.json", "w") as file:
        json.dump(registros, file, indent=2)

    return jsonify({"message": f"Archivo 'registros_aleatorios.json' creado con {num_registros} registros."})

"""    Endpoint para el manejo de solicitudes a '/analisis_datos'. Recupera datos de 'registros_aleatorios.json',
    realiza análisis, genera gráficos y devuelve una respuesta JSON con un mensaje.    """
@app.route('/analisis_datos', methods=['GET'])
def analisis_datos_endpoint():
    with open("registros_aleatorios.json", "r") as file:
        data = json.load(file)

    dominios, claves_mas_8_caracteres = analisis_datos(data)

    fig_dominios, fig_claves = generar_graficos(dominios, claves_mas_8_caracteres)

    fig_dominios.write_html("grafico_dominios.html")
    fig_claves.write_html("grafico_claves.html")

    return jsonify({"message": "Análisis de datos y gráficos generados."})

"""    Ruta para la obtención de la gráfica de dominios. Maneja solicitudes GET.
    Abre y lee el archivo 'grafico_dominios.html' y devuelve su contenido.    """
@app.route('/grafico_dominios', methods=['GET'])
def obtener_grafico_dominios():
    with open("grafico_dominios.html", "r") as file:
        return file.read()
    
"""    Ruta para la obtención de una gráfica de claves. Utiliza el método GET. Lee y devuelve el contenido del archivo "grafico_claves.html".    """
@app.route('/grafico_claves', methods=['GET'])
def obtener_grafico_claves():
    with open("grafico_claves.html", "r") as file:
        return file.read()

if __name__ == "__main__":
    app.run(debug=True)
