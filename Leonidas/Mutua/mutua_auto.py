# mutua_auto.py

from playwright.sync_api import sync_playwright
import time
import os
import urllib.parse
import math

def login_and_download_documents(usuario, contraseña, tipo_busqueda, numero_busqueda, ruta_descarga):
    try:
        with sync_playwright() as p:
            # Crear el navegador y el contexto
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                java_script_enabled=True,
                
                accept_downloads=True
            )
            page = context.new_page()

            # Deshabilitar propiedades que delatan automatización
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """)

            # Navegar a la página de inicio
            page.goto("https://www.mutua.es/Expedientes")
            time.sleep(2)

            # Completar el formulario de inicio de sesión
            page.fill('input[name="username"]', usuario)
            time.sleep(3)
            page.fill('input[name="password"]', contraseña)
            page.click('input[id="kc-login"]')
           
            # Esperar a que la página cargue después del inicio de sesión
            page.wait_for_load_state('networkidle')

            

            # Verificar si el login fue exitoso
            if page.is_visible('input[id="buscar"]'):
                pass  # Login exitoso
            else:
                print("Error en el login.")
                browser.close()
                return 411  # Error en el login

          

            # Verificar si el tipo de búsqueda es 'Póliza'
            if tipo_busqueda.lower() != 'poliza':
                print("Tipo de búsqueda no soportado en este momento.")
                browser.close()
                return 416  # Tipo de búsqueda no soportado

            # Completar el formulario de búsqueda de póliza
            page.fill('input[id="numPoliza"]', numero_busqueda)
            page.click('input[id="buscar"]')

            # Esperar a que se carguen los resultados
            page.wait_for_load_state('networkidle')

            # Hacer clic en el botón 'Ver documentos'
            try:
                page.wait_for_selector('input[id="verDocumentos"]', timeout=10000)
                page.click('input[id="verDocumentos"]')
                # Esperar a que la tabla de documentos aparezca
                page.wait_for_selector('table#task')
            except:
                print("No se encontró el botón de 'Ver documentos'.")
                browser.close()
                return 415  # Siniestro no encontrado

            # Crear carpeta para guardar documentos
            download_dir = ruta_descarga
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # Obtener el número total de documentos
            total_documents = int(page.get_attribute('#tamanoLista', 'value'))
            print(f"Total de documentos a descargar: {total_documents}")

            # Calcular el número de páginas (asumiendo 10 documentos por página)
            documents_per_page = 10
            total_pages = math.ceil(total_documents / documents_per_page)
            current_page = 1

            # Mantener un conjunto de IDs de documentos procesados para evitar duplicados
            processed_document_ids = set()

            while current_page <= total_pages:
                print(f"Procesando página {current_page} de {total_pages}")

                # Esperar a que se cargue la tabla de documentos
                page.wait_for_selector('table#task')

                # Extraer información de los documentos en la página actual
                document_rows = page.query_selector_all('table#task tbody tr')

                for row in document_rows:
                    # Extraer el enlace del documento
                    link_element = row.query_selector('td:nth-child(3) a')
                    if link_element:
                        onclick_attr = link_element.get_attribute('href')
                        # Extraer el ID del documento de la función JavaScript
                        document_id = None
                        if 'openDocWinWindowName' in onclick_attr:
                            # Obtener el valor del parámetro 'document' en la URL
                            start = onclick_attr.find('document=') + len('document=')
                            end = onclick_attr.find("','", start)
                            document_id = onclick_attr[start:end]

                        if document_id and document_id not in processed_document_ids:
                            processed_document_ids.add(document_id)

                            # Obtener el nombre del documento
                            document_name = link_element.inner_text().strip()
                            print(f"Descargando documento: {document_name} (ID: {document_id})")

                            # Construir la URL codificada del documento
                            encoded_url = f'/Expedientes/showExternalDocument.do?document={urllib.parse.quote(document_id)}&idEntidad={document_id}'

                            # Decodificar la URL
                            decoded_url = urllib.parse.unquote(encoded_url)

                            # Manejar la descarga usando expect_download
                            try:
                                with page.expect_download() as download_info:
                                    # Ejecutar el script JavaScript en el contexto de la página para iniciar la descarga
                                    js_script = f"""
                                    const encodedUrl = '{encoded_url}';
                                    const decodedUrl = decodeURIComponent(encodedUrl);
                                    fetch(decodedUrl, {{
                                        method: 'GET',
                                        credentials: 'include',
                                    }})
                                    .then(response => {{
                                        if (!response.ok) {{
                                            throw new Error('Error al descargar el archivo: ' + response.statusText);
                                        }}
                                        return response.blob();
                                    }})
                                    .then(blob => {{
                                        const downloadLink = document.createElement('a');
                                        const url = window.URL.createObjectURL(blob);
                                        downloadLink.href = url;
                                        downloadLink.download = '{document_name}_{document_id}';  // Puedes cambiar el nombre aquí
                                        document.body.appendChild(downloadLink);
                                        downloadLink.click();
                                        setTimeout(() => {{
                                            window.URL.revokeObjectURL(url);
                                            downloadLink.remove();
                                        }}, 1000);
                                    }})
                                    .catch(err => console.error('Error:', err));
                                    """
                                    # Ejecutar el script
                                    page.evaluate(js_script)

                                # Obtener el objeto de descarga
                                download = download_info.value

                                # Sanitizar el nombre del documento
                                safe_document_name = "".join(c if c.isalnum() or c in " .-_()" else "_" for c in document_name).rstrip()

                                # Usar siempre la extensión '.pdf' ya que todos los archivos son PDFs
                                file_extension = '.pdf'

                                # Construir el nombre final del archivo
                                save_filename = f"{safe_document_name}_{document_id}{file_extension}"
                                save_path = os.path.join(download_dir, save_filename)

                                # Guardar el archivo descargado
                                download.save_as(save_path)
                                print(f"Documento guardado en: {save_path}")
                            except Exception as e:
                                print(f"Error al descargar el documento {document_name} (ID: {document_id}): {e}")
                                browser.close()
                                return 414  # Error descargando algún archivo
                        else:
                            print(f"Documento con ID {document_id} ya procesado o no válido.")

                if current_page < total_pages:
                    # Intentar encontrar el botón o enlace 'Siguiente' para la paginación
                    try:
                        # Verificar si hay un enlace con un icono de 'Siguiente' habilitado
                        next_button = page.query_selector('a > img[alt="Siguiente"]')
                        if next_button:
                            # Hacer clic en el enlace 'Siguiente'
                            next_button.click()
                            # Esperar a que se cargue la nueva página
                            page.wait_for_load_state('networkidle')
                            time.sleep(1)
                            current_page += 1
                        else:
                            # No hay más páginas
                            print("No hay más páginas.")
                            break
                    except Exception as e:
                        # No hay más páginas
                        print(f"No hay más páginas. Error: {e}")
                        break
                else:
                    print("Se han procesado todas las páginas.")
                    break

            # Cerrar el navegador
            browser.close()
            return 200  # Descarga satisfactoria

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return 412  # Página de mutua.es está dando errores

# Ejemplo de uso (para pruebas, puedes descomentar y ajustar los parámetros)
# resultado = login_and_download_documents('usuario', 'contraseña', 'Póliza', '44091', '/ruta/de/descarga')
# print(f"Código de resultado: {resultado}")
if __name__ == "__main__":
    usuario = "A0048012"
    psswd = "2025-Abr"
    tipo= "poliza"
    poliza = "5898992"
    ruta_ds = "Downloads_prueba"
    login_and_download_documents(usuario, psswd, tipo, poliza, ruta_ds)