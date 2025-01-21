import time
import os
from playwright.sync_api import Playwright, sync_playwright

def mutua_propietarios_descarga(usuario: str,
                                contrasena: str,
                                anio: str,
                                siniestro: str,
                                download_path: str) -> int:
    """
    Automatiza la descarga de documentos de Mutua de Propietarios.
    
    Parámetros
    ----------
    usuario : str
        Usuario para login
    contrasena : str
        Contraseña para login
    anio : str
        Año del siniestro a buscar
    siniestro : str
        Número de siniestro a buscar
    download_path : str
        Ruta local para guardar los archivos descargados

    Retorna
    -------
    int
        Código de estado:
            200: Descarga satisfactoria
            411: Error en el login
            412: Página de Mutua de Propietarios está dando errores
            413: El siniestro a buscar está duplicado (No implementado actualmente)
            414: Error descargando algún archivo
            415: Siniestro no encontrado
            416: Tipo de búsqueda no soportado (No se maneja aquí, por si se extiende la lógica)
    """
    try:
        with sync_playwright() as playwright:
            # Lanzar navegador
            try:
                browser = playwright.chromium.launch(headless=True)
            except Exception as e:
                print(f"Error al lanzar Chromium: {e}")
                return 412  # Página con errores (o browser)

            # Crear contexto
            context = browser.new_context(
                accept_downloads=True
            )

            page = context.new_page()

            # Navegar a la URL principal
            try:
                page.goto("https://innova.mutuadepropietarios.es/web/login.jsp")
            except Exception as e:
                print(f"Error cargando la página de login: {e}")
                browser.close()
                return 412

            # 1) Login
            try:
                page.get_by_label("Usuario:").fill(usuario)
                page.get_by_label("Clave:").fill(contrasena)
                page.get_by_role("button", name="Entrar").click()
            except Exception as e:
                print(f"Error en la fase de login: {e}")
                browser.close()
                return 411  # Error en el login

            # Verificar si el login fue exitoso
            time.sleep(2)
            # Si la página no presenta iframe o algún indicio de login OK, devolvemos 411
            if not page.locator("iframe[name=\"cuerpo\"]"):
                print("Parece que no se ha cargado el iframe 'cuerpo'. Posible login fallido.")
                browser.close()
                return 411

            # 2) Navegar hasta la sección de documentos
            try:
                page.locator("iframe[name=\"cuerpo\"]").content_frame.get_by_role("link", name=" Encargos").click()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Varios").check()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").click()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").fill(anio)
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").click()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").fill(siniestro)
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("button", name="Buscar").click()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="").click()
                page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="Documentos").click()
                encargos_frame = page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame
            except Exception as e:
                print(f"Error navegando a la sección de documentos: {e}")
                browser.close()
                return 415  # Siniestro no encontrado, 
                           # (o podría ser otra causa, ajusta si lo deseas)

            # Esperar a que aparezcan los links de descarga
            time.sleep(3)

            # 3) Localizar los enlaces con title="Descargar"
            try:
                links = encargos_frame.locator('a[title="Descargar"]')
                total_links = links.count()
            except Exception as e:
                print(f"Error localizando enlaces con title='Descargar': {e}")
                browser.close()
                return 412  # Error general

            if total_links == 0:
                print("No se encontraron enlaces con title='Descargar'.")
                browser.close()
                return 415  # Siniestro no encontrado (sin docs)

            print(f"Encontrados {total_links} enlaces con 'title=Descargar'.")

            # 4) Descarga secuencial de cada archivo con expect_download()
            def on_download(download):
                try:
                    suggested_name = download.suggested_filename or "archivo_sin_nombre.pdf"
                    # Forzar extensión .pdf si no la tiene
                    base, extension = os.path.splitext(suggested_name)
                    if not extension.lower().endswith(".pdf"):
                        extension = ".pdf"

                    # Construir primera ruta tentativa
                    final_path = os.path.join(download_path, base + extension)
                    
                    # Si existe, agregar sufijo (1), (2), etc. para evitar sobreescritura
                    counter = 1
                    while os.path.exists(final_path):
                        final_path = os.path.join(download_path, f"{base}({counter}){extension}")
                        counter += 1

                    # Guardar el archivo con el nombre único
                    download.save_as(final_path)
                    print(f"Descargado: {final_path}")
                except Exception as e:
                    print(f"Error descargando archivo: {e}")
                    return 414
                    # Manejo de errores adicional si lo deseas


            page.on("download", on_download)

            for i in range(total_links):
                try:
                    with page.expect_download() as download_info:
                        links.nth(i).click()
                    _ = download_info.value  # 'on_download' se encarga del guardado
                except Exception as e:
                    print(f"Error en la descarga del archivo {i+1}: {e}")
                    # Si consideras crítico, cierra y devuelves 414
                    browser.close()
                    return 414

            # 5) Esperar si es necesario
            time.sleep(2)

            # Cerrar todo
            context.close()
            browser.close()
            return 200  # Descarga satisfactoria

    except Exception as e:
        print(f"Excepción inesperada: {e}")
        return 412  # Página con errores o excepción genérica

# Ejemplo de uso:
if __name__ == "__main__":
    codigo = mutua_propietarios_descarga(
        usuario="AB_SCGMABO",
        contrasena="Eneroinvierno2025.*",
        anio="2024",
        siniestro="4041692",
        download_path=r"C:\QTPI\Leonidas\Mutua_propietarios\descargas-test2"
    )
    print(f"Código de retorno: {codigo}")
