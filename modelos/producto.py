class Producto:
    def __init__(self, id, descripcion, precio_costo, porcentaje_utilidad, 
                alicuota_iva, precio_venta, detalle_extendido=None, 
                codigo_barras=None, codigo_producto=None):
        self.id = id
        self.descripcion = descripcion
        self.precio_costo = precio_costo
        self.porcentaje_utilidad = porcentaje_utilidad
        self.alicuota_iva = alicuota_iva
        self.precio_venta = precio_venta
        self.detalle_extendido = detalle_extendido
        self.codigo_barras = codigo_barras
        self.codigo_producto = codigo_producto