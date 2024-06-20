from flask import Flask, request, render_template, redirect, url_for, jsonify
import psycopg2
import pandas as pd
from io import BytesIO

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

@app.route('/', methods=['GET'])
def get_productos_html():
    return render_template('productos.html', productos=get_productos())

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file.filename.endswith('.csv'):
        try:
            data = pd.read_csv(file)
            conn = get_db_connection()
            cur = conn.cursor()
            order_ids = []

            for index, row in data.iterrows():
                nombre = row['Nombre del cliente']
                cedula = str(row['Cédula de identidad'])
                direccion = row['Dirección']
                productos_str = row['Productos']

                # Verificar si el cliente ya existe
                cur.execute("SELECT cliente_id FROM clientes WHERE cedula = %s", (cedula,))
                cliente = cur.fetchone()

                if cliente is None:
                    # Insertar nuevo cliente
                    cur.execute(
                        "INSERT INTO clientes (nombre, cedula, direccion) VALUES (%s, %s, %s) RETURNING cliente_id",
                        (nombre, cedula, direccion)
                    )
                    cliente_id = cur.fetchone()[0]
                else:
                    cliente_id = cliente[0]

                # Insertar nueva orden de compra
                cur.execute("INSERT INTO orden_compra (cliente_id) VALUES (%s) RETURNING orden_id", (cliente_id,))
                orden_id = cur.fetchone()[0]
                order_ids.append(orden_id)

                # Insertar productos en la orden y actualizar la cantidad en productos
                productos_list = productos_str.split(';')
                for producto in productos_list:
                    producto_id, cantidad = map(int, [x.split(':')[1].strip() for x in producto.split(',')])
                    cur.execute(
                        "INSERT INTO orden_producto (orden_id, producto_id, cantidad) VALUES (%s, %s, %s)",
                        (orden_id, producto_id, cantidad)
                    )
                    cur.execute(
                        "UPDATE productos SET cantidad = cantidad - %s WHERE producto_id = %s AND cantidad >= %s",
                        (cantidad, producto_id, cantidad)
                    )
                    if cur.rowcount == 0:
                        raise Exception(f"No hay suficiente cantidad del producto con ID {producto_id}")

            conn.commit()
            cur.close()
            conn.close()
            message = f"Datos subidos exitosamente. ID de las ordenes de compra: {', '.join(map(str, order_ids))}"
        except Exception as e:
            message = f"Error al subir datos: {str(e)}"
    else:
        message = "Formato de archivo no soportado"

    return render_template('productos.html', productos=get_productos(), message=message)

def get_productos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    productos_list = []
    for producto in productos:
        productos_list.append({
            'producto_id': producto[0],
            'nombre': producto[1],
            'descripcion': producto[2],
            'cantidad': producto[3]
        })
    
    return productos_list

@app.route('/orden/<int:orden_id>', methods=['GET'])
def get_orden(orden_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT oc.orden_id, c.nombre, c.cedula, c.direccion, op.producto_id, p.nombre, p.descripcion, op.cantidad, p.precio
        FROM orden_compra oc
        JOIN clientes c ON oc.cliente_id = c.cliente_id
        JOIN orden_producto op ON oc.orden_id = op.orden_id
        JOIN productos p ON op.producto_id = p.producto_id
        WHERE oc.orden_id = %s
    ''', (orden_id,))
    orden_data = cur.fetchall()
    cur.close()
    conn.close()
    
    if not orden_data:
        return jsonify({"error": "Orden no encontrada"}), 404

    factura = {
        "orden_id": orden_data[0][0],
        "cliente": {
            "nombre": orden_data[0][1],
            "cedula": orden_data[0][2],
            "direccion": orden_data[0][3]
        },
        "productos": [
            {
                "producto_id": row[4],
                "nombre": row[5],
                "descripcion": row[6],
                "cantidad": row[7],
                "precio": float(row[8])
            } for row in orden_data
        ]
    }

    return jsonify(factura)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
