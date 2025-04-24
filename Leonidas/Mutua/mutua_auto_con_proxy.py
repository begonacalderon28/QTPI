# mutua_auto_con_proxy.py

from playwright.sync_api import sync_playwright
import time
import os
import urllib.parse
import math
import requests
import random

def get_https_proxies():
    """
    Descarga una lista de proxies HTTP(S) gratuitos desde ProxyScrape.
    """
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=true&anonymity=all"
    try:
        resp = requests.get(url, timeout=10)
        lines = [line.strip() for line in resp.text.splitlines() if line.strip()]
        random.shuffle(lines)
        # ProxyScrape devuelve 'ip:puerto'
        return [f"http://{line}" for line in lines]
    except Exception as e:
        print("Error obteniendo proxies:", e)
        return []

def login_and_download_documents(usuario, contraseña, tipo_busqueda, numero_busqueda, ruta_descarga, proxy=None):
    try:
        with sync_playwright() as p:
            # Lanzar Chromium con o sin proxy
            launch_args = {"headless": False}
            if proxy:
                launch_args["proxy"] = {"server": proxy}
            browser = p.chromium.launch(**launch_args)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/123.0.0.0 Safari/537.36",
                java_script_enabled=True,
                accept_downloads=True
            )
            page = context.new_page()

            # Deshabilitar propiedades que delatan automatización
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """)
            
            # Navegar e iniciar sesión
            page.goto("https://www.mutua.es/Expedientes")
            
            page.fill('input[name="username"]', usuario)
            
            page.fill('input[name="password"]', contraseña)
            page.click('input[id="kc-login"]')
            page.wait_for_load_state('networkidle')

            # Comprobación de login
            if not page.is_visible('input[id="buscar"]'):
                print("Error en el login.")
                browser.close()
                return 411

            # Sólo soportamos 'poliza'
            if tipo_busqueda.lower() != 'poliza':
                print("Tipo de búsqueda no soportado.")
                browser.close()
                return 416

            # Búsqueda de póliza
            page.fill('input[id="numPoliza"]', numero_busqueda)
            page.click('input[id="buscar"]')
            page.wait_for_load_state('networkidle')

            try:
                page.wait_for_selector('input[id="verDocumentos"]', timeout=10000)
                page.click('input[id="verDocumentos"]')
                page.wait_for_selector('table#task')
            except:
                print("No se encontró 'Ver documentos'.")
                browser.close()
                return 415

            # Preparar carpeta de descarga
            if not os.path.exists(ruta_descarga):
                os.makedirs(ruta_descarga)

            total_documents = int(page.get_attribute('#tamanoLista', 'value'))
            documents_per_page = 10
            total_pages = math.ceil(total_documents / documents_per_page)
            current_page = 1
            processed_document_ids = set()

            while current_page <= total_pages:
                print(f"Pág {current_page}/{total_pages} (proxy={proxy})")
                page.wait_for_selector('table#task')
                document_rows = page.query_selector_all('table#task tbody tr')

                for row in document_rows:
                    link_element = row.query_selector('td:nth-child(3) a')
                    if not link_element:
                        continue
                    href = link_element.get_attribute('href')
                    if 'document=' not in href:
                        continue
                    start = href.find('document=') + len('document=')
                    end = href.find("','", start)
                    document_id = href[start:end]
                    if document_id in processed_document_ids:
                        continue
                    processed_document_ids.add(document_id)

                    document_name = link_element.inner_text().strip()
                    print(f" Descargando: {document_name} (ID: {document_id})")

                    encoded_url = (
                        f"/Expedientes/showExternalDocument.do?"
                        f"document={urllib.parse.quote(document_id)}&idEntidad={document_id}"
                    )

                    try:
                        with page.expect_download() as download_info:
                            page.evaluate(f"""
                                const url = decodeURIComponent('{encoded_url}');
                                fetch(url, {{ credentials: 'include' }})
                                  .then(r => r.blob())
                                  .then(b => {{
                                    const a = document.createElement('a');
                                    a.href = URL.createObjectURL(b);
                                    a.download = '{document_name}_{document_id}.pdf';
                                    document.body.appendChild(a);
                                    a.click();
                                  }});
                            """)
                        download = download_info.value
                        safe_name = "".join(c if c.isalnum() or c in " .-_()" else "_" for c in document_name)
                        save_path = os.path.join(ruta_descarga, f"{safe_name}_{document_id}.pdf")
                        download.save_as(save_path)
                        print("  → Guardado en:", save_path)
                        time.sleep(2)
                    except Exception as e:
                        print(f" Error descargando {document_id}: {e}")
                        browser.close()
                        return 414

                # Paginación
                if current_page < total_pages:
                    try:
                        next_btn = page.query_selector('a > img[alt="Siguiente"]')
                        if not next_btn:
                            break
                        next_btn.click()
                        page.wait_for_load_state('networkidle')
                        time.sleep(1)
                        current_page += 1
                    except:
                        break
                else:
                    break

            browser.close()
            return 200

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return 412

if __name__ == "__main__":
    usuario    = "A0048012"
    contraseña = "2025-Abr"
    tipo       = "poliza"
    poliza     = "5898992"
    ruta_ds    = "Downloads_prueba"

    proxies = get_https_proxies()
    print(f"Proxies obtenidos: {len(proxies)}. Probando secuencialmente...")

    for proxy in proxies:
        code = login_and_download_documents(usuario, contraseña, tipo, poliza, ruta_ds, proxy)
        if code == 200:
            print("✅ Descarga exitosa con proxy", proxy)
            break
        else:
            print("❌ Proxy falló con código", code)
            time.sleep(3)

    else:
        print("⚠️ Todos los proxies fallaron. Intentando sin proxy...")
        login_and_download_documents(usuario, contraseña, tipo, poliza, ruta_ds)
