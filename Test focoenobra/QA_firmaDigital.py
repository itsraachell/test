import base64
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import HtmlTestRunner

class TestCargaExitosa(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")

        # Iniciar el navegador
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

        self.driver.get("https://ambienteqa.focoenobra.cl:1010/Seguridad/Login.aspx")

        # Ingresar credenciales y hacer clic en el botón de enviar
        self.driver.find_element(By.ID, 'fname').send_keys('rrosales')
        codif_contraseña = "cm9zYWxlczIwMjMk"
        contraseña = base64.b64decode(codif_contraseña).decode('utf-8')
        self.driver.find_element(By.ID, 'fpass').send_keys(contraseña)
        self.driver.find_element(By.ID, 'btningresar_CD').click()

    def test_1trabajadoresEnrolados(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/ul/li[3]/a"))).click()

        # Esperar y hacer clic en menú de Firma Digital
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Firma Digital')]"))).click()

        # Esperar y hacer clic en "Listado de Empleadores"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Trabajadores Enrolados')]"))).click()

        # Esperar a que se abra la nueva pestaña y cambiar el foco a ella
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        lista_pestañas = self.driver.window_handles
        self.driver.switch_to.window(lista_pestañas[-1])
        time.sleep(5)

        try:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/iframe"))
            time.sleep(10)

        except Exception:
            self.fail("Error al cargar: No se encontró información de los trabajadores enrolados.")

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/h2').text
            enrolados = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div[1]/div[1]').text
            enrolados_numero = enrolados.split(": ")[1]
            sinenrolar = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div[1]/div[2]').text
            sinenrolar_numero = sinenrolar.split(": ")[1]

            nombre = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]/span'))).text.strip()
            # Obtener el empleador
            empleador = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[3]').text.strip()
            # Obtener el rut
            rut = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener el email
            email = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]').text.strip()

        except Exception:
            self.fail("Error al procesar los registros: No se encontró información de los trabajadores enrolados.")

        if enrolados.strip() == "0":
            self.fail("No se muestran registros de trabajadores enrolados.")

        print("Informacion encontrada:<br>")
        print("Titulo: ", titulo, "<br>")
        print("Trabajadores enrolados: ",enrolados_numero, "<br>")
        print("Trabajadores sin enrolar: ",sinenrolar_numero, "<br>")
        print("--------------------<br>")
                                    
        # Imprimir los detalles
        print("Ultimo registro:<br>")
        print("Nombre - Cargo:", nombre, "<br>")
        print("Empleador:", empleador, "<br>")
        print("RUT:", rut, "<br>")
        print("Email - Telefono:", email, "<br>")

        self.driver.close()
        self.driver.switch_to.window(lista_pestañas[0])

    def test_2Fiscalizadores(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/ul/li[3]/a"))).click()

        # Esperar y hacer clic en menú de Firma Digital
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Firma Digital')]"))).click()

        # Esperar y hacer clic en "Fiscalizadores"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Fiscalizadores')]"))).click()

        # Esperar a que se abra la nueva pestaña y cambiar el foco a ella
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        lista_pestañas = self.driver.window_handles
        self.driver.switch_to.window(lista_pestañas[-1])
        time.sleep(5)

        try:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/iframe"))
            time.sleep(10)
        except Exception:
            self.fail("No se encontro información de los fiscalizadores.")

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/h2').text
            conacceso = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[1]/div[1]').text
            conacceso_numero = conacceso.split(": ")[1]
            sinacceso = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[1]/div[2]').text
            sinacceso_numero = sinacceso.split(": ")[1]

            nombre = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[3]'))).text.strip()
            # Obtener el empleador
            rut = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[2]').text.strip()
            # Obtener el rut
            estado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]').text.strip()
            # Obtener el email
            email = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener el teléfono
            trabajadores = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[7]/div').text.strip()

        except Exception:
            self.fail("Error al procesar los registros: No se encontró información de los fiscalizadores")

        if conacceso.strip() == "0":
            self.fail("No se muestran registros de fiscalizadores.")

        print("Informacion encontrada:<br>")
        print("Titulo: ", titulo, "<br>")
        print("Con acceso habilitado: ",conacceso_numero, "<br>")
        print("Sin acceso habilitado: ",sinacceso_numero, "<br>")
        print("--------------------<br>")

        # Imprimir los detalles
        print("Ultimo registro:<br>")
        print("Nombre: ",nombre, "<br>")
        print("RUT: ",rut, "<br>")
        print("Estado de cuenta: ",estado, "<br>")
        print("Email: ",email, "<br>")
        print("Acceso trabajadores: ",trabajadores, "<br>")

        self.driver.close()
        self.driver.switch_to.window(lista_pestañas[0])

    def test_3listadoNominas(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/ul/li[3]/a"))).click()

        # Esperar y hacer clic en menú de Firma Digital
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Firma Digital')]"))).click()

        # Esperar y hacer clic en "Fiscalizadores"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Listado de Nóminas')]"))).click()

        # Esperar a que se abra la nueva pestaña y cambiar el foco a ella
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        lista_pestañas = self.driver.window_handles
        self.driver.switch_to.window(lista_pestañas[-1])
        time.sleep(5)

        try:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/iframe"))
            time.sleep(10)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='root']/div/div/div[2]/div/div/div[2]/div/span[2]"))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[5]'))).click()
            time.sleep(5)

        except Exception:
            self.fail("Error al cargar: No se encontro información de nominas de firmantes.")

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/h2').text
            nominas = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div').text
            nominas_numero = nominas.split(": ")[1]

            nombre = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[3]/div/table/tbody/tr[1]/td[3]'))).text.strip()
            # Obtener quien lo generó
            generado = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener cuando se generó
            fecha = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div/table/tbody/tr[1]/td[5]/div').text.strip()
            # Obtener la cantidad de firmantes
            firmantes = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div/table/tbody/tr[1]/td[6]/div/span').text.strip()
            
        except Exception:
            self.fail("Error al procesar los registros: No se encuentran registros de nominas de firmantes")

        if nominas.strip() == "0":
            self.fail("No se muestran registros de nominas de firmantes.")

        print("Informacion encontrada:<br>")
        print("Titulo: ", titulo, "<br>")
        print("Total de nominas: ",nominas_numero, "<br>")
        print("--------------------<br>")
      
        # Imprimir los detalles
        print("Ultimo registro:<br>")
        print("Nombre de nomina: ",nombre, "<br>")
        print("Generado por: ",generado, "<br>")
        print("Generado el: ",fecha, "<br>")
        print("Cantidad de firmantes: ",firmantes, "<br>")     

        self.driver.close()
        self.driver.switch_to.window(lista_pestañas[0])

    def test_4listadoEmpleadores(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/ul/li[3]/a"))).click()

        # Esperar y hacer clic en menú de Firma Digital
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Firma Digital')]"))).click()

        # Esperar y hacer clic en "Listado de Empleadores"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main-menu']/ul/div[2]/div/li[4]/ul/li[6]/a"))).click()

        # Esperar a que se abra la nueva pestaña y cambiar el foco a ella
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        lista_pestañas = self.driver.window_handles
        self.driver.switch_to.window(lista_pestañas[-1])
        time.sleep(5)

        try:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/iframe"))
            time.sleep(10)

        except Exception:
            self.fail("Error al cargar: No se encontró información de los empleadores.")

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/h2').text
            total = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div').text
            total_numero = total.split(": ")[1]

            id = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[3]'))).text.strip()
            # Obtener la razon social
            razon = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener el rut
            rut = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]').text.strip()
            # Obtener el nombre de fantasia
            nombref = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]').text.strip()
            # Obtener cantidad de trabajadores
            trabajadores = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[11]/div').text.strip()
            
        except Exception:
                self.fail("Error al procesar los registros: No se encuentran registros de empleadores")

        if total.strip() == "0":
            self.fail("No se muestran registros de empleadores.")

        print("Informacion encontrada:<br>")
        print("Titulo: ", titulo, "<br>")
        print("Total: ",total_numero, "<br>")
        print("--------------------<br>")

        # Imprimir los detalles
        print("Ultimo registro:<br>")
        print("ID:", id, "<br>")
        print("Razon social:", razon, "<br>")
        print("RUT:", rut, "<br>")
        print("Nombre fantasia:", nombref, "<br>")
        print("Trabajadores:", trabajadores, "<br>")

        self.driver.close()
        self.driver.switch_to.window(lista_pestañas[0])

    def test_5listadoDocumentos(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/ul/li[3]/a"))).click()

        # Esperar y hacer clic en menú de Firma Digital
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Firma Digital')]"))).click()

        # Esperar y hacer clic en "Listado de Empleadores"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Listado de Documentos Firmados')]"))).click()

        # Esperar a que se abra la nueva pestaña y cambiar el foco a ella
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        lista_pestañas = self.driver.window_handles
        self.driver.switch_to.window(lista_pestañas[-1])
        time.sleep(5)

        try:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[5]/iframe'))
            time.sleep(10)
            
            #Seleccionar proyecto
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[2]/div/span[2]'))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[5]/div'))).click()
            time.sleep(5)

            #Seleccionar periodo
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[3]/div[2]/div[1]/span[2]'))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[5]'))).click()
            time.sleep(5)
        
        except Exception:
            self.fail("Error al cargar: No se encontró información del listado de documentos.")

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/h2').text
            cargados = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div[1]/div[1]').text
            cargados_numero = cargados.split(": ")[1]
            pendientes = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div[1]/div[2]').text
            pendientes_numero = pendientes.split(": ")[1]

            numero = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[3]'))).text.strip()
            # Obtener el tipo de documento
            tipodoc = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener quien lo genero
            generado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]').text.strip()
            # Obtener cuando se genero
            fecha = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]/div').text.strip()
            # Obtener los pendientes
            pendientes = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[7]/div').text.strip()
            # Obtener los firmados
            firmados = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[8]/div').text.strip()
        
        except Exception:
            self.fail("Error al procesar los registros: No se encuentran registros de listado de documentos")

        if cargados.strip() == "0":
            self.fail("No se muestran registros de documentos.")

        print("Informacion encontrada:<br>")
        print("Titulo: ", titulo, "<br>")
        print("Documentos cargados: ",cargados_numero, "<br>")
        print("Pendientes de firma: ",pendientes_numero, "<br>")
        print("--------------------<br>")

        # Imprimir los detalles
        print("Ultimo registro:<br>")
        print("Numero:", numero, "<br>")
        print("Tipo de documento:", tipodoc, "<br>")
        print("Generado por:", generado, "<br>")
        print("Generado el:", fecha, "<br>")
        print("Pendientes:", pendientes, "<br>")
        print("Firmados:", firmados, "<br>")
        print("--------------------<br>")

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#table-container > div > table > tbody > tr:nth-child(1) > td:nth-child(9) > div > svg.mr-24.cursor-pointer'))).click()
            time.sleep(5)

            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/h2').text
            print("Titulo del documento visualizado: ", titulo, "<br>")

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#rc-tabs-0-panel-1 > div > div.document-wrapper.w-100.border-box.flex.items-center.justify-center > div > div > svg'))).click()
            time.sleep(10)
            print("El documento se esta mostrando correctamente<br>")
            print("--------------------<br>")

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#rc-tabs-0-panel-1 > div > div.document-wrapper.w-100.border-box.flex.items-center.justify-center > div > div > div.viewer-full-screen > button'))).click()

        except Exception:
            self.fail("Error al visualizar el PDF (documento)")

        try:
            # Obtener todos los elementos de la tabla de firmantes
            time.sleep(3)
            firmantes = self.driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/table/tbody/tr')

            if not firmantes:
                raise Exception("No se encontraron firmantes en la tabla")
            
            print("Firmante(s):<br>")

            for firmante_element in firmantes:
                # Obtener información del firmante de esta fila
                rut = firmante_element.find_element(By.XPATH, './td[2]/div/div[2]/span[1]').text.strip()
                firmante = firmante_element.find_element(By.XPATH, './td[2]/div/div[2]/span[2]').text.strip()
                estado = firmante_element.find_element(By.XPATH, './td[3]/div/span').text.strip()
                # Imprimir los detalles del firmante
                print("RUT:", rut,"<br>")
                print("Nombre:", firmante,"<br>")
                print("Estado:", estado,"<br>")
                print("--------------------<br>")

        except Exception as e:
            self.fail(f"No se ha podido obtener informacion del documento: {str(e)}")

        self.driver.close()
        self.driver.switch_to.window(lista_pestañas[0])

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
