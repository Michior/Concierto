from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json

app = Flask(__name__)

# Carga el archivo Excel al iniciar la app
# Cambia 'boletos.xlsx' por el nombre de tu archivo si es diferente
try:
    df = pd.read_excel('./boletos.xlsm')
except FileNotFoundError as e:
    df = None
    print(f"Archivo no encontrado: {e}")
except ValueError as e:
    df = None
    print(f"Error al leer el archivo Excel: {e}")

# Carga solo la hoja 'Datos' del archivo Excel al iniciar la app
try:
    df = pd.read_excel('./boletos.xlsm', sheet_name='Datos')
except FileNotFoundError as e:
    df = None
    print(f"Archivo no encontrado: {e}")
except ValueError as e:
    df = None
    print(f"Error al leer la hoja 'Datos' del archivo Excel: {e}")

# Cargar boletos validados desde un archivo JSON al iniciar la app
try:
    with open('boletos_validados.json', 'r', encoding='utf-8') as json_file:
        boletos_validados = json.load(json_file)
except FileNotFoundError:
    boletos_validados = {}
except json.JSONDecodeError:
    boletos_validados = {}

def buscar_boleto(numero_entrada):
    """
    Busca el boleto por 'Número de entrada vendida' en la hoja 'Datos'.
    Retorna un diccionario con la información si lo encuentra, o None si no existe.
    También agrega el estado de validación desde el JSON.
    """
    if df is None:
        return None
    resultado = df[df['Número de entrada vendida'] == int(numero_entrada)]
    if not resultado.empty:
        boleto_info = resultado.iloc[0].to_dict()
        # Add validation status from JSON
        boleto_info['Estado'] = boletos_validados.get(str(numero_entrada), {}).get('Estado', 'No validado')
        return boleto_info
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal. Muestra el formulario y el resultado de la búsqueda.
    """
    info = None
    no_encontrado = False
    mensaje = request.args.get('mensaje')  # Obtener el mensaje de la query string
    estado_validacion = None  # Variable para almacenar el estado del boleto

    if request.method == 'POST':
        numero_entrada = request.form['correlativo']
        info = buscar_boleto(numero_entrada)
        if info is None:
            no_encontrado = True
        else:
            # Verificar el estado de validación desde el JSON
            estado_validacion = boletos_validados.get(str(numero_entrada), {}).get('Estado', 'No validado')
            info['Estado'] = estado_validacion  # Agregar el estado a la información del boleto

    return render_template(
        'index.html',
        info=info,
        no_encontrado=no_encontrado,
        boletos_validados=boletos_validados,
        mensaje=mensaje,
        estado_validacion=estado_validacion
    )

# Ruta para validar el boleto
@app.route('/validar', methods=['POST'])
def validar():
    numero_entrada = request.form.get('numero_entrada')
    if not numero_entrada:
        return render_template('index.html', info=None, mensaje="Número de entrada no proporcionado.")

    info = buscar_boleto(numero_entrada)
    mensaje = None
    if info:
        if str(numero_entrada) in boletos_validados:  # Verificar si ya está validado
            mensaje = f"El boleto número {numero_entrada} ya fue validado anteriormente."
        else:
            # Actualizar el estado del boleto a "Validado"
            info['Estado'] = 'Validado'
            boletos_validados[str(numero_entrada)] = info  # Guardar el boleto en el JSON

            mensaje = f"El boleto número {numero_entrada} ha sido validado correctamente."

            # Guardar los boletos validados en un archivo Excel
            try:
                boletos_df = pd.DataFrame([
                    {**value, 'Estado': 'Validado'} for value in boletos_validados.values()
                ])
                boletos_df.to_excel('boletos_validados.xlsx', index=False)
            except Exception as e:
                mensaje += f" Sin embargo, ocurrió un error al guardar en el archivo Excel: {e}"

            # Guardar los boletos validados en un archivo JSON
            try:
                boletos_serializables = {
                    key: {k: (str(v) if isinstance(v, pd.Timestamp) else v) for k, v in value.items()}
                    for key, value in boletos_validados.items()
                }
                with open('boletos_validados.json', 'w', encoding='utf-8') as json_file:
                    json.dump(boletos_serializables, json_file, ensure_ascii=False, indent=4)
            except Exception as e:
                mensaje += f" Sin embargo, ocurrió un error al guardar en el archivo JSON: {e}"

    else:
        mensaje = f"El boleto número {numero_entrada} no existe o no fue vendido."

    # Redirigir a la página principal con un mensaje
    return redirect(url_for('index', mensaje=mensaje))

if __name__ == '__main__':
    app.run(debug=True)