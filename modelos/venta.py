class Venta:
    def __init__(self, id, fecha, pago, cliente, total):
        self.id = id
        self.fecha = fecha
        self.pago = pago
        self.cliente = cliente
        self.total = total

class VentaDetalle:
    def __init__(self, id, venta_id, producto_id, descripcion, precio_venta, cantidad, subtotal):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.descripcion = descripcion
        self.precio_venta = precio_venta
        self.cantidad = cantidad
        self.subtotal = subtotal