from flask import Flask, request, render_template, send_file
import psycopg2
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = {
    'host': 'localhost',
    'database': 'MyShopping',
    'user': 'postgres',
    'password': 'Felixpro2510'
}

def get_db_connection():
    conn = psycopg2.connect(
        host=DATABASE['host'],
        database=DATABASE['database'],
        user=DATABASE['user'],
        password=DATABASE['password']
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT producto_id, nombre, descripcion, imagen_url, precio FROM productos')
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/comprar', methods=['POST'])
def comprar():
    data = request.form
    productos_seleccionados = data.getlist('producto_id')
    nombre_cliente = data['nombre_cliente']
    cedula_identidad = data['cedula_identidad']
    direccion = data['direccion']

    productos_data = []

    for producto_id in productos_seleccionados:
        cantidad = data.get(f'cantidad_{producto_id}')
        productos_data.append({
            'producto_id': producto_id,
            'cantidad': cantidad
        })

    cliente_info = {
        'nombre_cliente': nombre_cliente,
        'cedula_identidad': cedula_identidad,
        'direccion': direccion,
        'productos': productos_data
    }

    # Crear CSV con una estructura mejorada
    productos_str = '; '.join([f"ID: {p['producto_id']}, Cantidad: {p['cantidad']}" for p in productos_data])
    csv_data = [[nombre_cliente, cedula_identidad, direccion, productos_str]]

    df = pd.DataFrame(csv_data, columns=['Nombre del cliente', 'Cédula de identidad', 'Dirección', 'Productos'])
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_buffer.seek(0)

    return send_file(csv_buffer, mimetype='text/csv', download_name='pedido.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
