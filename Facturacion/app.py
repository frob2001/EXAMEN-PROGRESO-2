from flask import Flask, request, render_template, redirect, url_for, jsonify
import psycopg2
import requests

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = {
    'host': 'localhost',
    'database': 'MyShoppingBack',
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
    return render_template('index.html')

@app.route('/fetch_order', methods=['POST'])
def fetch_order():
    orden_id = request.form.get('orden_id')
    if not orden_id:
        return "No se proporcionó el ID de la orden.", 400

    # Consumir la API
    api_url = f'http://127.0.0.1:5001/orden/{orden_id}'
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return f"Error al consumir la API: {response.text}", 500

    order_data = response.json()

    # Calcular el precio total
    precio_total = sum(producto['cantidad'] * producto['precio'] for producto in order_data['productos'])

    # Crear la factura en la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO factura (orden_id, fecha, precio_total) VALUES (%s, current_date, %s) RETURNING factura_id", (orden_id, precio_total))
    factura_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return render_template('detalles.html', order_data=order_data, factura_id=factura_id, precio_total=precio_total)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
