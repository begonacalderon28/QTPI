import re
from playwright.sync_api import Playwright, sync_playwright, expect


















def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.locator("body").click()
    page.goto("https://ssoaut.gco.global/my.policy?apm=3")
    page.locator("div:nth-child(3)").first.click()
    page.get_by_placeholder("Usuario").click(modifiers=["ControlOrMeta"])
    page.get_by_placeholder("Usuario").fill("Pf003700")
    page.get_by_placeholder("Usuario").click(modifiers=["ControlOrMeta"])
    page.locator("div:nth-child(3)").first.click()
    page.get_by_placeholder("Clave").click()
    page.get_by_placeholder("Clave").fill("Rsa0041*")
    with page.expect_popup() as page1_info:
        page.get_by_placeholder("Iniciar sesión").click()
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
    page2.get_by_role("textbox", name="Nº Siniestro\\Inspección: *").fill("26580769")
    page2.get_by_role("button", name="Buscar").click()
    page2.locator("#trGridResultados0").get_by_role("gridcell", name="").locator("a").click()
    page2.get_by_text("Acciones", exact=True).click()
    page2.get_by_role("link", name="Documentación").click()
    with page2.expect_popup() as page3_info:
        page2.get_by_text("Resumen del encargo").click()
    page3 = page3_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
