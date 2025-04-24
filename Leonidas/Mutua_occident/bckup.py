import os
import time
from playwright.sync_api import sync_playwright, expect

def ensure_subdir(subdir):
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    return subdir

def minimize_and_move_page(page):
    """
    Minimiza la ventana y la mueve a la posición (-1000, -1000) usando el protocolo CDP.
    """
    try:
        cdp_session = page.context.new_cdp_session(page)
        target_info = cdp_session.send("Browser.getWindowForTarget")
        window_id = target_info["windowId"]
        cdp_session.send("Browser.setWindowBounds", {
            "windowId": window_id,
            "bounds": {
                "windowState": "minimized",
                "left": -1000,
                "top": -1000
            }
        })
    except Exception as e:
        print("Error al minimizar y mover la ventana:", e)

def download_informes(page, base_dir):
    subdir = ensure_subdir(os.path.join(base_dir, "informes"))
    table_selector = "table#ListadoInformes tbody tr"
    page.wait_for_selector(table_selector, timeout=10000)
    rows = page.locator(table_selector)
    count = rows.count()
    print(f"[Informes] Encontradas {count} filas")
    
    for i in range(count):
        row = rows.nth(i)
        link = row.locator("a").nth(1)
        file_name = link.inner_text().strip()
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        print(f"[Informes] Descargando fila {i+1}: {file_name}")
        
        with page.expect_popup() as popup_info:
            link.click()
        new_page = popup_info.value
        time.sleep(0.5)  # Espera para que el popup se inicialice
        minimize_and_move_page(new_page)
        
        with new_page.expect_download() as download_info:
            new_page.evaluate("""() => {
                const a = document.createElement('a');
                a.href = window.location.href;
                a.download = 'archivo.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }""")
        download = download_info.value
        save_path = os.path.join(subdir, file_name)
        download.save_as(save_path)
        print(f"[Informes] Guardado en: {save_path}")
        new_page.close()

def download_docs_recibidos(page, base_dir):
    subdir = ensure_subdir(os.path.join(base_dir, "docs_recibidos"))
    table_selector = "table#grDocsCia tbody tr"
    page.wait_for_selector(table_selector, timeout=10000)
    rows = page.locator(table_selector)
    count = rows.count()
    print(f"[Docs. recibidos] Encontradas {count} filas")
    
    for i in range(count):
        row = rows.nth(i)
        link = row.locator("a").first
        file_name = link.inner_text().strip()
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        print(f"[Docs. recibidos] Descargando fila {i+1}: {file_name}")
        
        with page.expect_popup() as popup_info:
            link.click()
        new_page = popup_info.value
        time.sleep(0.5)
        minimize_and_move_page(new_page)
        
        with new_page.expect_download() as download_info:
            new_page.evaluate("""() => {
                const a = document.createElement('a');
                a.href = window.location.href;
                a.download = 'archivo.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }""")
        download = download_info.value
        save_path = os.path.join(subdir, file_name)
        download.save_as(save_path)
        print(f"[Docs. recibidos] Guardado en: {save_path}")
        new_page.close()

def download_docs_añadidos(page, base_dir):
    subdir = ensure_subdir(os.path.join(base_dir, "docs_añadidos"))
    try:
        page.wait_for_selector("table#grDocs", state="visible", timeout=10000)
    except Exception as e:
        print("No se encontró la tabla con id 'grDocs':", e)
        return

    try:
        page.wait_for_selector("table#grDocs tbody tr", state="visible", timeout=10000)
    except Exception as e:
        print("No se encontraron filas en 'table#grDocs tbody tr':", e)
        return

    rows = page.locator("table#grDocs tbody tr")
    count = rows.count()
    print(f"[Docs. añadidos] Encontradas {count} filas en table#grDocs tbody tr")

    for i in range(count):
        row = rows.nth(i)
        link = row.locator("a").first
        file_name = link.inner_text().strip()
        if not file_name:
            file_name = f"doc_añadidos_{i+1}.pdf"
        elif not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        print(f"[Docs. añadidos] Descargando fila {i+1}: {file_name}")

        with page.expect_popup() as popup_info:
            link.click()
        new_page = popup_info.value
        time.sleep(0.5)
        minimize_and_move_page(new_page)
        
        with new_page.expect_download() as download_info:
            new_page.evaluate("""() => {
                const a = document.createElement('a');
                a.href = window.location.href;
                a.download = 'archivo.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }""")
        download = download_info.value
        save_path = os.path.join(subdir, file_name)
        download.save_as(save_path)
        print(f"[Docs. añadidos] Guardado en: {save_path}")
        new_page.close()

def download_docs_prof(page, base_dir):
    subdir = ensure_subdir(os.path.join(base_dir, "docs_prof_intervinientes"))
    table_selector = "table#GrDocumentos tbody tr"
    page.wait_for_selector(table_selector, timeout=10000)
    rows = page.locator(table_selector)
    count = rows.count()
    print(f"[Docs. prof. intervinientes] Encontradas {count} filas")
    
    for i in range(count):
        row = rows.nth(i)
        link = row.locator("a").first
        file_name = link.inner_text().strip()
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        print(f"[Docs. prof. intervinientes] Descargando fila {i+1}: {file_name}")
        
        with page.expect_popup() as popup_info:
            link.click()
        new_page = popup_info.value
        time.sleep(0.5)
        minimize_and_move_page(new_page)
        
        with new_page.expect_download() as download_info:
            new_page.evaluate("""() => {
                const a = document.createElement('a');
                a.href = window.location.href;
                a.download = 'archivo.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }""")
        download = download_info.value
        save_path = os.path.join(subdir, file_name)
        download.save_as(save_path)
        print(f"[Docs. prof. intervinientes] Guardado en: {save_path}")
        new_page.close()

def run_script(playwright, usuario, contrasena, siniestro, download_path):
    base_dir = download_path
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    browser = None
    context = None
    try:
        browser = playwright.chromium.launch(
            headless=False, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-minimized",
                "--window-position=-1000,-1000",
                "--window-size=1920,1080"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
        )
        context.grant_permissions(["notifications"])

        page = context.new_page()
        page.goto("https://portalprepersa.gco.global/")
        page.goto("https://ssoaut.gco.global/x-vdesk/hangup.php3?return=aHR0cHM6Ly9wb3J0YWxhcGkxLmdjby5nbG9iYWwvbG9naW4vP2Q9aHR0cHMlM0ElMkYlMkZwb3J0YWxwcmVwZXJzYS5nY28uZ2xvYmFsJTJG")
        page.goto("https://ssoaut.gco.global/my.policy?apm=3")
        page.get_by_placeholder("Usuario").click()
        page.get_by_placeholder("Usuario").fill(usuario)
        page.get_by_placeholder("Clave").click()
        page.get_by_placeholder("Clave").fill(contrasena)
        
        with page.expect_popup() as page1_info:
            page.get_by_role("button", name="Logon").click()
        page1 = page1_info.value
        page1.close()
        page.get_by_text("Pulsa aquí para continuar sin").click()
        
        page.get_by_label("Prepersa.Net").click()
        with page.expect_popup() as page2_info:
            page.get_by_role("link", name="Búsqueda de encargos").click()
        page2 = page2_info.value
        page2.get_by_title("En curso").click()
        page2.get_by_role("treeitem", name="Todos").click()
        page2.get_by_title("Nº Siniestro\\Inspección", exact=True).click()
        page2.get_by_role("treeitem", name="Nº Siniestro\\Inspección").click()
        page2.get_by_role("textbox", name="Nº Siniestro\\Inspección: *").click()
        page2.get_by_role("textbox", name="Nº Siniestro\\Inspección: *").click()
        page2.get_by_role("textbox", name="Nº Siniestro\\Inspección: *").fill(siniestro)
        page2.get_by_role("button", name="Buscar").click()
        ver_button = page2.locator("td.icon-grid-avanzado a[name='GridResultados']").first
        ver_button.wait_for(state="visible", timeout=5000)
        ver_button.click()
        page2.get_by_text("Acciones", exact=True).click()
        page2.get_by_role("link", name="Documentación").click()
        
        print("Descargando documentos de la sección Informes...")
        download_informes(page2, base_dir)
        
        print("Descargando documentos de la sección Docs. añadidos...")
        page2.locator("ul.cat-nav.cat-nav-list li a:has-text('Docs. añadidos')").click()
        download_docs_añadidos(page2, base_dir)
        
        print("Descargando documentos de la sección Docs. recibidos...")
        page2.locator("ul.cat-nav.cat-nav-list li a:has-text('Docs. recibidos')").click()
        download_docs_recibidos(page2, base_dir)
        
        print("Descargando documentos de la sección Docs. prof. intervinientes...")
        page2.locator("ul.cat-nav.cat-nav-list li a:has-text('Docs. prof. intervinientes')").click()
        download_docs_prof(page2, base_dir)
    finally:
        if context:
            context.close()
        if browser:
            browser.close()

def login_and_download_documents(usuario, contrasena, siniestro, download_path):
    try:
        with sync_playwright() as playwright:
            run_script(playwright, usuario, contrasena, siniestro, download_path)
        return 200
    except Exception as e:
        print("Error en la automatización:", e)
        return 500

if __name__ == '__main__':
    usuario = "Pf003700"
    contrasena = "Rsa0042*"
    siniestro = "26580769"
    download_path = "./descargas"
    
    result = login_and_download_documents(usuario, contrasena, siniestro, download_path)
    print("Resultado:", result)
