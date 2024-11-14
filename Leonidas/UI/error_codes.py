# error_codes.py

def get_error_message(error_code):
    error_messages = {
        200: "Descarga satisfactoria",
        411: "Error en el login",
        412: "Página de mutua.es está dando errores",
        413: "El siniestro a buscar está duplicado",
        414: "Error descargando algún archivo",
        415: "Siniestro no encontrado",
        416: "Tipo de búsqueda no soportado",
    }
    return error_messages.get(error_code, "Código de error desconocido")
