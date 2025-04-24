"""
occident_auto.py  –  v2
Descarga silenciosa de la documentación de un siniestro en Mutua Occident
con control de errores por sección y resumen final.
"""

import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


# --------------------------------------------------------------------------- #
# Utilidades                                                                  #
# --------------------------------------------------------------------------- #

def ensure_subdir(subdir: str) -> str:
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    return subdir


def minimize_and_move_page(page) -> None:
    try:
        cdp = page.context.new_cdp_session(page)
        win_id = cdp.send("Browser.getWindowForTarget")["windowId"]
        cdp.send("Browser.setWindowBounds",
                 {"windowId": win_id,
                  "bounds": {"left": -2000, "top": -2000,
                             "windowState": "normal"}})
        cdp.send("Browser.setWindowBounds",
                 {"windowId": win_id,
                  "bounds": {"windowState": "minimized"}})
    except Exception as e:
        print("Error al ocultar la ventana:", e)


def _download_via_popup(link_locator, subdir, fname_fallback):
    """Helper común: abre el popup, oculta ventana y guarda descarga."""
    file_name = link_locator.inner_text().strip() or fname_fallback
    if not file_name.lower().endswith(".pdf"):
        file_name += ".pdf"

    with link_locator.page.expect_popup() as pop_info:
        link_locator.click()
    new_page = pop_info.value
    time.sleep(0.5)
    minimize_and_move_page(new_page)

    with new_page.expect_download() as d_info:
        new_page.evaluate("""
            () => {
              const a=document.createElement('a');
              a.href = window.location.href;
              a.download='archivo.pdf';
              document.body.appendChild(a); a.click(); a.remove();
            }""")
    download = d_info.value
    save_path = os.path.join(subdir, file_name)
    download.save_as(save_path)
    new_page.close()
    return save_path


# --------------------------------------------------------------------------- #
# Secciones                                                                   #
# --------------------------------------------------------------------------- #

def download_informes(page, base_dir):
    seccion = "Informes"
    subdir = ensure_subdir(os.path.join(base_dir, "informes"))
    selector = "table#ListadoInformes tbody tr"
    page.wait_for_selector(selector, timeout=10_000)
    rows = page.locator(selector)
    n = rows.count()
    if n == 0:
        print(f"[{seccion}] Tabla vacía")
        return "vacía"

    print(f"[{seccion}] Encontradas {n} filas")
    for i in range(n):
        link = rows.nth(i).locator("a").nth(1)
        path = _download_via_popup(link, subdir, f"inf_{i+1}.pdf")
        print(f"[{seccion}] Guardado en: {path}")
    return "ok"


def download_docs_añadidos(page, base_dir):
    seccion = "Docs. añadidos"
    subdir = ensure_subdir(os.path.join(base_dir, "docs_añadidos"))
    try:
        page.wait_for_selector("table#grDocs", state="visible", timeout=10_000)
        page.wait_for_selector("table#grDocs tbody tr",
                               state="visible", timeout=10_000)
    except PWTimeout:
        print(f"[{seccion}] Tabla no encontrada o vacía")
        return "vacía"

    rows = page.locator("table#grDocs tbody tr")
    n = rows.count()
    if n == 0:
        print(f"[{seccion}] Tabla vacía")
        return "vacía"

    print(f"[{seccion}] Encontradas {n} filas")
    for i in range(n):
        a_tags = rows.nth(i).locator("a")
        if a_tags.count() == 0:            # fila sin enlace
            continue
        link = a_tags.first
        path = _download_via_popup(link, subdir, f"doc_añadido_{i+1}.pdf")
        print(f"[{seccion}] Guardado en: {path}")
    return "ok"


def download_docs_recibidos(page, base_dir):
    seccion = "Docs. recibidos"
    subdir = ensure_subdir(os.path.join(base_dir, "docs_recibidos"))
    selector = "table#grDocsCia tbody tr"
    try:
        page.wait_for_selector(selector, timeout=10_000)
    except PWTimeout:
        print(f"[{seccion}] Tabla no encontrada")
        return "vacía"

    rows = page.locator(selector)
    n = rows.count()
    if n == 0:
        print(f"[{seccion}] Tabla vacía")
        return "vacía"

    print(f"[{seccion}] Encontradas {n} filas")
    for i in range(n):
        link = rows.nth(i).locator("a").first
        path = _download_via_popup(link, subdir, f"doc_recibido_{i+1}.pdf")
        print(f"[{seccion}] Guardado en: {path}")
    return "ok"


def download_docs_prof(page, base_dir):
    seccion = "Docs. prof. intervinientes"
    subdir = ensure_subdir(os.path.join(base_dir, "docs_prof_intervinientes"))
    selector = "table#GrDocumentos tbody tr"
    try:
        page.wait_for_selector(selector, timeout=10_000)
    except PWTimeout:
        print(f"[{seccion}] Tabla no encontrada")
        return "vacía"

    rows = page.locator(selector)
    n = rows.count()
    if n == 0:
        print(f"[{seccion}] Tabla vacía")
        return "vacía"

    print(f"[{seccion}] Encontradas {n} filas")
    for i in range(n):
        link = rows.nth(i).locator("a").first
        path = _download_via_popup(link, subdir, f"doc_prof_{i+1}.pdf")
        print(f"[{seccion}] Guardado en: {path}")
    return "ok"


# --------------------------------------------------------------------------- #
# Flujo principal                                                             #
# --------------------------------------------------------------------------- #

def run_script(playwright, usuario, contrasena, siniestro, download_path):
    base_dir = download_path
    os.makedirs(base_dir, exist_ok=True)

    browser = context = None
    secciones_estado = {
        "Informes": "pendiente",
        "Docs. añadidos": "pendiente",
        "Docs. recibidos": "pendiente",
        "Docs. prof. intervinientes": "pendiente",
    }

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
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/103.0.0.0 Safari/537.36"),
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
        )
        context.grant_permissions(["notifications"])
        context.on("page", minimize_and_move_page)

        page = context.new_page()

        # ---------- LOGIN & BÚSQUEDA DEL SINIESTRO (sin cambios) ----------
        page.goto("https://portalprepersa.gco.global/")
        page.goto(("https://ssoaut.gco.global/x-vdesk/hangup.php3?"
                   "return=aHR0cHM6Ly9wb3J0YWxhcGkxLmdjby5nbG9iYWwvbG9naW4v"
                   "P2Q9aHR0cHMlM0ElMkYlMkZwb3J0YWxwcmVwZXJzYS5nY28uZ2xvYmFs"
                   "JTJG"))
        page.goto("https://ssoaut.gco.global/my.policy?apm=3")
        page.get_by_placeholder("Usuario").fill(usuario)
        page.get_by_placeholder("Clave").fill(contrasena)

        with page.expect_popup() as p1:
            page.get_by_role("button", name="Logon").click()
        p1.value.close()
        page.get_by_text("Pulsa aquí para continuar sin").click()

        page.get_by_label("Prepersa.Net").click()
        with page.expect_popup() as p2:
            page.get_by_role("link", name="Búsqueda de encargos").click()

        page2 = p2.value
        page2.get_by_title("En curso").click()
        page2.get_by_role("treeitem", name="Todos").click()
        page2.get_by_title("Nº Siniestro\\Inspección", exact=True).click()
        page2.get_by_role("treeitem", name="Nº Siniestro\\Inspección").click()
        page2.get_by_role("textbox", name="Nº Siniestro\\Inspección: *")\
             .fill(siniestro)
        page2.get_by_role("button", name="Buscar").click()

        ver_btn = page2.locator(
            "td.icon-grid-avanzado a[name='GridResultados']").first
        ver_btn.wait_for(state="visible", timeout=5000)
        ver_btn.click()

        page2.get_by_text("Acciones", exact=True).click()
        page2.get_by_role("link", name="Documentación").click()

        # ---------- DESCARGAS CON CONTROL DE ERRORES ----------------------
        try:
            print("\nDescargando sección Informes…")
            secciones_estado["Informes"] = download_informes(page2, base_dir)
        except Exception as e:
            secciones_estado["Informes"] = f"error: {e}"

        try:
            print("\nDescargando sección Docs. añadidos…")
            page2.locator("ul.cat-nav li a:has-text('Docs. añadidos')").click()
            secciones_estado["Docs. añadidos"] = download_docs_añadidos(
                page2, base_dir)
        except Exception as e:
            secciones_estado["Docs. añadidos"] = f"error: {e}"

        try:
            print("\nDescargando sección Docs. recibidos…")
            page2.locator("ul.cat-nav li a:has-text('Docs. recibidos')").click()
            secciones_estado["Docs. recibidos"] = download_docs_recibidos(
                page2, base_dir)
        except Exception as e:
            secciones_estado["Docs. recibidos"] = f"error: {e}"

        try:
            print("\nDescargando sección Docs. prof. intervinientes…")
            page2.locator(
                "ul.cat-nav li a:has-text('Docs. prof. intervinientes')").click()
            secciones_estado["Docs. prof. intervinientes"] = \
                download_docs_prof(page2, base_dir)
        except Exception as e:
            secciones_estado["Docs. prof. intervinientes"] = f"error: {e}"

        # --------------------- RESUMEN FINAL ------------------------------
        print("\n================  RESUMEN DE LA DESCARGA  ================")
        for sec, estado in secciones_estado.items():
            print(f"  • {sec:<28}: {estado}")
        print("==========================================================\n")

    finally:
        if context:
            context.close()
        if browser:
            browser.close()


def login_and_download_documents(usuario, contrasena, siniestro, download_path):
    try:
        with sync_playwright() as pw:
            run_script(pw, usuario, contrasena, siniestro, download_path)
        return 200
    except Exception as e:
        print("Error global en la automatización:", e)
        return 500


# --------------------------------------------------------------------------- #
# Ejecución directa                                                           #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    usuario = "Pf003700"
    contrasena = "Rsa0042*"
    siniestro = "26580769"
    download_path = r"C:/Users/asier/Documents/PruebasQtpi/3"

    resultado = login_and_download_documents(
        usuario, contrasena, siniestro, download_path)
    print("Resultado:", resultado)
