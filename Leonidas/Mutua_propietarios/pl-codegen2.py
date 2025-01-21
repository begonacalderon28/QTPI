import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://innova.mutuadepropietarios.es/web/login.jsp")
    page.get_by_label("Usuario:").click()
    page.get_by_label("Usuario:").fill("AB_SCGMABO")
    page.get_by_label("Usuario:").press("Tab")
    page.get_by_label("Clave:").fill("Eneroinvierno2025.*")
    page.get_by_role("button", name="Entrar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.get_by_role("link", name=" Encargos").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Varios").check()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").fill("2024")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").fill("4041692")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("button", name="Buscar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="Documentos").click()
    with page.expect_download() as download_info:
        with page.expect_popup() as page1_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="1. Revitec PRES1498 FACHADA SATE Y VARIOS URUGUAY 13V4.pdf Revitec PRES1498 FACHADA SATE Y VARIOS URUGUAY 13V4.pdf 11/07/2024 ", exact=True).get_by_role("link").click()
        page1 = page1_info.value
    download = download_info.value
    with page.expect_download() as download1_info:
        with page.expect_popup() as page2_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="2. SKMC250i24070911140.pdf SKMC250i24070911140.pdf 11/07/2024 ", exact=True).get_by_role("link").click()
        page2 = page2_info.value
    download1 = download1_info.value
    with page.expect_download() as download2_info:
        with page.expect_popup() as page3_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="3. ContenidoMail.doc ContenidoMail.doc 11/07/2024 ", exact=True).get_by_role("link").click()
        page3 = page3_info.value
    download2 = download2_info.value
    with page.expect_download() as download3_info:
        with page.expect_popup() as page4_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="4. 723e4c7dc6c564bb3e1d2ad95abcd49d_valorationReport.pdf 723e4c7dc6c564bb3e1d2ad95abcd49d_valorationReport.pdf 10/06/2024 ", exact=True).get_by_role("link").click()
        page4 = page4_info.value
    download3 = download3_info.value
    with page.expect_download() as download4_info:
        with page.expect_popup() as page5_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="5. SKMC250i24051517440.pdf SKMC250i24051517440.pdf 17/05/2024 ", exact=True).get_by_role("link").click()
        page5 = page5_info.value
    download4 = download4_info.value
    with page.expect_download() as download5_info:
        with page.expect_popup() as page6_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="7. Parte_Encargo_Manual_20245170382.pdf Parte_Encargo_Manual_20245170382.pdf 17/05/2024 ", exact=True).get_by_role("link").click()
        page6 = page6_info.value
    download5 = download5_info.value
    with page.expect_download() as download6_info:
        with page.expect_popup() as page7_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="8. Texto libre Texto libre 17/05/2024 ", exact=True).get_by_role("link").click()
        page7 = page7_info.value
    download6 = download6_info.value
    with page.expect_download() as download7_info:
        with page.expect_popup() as page8_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="9. Texto libre Texto libre 17/05/2024 ", exact=True).get_by_role("link").click()
        page8 = page8_info.value
    download7 = download7_info.value
    with page.expect_download() as download8_info:
        with page.expect_popup() as page9_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="2. Docs. judicial DIOR 17-06-24(31).pdf 25/06/2024 10:45:34 ", exact=True).get_by_role("link").click()
        page9 = page9_info.value
    download8 = download8_info.value
    with page.expect_download() as download9_info:
        with page.expect_popup() as page10_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="3. Docs. judicial fichero.PDF 15/11/2024 12:05:40 ", exact=True).get_by_role("link").click()
        page10 = page10_info.value
    download9 = download9_info.value
    with page.expect_download() as download10_info:
        with page.expect_popup() as page11_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="5. Docs. judicial Binder1.pdf 18/11/2024 16:32:30 ", exact=True).get_by_role("link").click()
        page11 = page11_info.value
    download10 = download10_info.value
    with page.expect_download() as download11_info:
        with page.expect_popup() as page12_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="8. Docs. judicial 2025-8 Factura.pdf 10/01/2025 11:32:57 ", exact=True).get_by_role("link").click()
        page12 = page12_info.value
    download11 = download11_info.value
    with page.expect_download() as download12_info:
        with page.expect_popup() as page13_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="9. Docs. judicial 9473.pdf 13/01/2025 14:08:55 ", exact=True).get_by_role("link").click()
        page13 = page13_info.value
    download12 = download12_info.value
    with page.expect_download() as download13_info:
        with page.expect_popup() as page14_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("cell", name="Documentos asociados de póliza   Nombre del archivo Fecha Descargar 1.").get_by_role("link").click()
        page14 = page14_info.value
    download13 = download13_info.value
    with page.expect_download() as download14_info:
        with page.expect_popup() as page15_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("cell", name="Documento de factura Tipo").get_by_role("link").click()
        page15 = page15_info.value
    download14 = download14_info.value
    page15.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
