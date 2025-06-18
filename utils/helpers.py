def es_flotante(valor):
    if valor is None:
        return False
    try:
        # Reemplazar comas por puntos para soportar ambos formatos decimales
        valor_limpio = str(valor).replace(',', '.')
        float(valor_limpio)
        return True
    except (ValueError, TypeError):
        return False

def es_entero(valor):
    if valor is None:
        return False
    try:
        int(valor)
        return True
    except (ValueError, TypeError):
        return False