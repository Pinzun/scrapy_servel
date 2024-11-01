# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:05:24 2024

@author: pinzunza
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

ruta = "https://elecciones.servel.cl/"

options = Options()
# Elimina la opción headless para ejecutar el navegador con interfaz gráfica
# options.add_argument("--headless")

#service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)

# Navega a la URL especificada
driver.get(ruta)
WebDriverWait(driver, 10).until(EC.title_contains("Resultados"))


#APRIETA EL BOTÓN CORES

#xpath = "//div[@class='MuiStack-root css-68fvpc']/button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-1gvx38z']"
xpath = "//div[@class='MuiStack-root css-68fvpc']//button"
# Encuentra todos los elementos que coinciden con el XPath

try:
    botones = driver.find_elements(By.XPATH, xpath)
    boton=botones[3] 
    print(f"se encontro el elemento {boton.text}")
    time.sleep(5)
    # Intentar hacer clic en el botón
    try:
        boton.click()
        print(f"se hizo click en el elemento {boton.text}")
    except ElementClickInterceptedException:
        # Si el clic es interceptado, intentar con JavaScript
        driver.execute_script("arguments[0].click();", boton)
        print("se intentó hacer click en el elemento boton con java")
except TimeoutException:
    print(f"El botón {boton.text} no se encontró en el tiempo esperado")


#APRIETA BOTON DIVISIÓN ELECTORAL
#xpath_D_electoral = "//button[contains(@class, 'MuiButton-containedPrimary') and contains(@class, 'css-1dptqwv')]"
xpath_D_electoral="//div[@class='MuiStack-root css-18zsr3k']/button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-1dptqwv']"
try:
    boton = driver.find_element(By.XPATH, xpath_D_electoral)
    boton.click()
    print(f"se hizo click en el elemento {boton.text}")

except:
    print("El botón no se encontró en el tiempo esperado")

#RECORRE LISTA DE REGIONES
try:
    xpath="//div[@class='MuiFormControl-root MuiFormControl-fullWidth css-tzsjye']"
    boton = driver.find_element(By.XPATH, xpath)
    print(f"se encontró el elemento {boton.text} ")
except:
    print("No se encontró el xpath de la lista")

boton.click()
print(f"se hizo click en el elemento {boton.text}")
try:
    xpath="//li[@class='MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-1km1ehz']"
    regiones = driver.find_elements(By.XPATH, xpath)
    for region in regiones:
        print(region.text)
        region.click()
except:
    print("No se encontró el xpath de la lista de regiones")
    
    

# Cierra el navegador
time.sleep(1)
driver.quit()
