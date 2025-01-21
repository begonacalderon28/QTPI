import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False )
    context = browser.new_context(
        accept_downloads=True, 
        # Especifica la carpeta donde quieres guardar las descargas
        
    )
    page = context.new_page()
    page.goto("https://innova.mutuadepropietarios.es/web/login.jsp")
    page.get_by_label("Usuario:").click()
    page.get_by_label("Usuario:").fill("AB_SCGMABO")
    page.get_by_label("Clave:").click()
    page.get_by_label("Clave:").fill("Eneroinvierno2025.*")
    page.get_by_role("button", name="Entrar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.get_by_role("link", name=" Encargos").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Varios").check()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").fill("2023")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").fill("4058430")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("button", name="Buscar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="Documentos").click()
    encargos_frame = page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame
    
    # ---------------------
    # 5) Esperar un poco a que aparezcan los links de descarga
    time.sleep(3)
    
    # 6) Localizar los enlaces con title="Descargar"
    links = encargos_frame.locator('a[title="Descargar"]')
    count = links.count()
    print(f"Encontrados {count} enlace(s) con title='Descargar'.")
    
    # 7) Clic secuencial en cada enlace, capturando la descarga en un bucle
    for i in range(count):
        with page.expect_download() as download_info:
            links.nth(i).click()  # Clic en el enlace i
        download = download_info.value
        
        # Nombre sugerido por el servidor/navegador
        suggested_name = download.suggested_filename
        if not suggested_name:
            suggested_name = f"archivo_{i+1}.pdf"
        elif not suggested_name.lower().endswith(".pdf"):
            suggested_name += ".pdf"
        
        # Construir la ruta final en tu carpeta de descargas
        final_path = os.path.join(r"C:\QTPI\Leonidas\Mutua_propietarios\descargas-test", suggested_name)
        
        # Guardar el archivo
        download.save_as(final_path)
        print(f"Descargado: {final_path}")

    time.sleep(15)
    # Cerrar navegador
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
