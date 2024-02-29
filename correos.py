import json
import random
import string

def generar_correo():
    usuario = ''.join(random.choices(string.ascii_lowercase, k=8))  # Usuario aleatorio de 8 caracteres
    dominio = random.choice(['@gmail.com', '@hotmail.com'])  # Selecciona aleatoriamente el dominio
    return usuario + dominio

def generar_contrasena():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 10)))

def generar_registro():
    correo = generar_correo()
    contrasena = generar_contrasena()
    return {"email": correo, "password": contrasena}

def generar_json(num_registros):
    registros = [generar_registro() for _ in range(num_registros)]
    return json.dumps(registros, indent=2)

if __name__ == "__main__":
    num_registros = 500000
    json_data = generar_json(num_registros)

    with open("registros_aleatorios.json", "w") as file:
        file.write(json_data)

    print(f"Se ha creado el archivo 'registros_aleatorios.json' con {num_registros} registros aleatorios.")
