#allianz.py

from playwright.sync_api import sync_playwright
import time
import os
import urllib.parse
import math
import shutil
from pathlib import Path
import re


from typing import Union           # ← importa Union

def ensure_dir(p: Union[str, Path]) -> Path:
    """Crea la carpeta si no existe y devuelve Path."""
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


#CHANGE RETURN VIENDO SI EL LOGIN HA SIDO EXITOSO 
#hay veces que tarda mucho el login poner un measurement
#probar con distintos cosas el elif de autodescargable pero hay que dar a un boton


def allianz_document_download(usuario,contraseña, siniestro, downloads_path):
    with sync_playwright() as p:
        # Crear navegador y contexto
        browser = p.chromium.launch(headless=True, downloads_path=downloads_path)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            java_script_enabled=True,
            accept_downloads=True,
            )
        page = context.new_page()
        

        # Deshabilitar propiedades que delatan automatización
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        
        # Navegar a la página de inicio
        page.goto("https://www.e-pacallianz.com/ngx-epac-professional/public/home")
        page.wait_for_load_state('networkidle')

        # Iniciar sesión
        page.get_by_label("Usuario").fill(usuario)
        page.get_by_role("textbox", name="Contraseña").fill(contraseña)
        page.get_by_role("button", name="Iniciar sesión").click()
        page.wait_for_load_state('networkidle')
        time.sleep(3)


        # Verificar si el login fue exitoso
        if page.is_visible('role=menuitem[name="Aplic. Allianz"]'):
            print("bien")  # Login exitoso
            #pass
        else:
            time.sleep(5)
            if page.is_visible('role=menuitem[name="Aplic. Allianz"]'):
                print("bien")  # Login exitoso
                #pass
            else:
                print("Error en el login.")
                browser.close()
                return 411  # Error en el login

        # Navegar e introducir el siniestro
        page.get_by_role("menuitem", name="Aplic. Allianz").click()
        page.get_by_role("menuitem", name="Plataforma Abogados Allianz").click()
        page.wait_for_load_state('networkidle')

        # Metemos encargo y accedemos a la ficha de gestion
        page.locator("iframe[name=\"appArea\"]").content_frame.get_by_label("Siniestro / Encargo").fill(siniestro)
        page.locator("iframe[name=\"appArea\"]").content_frame.get_by_text("Enviar").click()
        page.locator("iframe[name=\"appArea\"]").content_frame.locator("#ordersList_0_0").click()
        with page.expect_popup() as page1_info:
            page.locator("iframe[name=\"appArea\"]").content_frame.locator("#FG div").filter(has_text="Ficha de Gestión").click()

        page1 = page1_info.value

        def handle_download(download):
            suggested_filename = download.suggested_filename
            name, ext = os.path.splitext(suggested_filename)
            suggested_filename = f"{name}_{file_total}{ext}"
            if suggested_filename:
                download_path = os.path.join(downloads_path, suggested_filename)
                download.save_as(download_path)
                print(f"Downloaded and saved as: {download_path}")
            else:
                pass

                
                
        page1.on("download", handle_download)

        # ── NUEVO: garantiza que existan las carpetas internas ───────────
        downloads_cwd = Path.cwd()                 # carpeta desde donde corre el EXE
        ensure_dir(downloads_cwd / "downloads")
        ensure_dir(downloads_cwd / "download_2")
        # ─────────────────────────────────────────────────────────────────


        src_path = str(downloads_cwd) + '/downloads'
        

        folder = src_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        # Logica para la descarga de archivos
        file_number = -1  
        block_number = 0
        file_total = -1

        while True:
            file_number = file_number + 1
            file_total = file_total + 1

            try:
                page1.get_by_role("button", name="Ver Mas").click()
            except:
                pass

            id = 'filaFile_' + str(block_number) +'_'+ str(file_number)

            element_selector = f"#{id}"
            element = page1.locator(element_selector)

            if element.is_visible() == False and file_number == 0:
                browser.close()
                return 200

            elif element.is_visible() == False:
                block_number = block_number + 1
                file_number = 0
                id = 'filaFile_' + str(block_number) +'_'+ str(file_number) 
                element = page.locator(element_selector)
                file_number = -1
            

            else:
                INVALID_id_name = element.locator('strong').nth(1).text_content()
                id_name = str(INVALID_id_name).replace(':', '')
                id_name = str(id_name).replace('<',"" )
                id_name = str(id_name).replace('/',"" )
                id_name = str(id_name).replace('>', '')
                id_name = str(id_name).replace('"', '')
                id_name = str(id_name).replace("'\'",'')
                id_name = str(id_name).replace('|', '')
                id_name = str(id_name).replace('?', '')
                id_name = str(id_name).replace('*', '')
                id_name = id_name + '_' + str(file_total)

                element.click()
                try:
                    page1.get_by_role("button", name="Acceso detalle extendido").wait_for(timeout=100000)
                    page1.get_by_role("button", name="Acceso detalle extendido").click()
                except:
                    try:
                        page1.get_by_role("button", name="Acceso detalle extendido").wait_for(timeout=100000)
                        page1.get_by_role("button", name="Acceso detalle extendido").click()
                    except:
                        pass


                page1.wait_for_load_state('networkidle')
                no_descargable_key = page1.locator("#txtLabelDescrip_label")
                time.sleep(2)
                if no_descargable_key.is_visible(): 
                    frame = page1.locator("#textAreaNota")
                    text_content = frame.input_value()
                    with open("downloads/" + str(id_name) + ".txt", "w") as f:
                        f.write(text_content) 
                else:
                    pass

                volver_btn = page1.get_by_text("Volver", exact=True)
                volver_btn.wait_for(timeout=300000)
                volver_btn.click()

                time.sleep(3)

                cwd = os.getcwd()
                src_path_downloads = str(cwd) + '/downloads'
                for file in os.listdir(src_path_downloads):
                    if file.endswith(".crdownload"):
                        print('File still downloading')
                        time.sleep(10)
                        log = open('log.txt', 'w')
                        log.write('File still downloading..')
                
                src_path_download_2 = str(cwd) + '/download_2'
                for file in os.listdir(src_path_download_2):
                    if file.endswith(".crdownload"):
                        print('File still downloading')
                        time.sleep(10)
                        log = open('log.txt', 'w')
                        log.write('File still downloading..')
                
                source_dir = 'downloads'
                target_dir = 'download_2'

                file_names = os.listdir(source_dir)
                print(file_names)
                for file_name in file_names:
                    shutil.move(os.path.join(source_dir, file_name), target_dir)
                
                #Rename file in the new directory
                
                new_file_name_pdf = 'download_2/'+ str(id_name) + '.PDF'
                new_file_name_eml = 'download_2/' + str(id_name) + '.EML'
                new_file_name_html = 'download_2/'+ str(id_name) + '.HTML'
                new_file_name_msg = 'download_2/' + str(id_name) + '.MSG'
                new_file_name_docx = 'download_2/' + str(id_name) + '.DOCX'
                
                try:
                    os.rename('download_2/fichero.PDF', new_file_name_pdf)
                    print('Renaming PDF file...')
                except:
                    try:
                        os.rename('download_2/fichero.EML', new_file_name_eml)
                        print('Renaming EML file...')
                    except:
                        try:
                            os.rename('download_2/fichero.HTML', new_file_name_html)
                            print('Renaming HTML file...')
                        except:
                            try:
                                os.rename('download_2/fichero.MSG', new_file_name_msg)
                                print('Renaming MSG file...')
                            except:
                                try:
                                    os.rename('download_2/fichero.DOCX', new_file_name_docx)
                                    print('Renaming DOCX file...')
                                except:
                                    pass

                print('Process finished')

                #get current directory and select target directory
                cwd = os.getcwd()

                src_path = str(cwd) + '/download_2'
                trg_path = str(downloads_path)
                file_names = os.listdir(src_path)


                for src_file in Path(src_path).glob('*.*'):
                    shutil.copy(src_file, trg_path)

                #Delete content of download_2
                folder = src_path
                for filename in os.listdir(downloads_path):
                    if re.match(r"^[0-9a-f\-]{36}$", filename):
                        file_path = os.path.join(downloads_path, filename)
                        try:
                            os.remove(file_path)
                            print(f"Deleted leftover file: {filename}")
                        except Exception as e:
                            print(f"Failed to delete {filename}. Reason: {e}")
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

                print("Done")

        

if __name__ == "__main__":
    user = "P0011324"
    pswd = "bilma-0014"
    sns = "876218555"
    path_des = "des_prueba"
    allianz_document_download(user,pswd,sns,path_des)


