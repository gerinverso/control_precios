import sqlite3
import os
from config import DB_PATH
from modelos.venta import Venta, VentaDetalle

def conectar():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            precio_costo REAL NOT NULL,
            porcentaje_utilidad REAL NOT NULL,
            alicuota_iva REAL NOT NULL,
            precio_venta REAL NOT NULL,
            detalle_extendido TEXT,
            codigo_barras TEXT,
            codigo_producto TEXT
        );
    """)
    # Tabla ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            pago TEXT,
            cliente TEXT,
            total REAL
        );
    """)
    # Tabla ventas_detalle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER,
            producto_id INTEGER,
            descripcion TEXT,
            precio_venta REAL,
            cantidad INTEGER,
            subtotal REAL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id)
        );
    """)
    conn.commit()
    conn.close()

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("Productos en BD:", productos)  # Debug
    conn.close()
    return productos

def buscar_productos(termino):
    conn = conectar()
    cursor = conn.cursor()
    try:
        termino = f"%{termino.lower()}%"
        cursor.execute("""
            SELECT * FROM productos 
            WHERE LOWER(descripcion) LIKE ? 
            OR codigo_barras LIKE ?
            ORDER BY descripcion
        """, (termino, termino))
        return cursor.fetchall()
    finally:
        conn.close()

def verificar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:", tablas)
    
    cursor.execute("PRAGMA table_info(productos)")
    columnas = cursor.fetchall()
    print("Columnas de la tabla productos:", columnas)
    
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("Productos registrados:", productos)
    conn.close()
    return productos

def insertar_producto(descripcion, precio_costo, porcentaje_utilidad, alicuota_iva, 
                    precio_venta, detalle_extendido=None, codigo_barras=None, 
                    codigo_producto=None):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO productos VALUES (
                NULL, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (descripcion, precio_costo, porcentaje_utilidad, alicuota_iva,
            precio_venta, detalle_extendido, codigo_barras, codigo_producto))
        conn.commit()  # Asegurar commit
        print("Producto insertado correctamente")  # Debug
    except Exception as e:
        print("Error al insertar:", e)  # Debug
        conn.rollback()
        raise
    finally:
        conn.close()

def verificar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:", tablas)
    
    cursor.execute("PRAGMA table_info(productos)")
    columnas = cursor.fetchall()
    print("Columnas de la tabla productos:", columnas)
    
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("Productos registrados:", productos)
    conn.close()
    return productos

def eliminar_producto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (int(id),))
    conn.commit()
    conn.close()
    
def editar_producto(id, descripcion, precio_costo, porcentaje_utilidad, alicuota_iva,
                precio_venta, detalle_extendido=None, codigo_barras=None,
                codigo_producto=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos SET
            descripcion = ?,
            precio_costo = ?,
            porcentaje_utilidad = ?,
            alicuota_iva = ?,
            precio_venta = ?,
            detalle_extendido = ?,
            codigo_barras = ?,
            codigo_producto = ?
        WHERE id = ?
    """, (descripcion, float(precio_costo), float(porcentaje_utilidad),
        float(alicuota_iva), float(precio_venta), 
        detalle_extendido, codigo_barras, codigo_producto, int(id)))
    conn.commit()
    conn.close()

def registrar_venta(productos, pago, cliente, total, fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ventas (fecha, pago, cliente, total)
        VALUES (?, ?, ?, ?)
    """, (fecha, pago, cliente, total))
    venta_id = cursor.lastrowid
    for prod in productos:
        cursor.execute("""
            INSERT INTO ventas_detalle (venta_id, producto_id, descripcion, precio_venta, cantidad, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (venta_id, prod["id"], prod["descripcion"], prod["precio_venta"], prod["cantidad"], prod["subtotal"]))
    conn.commit()
    conn.close()

def obtener_ventas_del_dia(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas WHERE fecha LIKE ?", (f"{fecha}%",))
    ventas = [Venta(*row) for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM ventas_detalle WHERE venta_id IN (SELECT id FROM ventas WHERE fecha LIKE ?)", (f"{fecha}%",))
    detalles = [VentaDetalle(*row) for row in cursor.fetchall()]
    conn.close()
    return ventas, detalles

def obtener_ventas_desde(fecha_desde):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas WHERE fecha > ?", (fecha_desde,))
    ventas = [Venta(*row) for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM ventas_detalle WHERE venta_id IN (SELECT id FROM ventas WHERE fecha > ?)", (fecha_desde,))
    detalles = [VentaDetalle(*row) for row in cursor.fetchall()]
    conn.close()
    return ventas, detalles
