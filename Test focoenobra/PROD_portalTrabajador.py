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

        self.driver.get("https://embeddedfocoqa.focoenobra.cl/employees-portal/login")

        # Ingresar credenciales y hacer clic en el botón de enviar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'basic_username'))).send_keys('269964499')
        #codif_contraseña = "cmFjaGVsbDI0="
        #contraseña = base64.b64decode(codif_contraseña).decode('utf-8')
        self.driver.find_element(By.ID, 'basic_password').send_keys('rachell24')
        self.driver.find_element(By.XPATH, '//*[@id="basic"]/div/div[3]/button').click()
        time.sleep(5)

    def test_1documentosPendientes(self):
        try:
            cuenta = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[1]/h2').text
            cuenta_nombre = cuenta.split(", ")[1]
            pendientes = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/span').text
            firmados = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[2]/div/span').text
            anulados = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[3]/div/span').text

        except NoSuchElementException:
            self.fail("No se encontro información del portal de trabajador")

        print("Informacion encontrada:<br>")
        print("Cuenta: ", cuenta_nombre, "<br>")
        print("Documentos pendientes: ",pendientes, "<br>")
        print("Documentos firmados: ",firmados, "<br>")
        print("Documentos anulados: ",anulados, "<br>")
        print("---------------------------<br>")

        if pendientes.strip() == "0":
            print("No hay documentos pendientes por firmar.")
            return

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/button'))).click()
        time.sleep(5)

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div/h2').text
            print("Titulo: ", titulo, "<br>")
            print("---------------------------<br>")

            # Obtener el numero del documento
            numero = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]'))).text.strip()
            # Obtener el tipo de documento
            tipodoc = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]/div').text.strip()
            # Obtener quien lo genero
            generado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]').text.strip()
            # Obtener cuando se genero
            fecha = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[7]/div').text.strip()
            # Obtener el estado
            estado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[8]/div/span').text.strip()

        except NoSuchElementException:
            self.fail("No se ha podido encontrar documentos para firmar")
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido encontrar documentos para firmar")

        # Imprimir los detalles
        print("Ultimo documento:<br>")
        print("Numero: ",numero, "<br>")
        print("Tipo de documento: ",tipodoc, "<br>")
        print("Generado por: ",generado, "<br>")
        print("Generado el: ",fecha, "<br>")
        print("Estado: ",estado, "<br>")
        print("--------------------<br>")

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#table-container > div > table > tbody > tr:nth-child(1) > td:nth-child(9) > div > svg.cursor-pointer'))).click()
            time.sleep(5)
            documento_titulo = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/h2'))).text.strip()
            print("Documento visualizado: ",documento_titulo, "<br>")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.full-screen-icon'))).click()
            time.sleep(10)
            print("El documento se esta mostrando correctamente<br>")
            print("---------------------------<br>")

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.back-button > span'))).click()
                    
        except NoSuchElementException:
                self.fail("Error al visualizar el documento")
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido encontrar visualizar el documento")

        try:
            firmar = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/button[2]')
            if firmar.is_enabled():
                firmar.click()
                time.sleep(3)

        except NoSuchElementException:
            self.fail("Error al intentar firmar el documento")
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido intentar firmar el documento")

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pin-field-content:nth-child(1)'))).send_keys("1")
        self.driver.find_element(By.CSS_SELECTOR, '.pin-field-content:nth-child(2)').send_keys("1")
        self.driver.find_element(By.CSS_SELECTOR, '.pin-field-content:nth-child(3)').send_keys("0")
        self.driver.find_element(By.CSS_SELECTOR, '.pin-field-content:nth-child(4)').send_keys("1")
        time.sleep(3)
                
        firmado = WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".foco-h3"))).text
        if firmado == "¡Firmaste con éxito!":
            print("Mensaje obtenido: ", firmado, "<br>")
        else:
            self.fail("No se ha podido firmar el documento correctamente.")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".foco-btn-primary-big"))).click()

        self.driver.close()

    def test_2documentosFirmados(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[2]/div/button'))).click()
        time.sleep(5)

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div/h2').text
            print("Titulo: ", titulo, "<br>")
            print("---------------------------<br>")

        except NoSuchElementException:
            self.fail("No se encontro información del portal de trabajador (Documentos firmados)")

        try:
            # Obtener el numero del documento
            numero = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener el tipo de documento
            tipodoc = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]').text.strip()
            # Obtener quien lo genero
            generado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]').text.strip()
            # Obtener cuando se genero
            fecha = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[7]/div').text.strip()
            # Obtener el estado
            estado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[8]/div/span[1]').text.strip()
            # Obtener la fecha de la firma
            firma = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[8]/div/span[2]').text.strip()
        except NoSuchElementException:
            self.fail("No se ha podido encontrar documentos firmados")
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido encontrar documentos firmados")

        # Imprimir los detalles
        time.sleep(10)
        print("Ultimo documento:<br>")
        print("Numero: ",numero, "<br>")
        print("Tipo de documento: ",tipodoc, "<br>")
        print("Generado por: ",generado, "<br>")
        print("Generado el: ",fecha, "<br>")
        print("Estado: ",estado, "<br>")
        print("Fecha y hora de la firma: ",firma, "<br>")
        print("--------------------<br>")

        try:  
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#table-container > div > table > tbody > tr:nth-child(1) > td:nth-child(9) > div > svg.cursor-pointer.not-signed-pen'))).click()

            documento_titulo = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/h2'))).text.strip()
            print("Documento visualizado: ",documento_titulo, "<br>")
            time.sleep(5)

            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.full-screen-icon'))).click()
            # time.sleep(5)
            # print("El documento se esta mostrando correctamente<br>")

            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.back-button > span'))).click()
            
        except NoSuchElementException:
            self.fail("No se ha podido visualizar el documento")
                    
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido visualizar el documento")
        
        self.driver.close()
    
    def test_3documentosAnulados(self):

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div[3]/div/button'))).click()
        time.sleep(5)

        try:
            titulo = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div/h2').text
            print("Titulo: ", titulo, "<br>")
            print("---------------------------<br>")

        except NoSuchElementException:
            self.fail("No se encontro información del portal de trabajador (Documentos anulados)")

        try:
            # Obtener el numero del documento
            numero = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[4]').text.strip()
            # Obtener el tipo de documento
            tipodoc = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[5]').text.strip()
            # Obtener quien lo genero
            generado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[6]').text.strip()
            # Obtener cuando se genero
            fecha = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[7]/div').text.strip()
            # Obtener el estado
            estado = self.driver.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[8]/div').text.strip()
        except NoSuchElementException:
            self.fail("No se ha podido encontrar documentos anulados")
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido encontrar documentos anulados")

        # Imprimir los detalles
        print("Ultimo documento:<br>")
        print("Numero: ",numero, "<br>")
        print("Tipo de documento: ",tipodoc, "<br>")
        print("Generado por: ",generado, "<br>")
        print("Generado el: ",fecha, "<br>")
        print("Estado: ",estado, "<br>")
        print("--------------------<br>")

        try:  
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#table-container > div > table > tbody > tr:nth-child(1) > td:nth-child(9) > div > svg.cursor-pointer.not-signed-pen'))).click()

            documento_titulo = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/h2'))).text.strip()
            time.sleep(5)
            print("Documento visualizado: ",documento_titulo, "<br>")

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.full-screen-icon'))).click()
            time.sleep(10)
            print("El documento se esta mostrando correctamente<br>")

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.back-button > span'))).click()
            
        except NoSuchElementException:
            self.fail("No se ha podido visualizar el documento")
                    
        except TimeoutException:
            self.fail("Tiempo de espera agotado: No se ha podido visualizar el documento")

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div > div.employees-portal-content > div > div > div.ant-row.document-viewer-document-wrapper > div.ant-col.d-flex.align-items-center.justify-content-between.ant-col-xs-24 > div.d-none.d-sm-flex > button.ant-btn.ant-btn-default.foco-btn-primary'))).click()
            time.sleep(5)

            quien = self.driver.find_element(By.CSS_SELECTOR, 'span:nth-child(1) > b:nth-child(1)').text.strip()
            fecha = self.driver.find_element(By.CSS_SELECTOR, 'b:nth-child(2)').text.strip()
            comentario = self.driver.find_element(By.CLASS_NAME, 'break-all').text.strip()

            self.driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(4) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > div.flex.justify-end.mt-16 > button').click()

        except NoSuchElementException:
            self.fail("No se ha encontrado el detalle de la anulación")

        print("---------------------------<br>")
        print("Detalle de anulacion:<br>")
        print("Anulado por: ",quien, "<br>")
        print("Anulado el: ",fecha, "<br>")
        print(comentario, "<br>")
        
        self.driver.close()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
