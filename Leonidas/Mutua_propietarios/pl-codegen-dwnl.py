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
    page.get_by_label("Clave:").press("Enter")
    page.get_by_role("button", name="Entrar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.get_by_role("link", name=" Encargos").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_title("Haz clic para seleccionar").nth(3).click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Año:").fill("2023")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_label("Nº siniestro:").fill("4058430")
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("button", name="Buscar").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="").click()
    page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("link", name="Documentos").click()
    with page.expect_download() as download_info:
        with page.expect_popup() as page1_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="1. 20241112114827882.pdf 20241112114827882.pdf 13/11/2024 ", exact=True).get_by_role("link").click()
        page1 = page1_info.value
    download = download_info.value
    with page.expect_download() as download1_info:
        with page.expect_popup() as page2_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="2. Texto libre Texto libre 23/10/2024 ", exact=True).get_by_role("link").click()
        page2 = page2_info.value
    download1 = download1_info.value
    with page.expect_download() as download2_info:
        with page.expect_popup() as page3_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="3. D2.202403180934.0.CARTDENEMABEL RUIZ VAREA.pdf D2.202403180934.0.CARTDENEMABEL RUIZ VAREA.pdf 25/09/2024 ", exact=True).get_by_role("link").click()
        page3 = page3_info.value
    download2 = download2_info.value
    with page.expect_download() as download3_info:
        with page.expect_popup() as page4_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="4. informe Edif.Alboraya.Pza.Mayor3.pdf informe Edif.Alboraya.Pza.Mayor3.pdf 17/07/2024 ", exact=True).get_by_role("link").click()
        page4 = page4_info.value
    download3 = download3_info.value
    with page.expect_download() as download4_info:
        with page.expect_popup() as page5_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="5. D2.202403180934.1.CARTDENE_C P PÇ MAYOR, 2-3 .pdf D2.202403180934.1.CARTDENE_C P PÇ MAYOR, 2-3 .pdf 18/03/2024 ", exact=True).get_by_role("link").click()
        page5 = page5_info.value
    download4 = download4_info.value
    with page.expect_download() as download5_info:
        with page.expect_popup() as page6_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="6. InformeDefinitivo1.pdf InformeDefinitivo1.pdf 19/02/2024 ", exact=True).get_by_role("link").click()
        page6 = page6_info.value
    download5 = download5_info.value
    with page.expect_download() as download6_info:
        with page.expect_popup() as page7_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="1. Docs. judicial contestación 10202.pdf 21/11/2024 08:44:01 ", exact=True).get_by_role("link").click()
        page7 = page7_info.value
    download6 = download6_info.value
    with page.expect_download() as download7_info:
        with page.expect_popup() as page8_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="1. M8ktrYnNx_5272-500-500526974-24-Tomador - CP.pdf 13/11/2024 ", exact=True).get_by_role("link").click()
        page8 = page8_info.value
    download7 = download7_info.value
    with page.expect_download() as download8_info:
        with page.expect_popup() as page9_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="2. 8vmudLQz0_5272-500-500526974-25-Tomador - CP.pdf 13/11/2024 ", exact=True).get_by_role("link").click()
        page9 = page9_info.value
    download8 = download8_info.value
    with page.expect_download() as download9_info:
        with page.expect_popup() as page10_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="3. N3MWkKQlM_5272-500-500526974-20-Tomador - CP.pdf 13/11/2024 ", exact=True).get_by_role("link").click()
        page10 = page10_info.value
    download9 = download9_info.value
    with page.expect_download() as download10_info:
        with page.expect_popup() as page11_info:
            page.locator("iframe[name=\"cuerpo\"]").content_frame.locator("#iFrameEncargos").content_frame.get_by_role("row", name="4. FPKaOpFbb_5272-500-500526974-11-Tomador - CP.pdf 13/11/2024 ", exact=True).get_by_role("link").click()
        page11 = page11_info.value
    download10 = download10_info.value
    page11.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)



