from flask import Flask, render_template, request, jsonify
import json
import random
import string

app = Flask(__name__)

def generar_correo():
    usuario = ''.join(random.choices(string.ascii_lowercase, k=8))
    dominio = random.choice(['@gmail.com', '@hotmail.com'])
    return usuario + dominio

def generar_contrasena():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 10)))

def generar_registro():
    correo = generar_correo()
    contrasena = generar_contrasena()
    return {"email": correo, "password": contrasena}

def generar_json(num_registros):
    registros = [generar_registro() for _ in range(num_registros)]
    return registros

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_registros', methods=['POST'])
def generar_registros():
    num_registros = int(request.form['num_registros'])
    registros = generar_json(num_registros)
    
    with open("registros_aleatorios.json", "w") as file:
        json.dump(registros, file, indent=2)

    return render_template('index.html', mensaje=f"Archivo 'registros_aleatorios.json' creado con {num_registros} registros.")

@app.route('/analisis_datos', methods=['GET'])
def analisis_datos():
    with open("registros_aleatorios.json", "r") as file:
        data = json.load(file)

    dominios = {'@gmail.com': 0, '@hotmail.com': 0}
    contrasenas_mas_8_caracteres = 0

    for registro in data:
        dominio = registro['email'].split('@')[1]
        if dominio in dominios:
            dominios[dominio] += 1
        if len(registro['password']) > 8:
            contrasenas_mas_8_caracteres += 1

    resultado = {
        "dominios": dominios,
        "contrasenas_mas_8_caracteres": contrasenas_mas_8_caracteres
    }

    return render_template('index.html', resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
