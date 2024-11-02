# -- coding: utf-8 --
"""
Created on Fri Nov  1 15:27:11 2024

@author: Ivan
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
import pandas as pd

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
columnas = ["candidato", "partido", "votos", "porcentaje", "numero de candidatos", "electos", "region", "comuna","local"]
datos=[]
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
    botones = driver.find_elements(By.XPATH, xpath)
    print(f"se encontró el elemento {boton.text} ")
except:
    print("No se encontró el xpath de la lista")

botones[0].click()
print(f"se hizo click en el elemento {boton.text}")
try:
    xpath="//li[@class='MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-1km1ehz']"
    regiones = driver.find_elements(By.XPATH, xpath)
    h=0
    aux=len(regiones)-2
    for i in range(6,aux):
        if h==0:
            region=regiones[i].text
            print(f"Intentando hacer clic en: {regiones[i].text}")
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", regiones[i])
            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
            driver.execute_script("arguments[0].click();", regiones[i])
            print(f"se hizo click en el elemento {regiones[i].text}")
            botones[3].click()
            comunas = driver.find_elements(By.XPATH, xpath)
            print(len(comunas))
            g=0
            for j in range(len(comunas)):
                try:
                    if j+1!=len(comunas):
                        if g==0:
                            comuna=comunas[j].text
                            print(f"Intentando hacer clic en: {comunas[j].text}")
                            time.sleep(1)        
                            driver.execute_script("arguments[0].scrollIntoView();", comunas[j])
                            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                            driver.execute_script("arguments[0].click();", comunas[j])
                            print(f"Se hizo clic en el elemento {comunas[j].text}")
                            botones[4].click()
                            locales=driver.find_elements(By.XPATH, xpath)
                            f=0
                            for k in range(len(locales)):
                                if k+1!=len(locales):
                                    if f==0:
                                        local=locales[k].text
                                        print(f"Intentando hacer clic en: {locales[k].text}")
                                        time.sleep(1)
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k])
                                        print(f"Se hizo clic en el elemento {locales[k].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                        f+=1
                                    else:
                                        local=locales[k-1].text
                                        print(f"Intentando hacer clic en: {locales[k-1].text}")
                                        time.sleep(1)       
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k-1])
                                        print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)    
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                            botones[3].click()
                            time.sleep(1)
                            comunas = driver.find_elements(By.XPATH, xpath)
                            g+=1
                        else:
                            comuna=comunas[j-1].text
                            print(f"Intentando hacer clic en: {comunas[j-1].text}")
                            time.sleep(1)    
                            driver.execute_script("arguments[0].scrollIntoView();", comunas[j-1])
                            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                            driver.execute_script("arguments[0].click();", comunas[j-1])
                            print(f"Se hizo clic en el elemento {comunas[j-1].text}")
                            botones[4].click()
                            locales=driver.find_elements(By.XPATH, xpath)
                            f=0
                            for k in range(len(locales)):
                                if k+1!=len(locales):
                                    if f==0:
                                        local=locales[k].text
                                        print(f"Intentando hacer clic en: {locales[k].text}")
                                        time.sleep(1)    
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k])
                                        print(f"Se hizo clic en el elemento {locales[k].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                        f+=1
                                    else:
                                        local=locales[k-1].text
                                        print(f"Intentando hacer clic en: {locales[k-1].text}")
                                        time.sleep(1)        
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k-1])
                                        print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones=driver.find_elements(By.XPATH, "//div[@class='MuiFormControl-root MuiFormControl-fullWidth css-tzsjye']")
                                        botones[4].click()
                        
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)   
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                            botones[3].click()
                            time.sleep(1)
                            comunas = driver.find_elements(By.XPATH, xpath)
                    else:
                        comuna=comunas[j-1].text
                        print(f"Intentando hacer clic en: {comunas[j-1].text}")
                        time.sleep(1)        
                        driver.execute_script("arguments[0].scrollIntoView();", comunas[j-1])
                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                        driver.execute_script("arguments[0].click();", comunas[j-1])
                        print(f"Se hizo clic en el elemento {comunas[j-1].text}")
                        botones[4].click()
                        locales=driver.find_elements(By.XPATH, xpath)
                        f=0
                        for k in range(len(locales)):
                            if k+1!=len(locales):
                                if f==0:
                                    local=locales[k].text
                                    print(f"Intentando hacer clic en: {locales[k].text}")
                                    time.sleep(1)        
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k])
                                    print(f"Se hizo clic en el elemento {locales[k].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                                    botones[4].click()
                                    time.sleep(1)
                                    locales = driver.find_elements(By.XPATH, xpath)
                                    f+=1
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                                    botones[4].click()
                                    time.sleep(1)
                                    locales = driver.find_elements(By.XPATH, xpath)
                            else:
                                local=locales[k-1].text
                                print(f"Intentando hacer clic en: {locales[k-1].text}")
                                time.sleep(1)  
                                driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                driver.execute_script("arguments[0].click();", locales[k-1])
                                print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                # Localiza la tabla en la página
                                tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                tabla = driver.find_element(By.XPATH, tabla_xpath)
                                
                                # Extrae las filas de la tabla
                                filas = tabla.find_elements(By.TAG_NAME, "tr")
                                
    
                                
                                # Itera por cada fila y cada celda dentro de la fila
                                for fila in filas:
                                    celdas = fila.find_elements(By.TAG_NAME, "td")
                                    fila_datos = [celda.text for celda in celdas]
                                    # Agrega región y comuna a la fila de datos
                                    fila_datos.extend([region, comuna, local])
                                    datos.append(fila_datos)
                                print("Datos obtenidos")
                except Exception as e:
                    print(f"Error al interactuar con la comuna {comunas[j].text}: {str(e)}")
            # Crea un DataFrame con los datos extraídos
            df = pd.DataFrame(datos, columns=columnas)
            df.to_excel(fr"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\tabla_servel_{i}.xlsx", index=False)
            print(f"La tabla ha sido exportada exitosamente a 'tabla_servel_{i}.xlsx'")
            datos=[]
            botones[0].click()
            time.sleep(1)
            regiones = driver.find_elements(By.XPATH, xpath)
            h+=1
            # Exporta el DataFrame a un archivo Excel 
        else:
            region=regiones[i-1].text
            print(f"Intentando hacer clic en: {regiones[i-1].text}")
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", regiones[i-1])
            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
            driver.execute_script("arguments[0].click();", regiones[i-1])
            print(f"se hizo click en el elemento {regiones[i-1].text}")
            botones[3].click()
            comunas = driver.find_elements(By.XPATH, xpath)
            g=0
            for j in range(len(comunas)):
                try:
                    if j+1!=len(comunas):
                        if g==0:
                            comuna=comunas[j].text
                            print(f"Intentando hacer clic en: {comunas[j].text}")
                            time.sleep(1)       
                            driver.execute_script("arguments[0].scrollIntoView();", comunas[j])
                            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                            driver.execute_script("arguments[0].click();", comunas[j])
                            print(f"Se hizo clic en el elemento {comunas[j].text}")
                            botones[4].click()
                            locales=driver.find_elements(By.XPATH, xpath)
                            f=0
                            for k in range(len(locales)):
                                if k+1!=len(locales):
                                    if f==0:
                                        local=locales[k].text
                                        print(f"Intentando hacer clic en: {locales[k].text}")
                                        time.sleep(1)
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k])
                                        print(f"Se hizo clic en el elemento {locales[k].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                        f+=1
                                    else:
                                        local=locales[k-1].text
                                        print(f"Intentando hacer clic en: {locales[k-1].text}")
                                        time.sleep(1)
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k-1])
                                        print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                            botones[3].click()
                            time.sleep(1)
                            comunas = driver.find_elements(By.XPATH, xpath)
                            g+=1
                        else:
                            comuna=comunas[j-1].text
                            print(f"Intentando hacer clic en: {comunas[j-1].text}")
                            time.sleep(1)
                            driver.execute_script("arguments[0].scrollIntoView();", comunas[j-1])
                            # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                            driver.execute_script("arguments[0].click();", comunas[j-1])
                            print(f"Se hizo clic en el elemento {comunas[j-1].text}")
                            botones[4].click()
                            locales=driver.find_elements(By.XPATH, xpath)
                            f=0
                            for k in range(len(locales)):
                                if k+1!=len(locales):
                                    if f==0:
                                        local=locales[k].text
                                        print(f"Intentando hacer clic en: {locales[k].text}")
                                        time.sleep(1)
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k])
                                        print(f"Se hizo clic en el elemento {locales[k].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                        f+=1
                                    else:
                                        local=locales[k-1].text
                                        print(f"Intentando hacer clic en: {locales[k-1].text}")
                                        time.sleep(1)      
                                        driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                        driver.execute_script("arguments[0].click();", locales[k-1])
                                        print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                        # Localiza la tabla en la página
                                        tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                        tabla = driver.find_element(By.XPATH, tabla_xpath)
                                        
                                        # Extrae las filas de la tabla
                                        filas = tabla.find_elements(By.TAG_NAME, "tr")
                                        
            
                                        
                                        # Itera por cada fila y cada celda dentro de la fila
                                        for fila in filas:
                                            celdas = fila.find_elements(By.TAG_NAME, "td")
                                            fila_datos = [celda.text for celda in celdas]
                                            # Agrega región y comuna a la fila de datos
                                            fila_datos.extend([region, comuna, local])
                                            datos.append(fila_datos)
                                        print("Datos obtenidos")
                                        botones[4].click()
                                        time.sleep(1)
                                        locales = driver.find_elements(By.XPATH, xpath)
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                            botones[3].click()
                            time.sleep(1)
                            comunas = driver.find_elements(By.XPATH, xpath)
                    else:
                        comuna=comunas[j-1].text
                        print(f"Intentando hacer clic en: {comunas[j-1].text}")
                        time.sleep(1)
                        driver.execute_script("arguments[0].scrollIntoView();", comunas[j-1])
                        # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                        driver.execute_script("arguments[0].click();", comunas[j-1])
                        print(f"Se hizo clic en el elemento {comunas[j-1].text}")
                        botones[4].click()
                        locales=driver.find_elements(By.XPATH, xpath)
                        f=0
                        for k in range(len(locales)):
                            if k+1!=len(locales):
                                if f==0:
                                    local=locales[k].text
                                    print(f"Intentando hacer clic en: {locales[k].text}")
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k])
                                    print(f"Se hizo clic en el elemento {locales[k].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                                    botones[4].click()
                                    time.sleep(1)
                                    locales = driver.find_elements(By.XPATH, xpath)
                                    f+=1
                                else:
                                    local=locales[k-1].text
                                    print(f"Intentando hacer clic en: {locales[k-1].text}")
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                    # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                    driver.execute_script("arguments[0].click();", locales[k-1])
                                    print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                    # Localiza la tabla en la página
                                    tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                    tabla = driver.find_element(By.XPATH, tabla_xpath)
                                    
                                    # Extrae las filas de la tabla
                                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                                    
        
                                    
                                    # Itera por cada fila y cada celda dentro de la fila
                                    for fila in filas:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        fila_datos = [celda.text for celda in celdas]
                                        # Agrega región y comuna a la fila de datos
                                        fila_datos.extend([region, comuna, local])
                                        datos.append(fila_datos)
                                    print("Datos obtenidos")
                                    botones[4].click()
                                    time.sleep(1)
                                    locales = driver.find_elements(By.XPATH, xpath)
                            else:
                                local=locales[k-1].text
                                print(f"Intentando hacer clic en: {locales[k-1].text}")
                                time.sleep(1)
                                driver.execute_script("arguments[0].scrollIntoView();", locales[k-1])
                                # Usa execute_script para hacer clic mediante JavaScript si es necesario, evitando problemas de interacción
                                driver.execute_script("arguments[0].click();", locales[k-1])
                                print(f"Se hizo clic en el elemento {locales[k-1].text}")
                                # Localiza la tabla en la página
                                tabla_xpath = "//tbody[@class='MuiTableBody-root css-1xnox0e']"
                                tabla = driver.find_element(By.XPATH, tabla_xpath)
                                
                                # Extrae las filas de la tabla
                                filas = tabla.find_elements(By.TAG_NAME, "tr")
                                
    
                                
                                # Itera por cada fila y cada celda dentro de la fila
                                for fila in filas:
                                    celdas = fila.find_elements(By.TAG_NAME, "td")
                                    fila_datos = [celda.text for celda in celdas]
                                    # Agrega región y comuna a la fila de datos
                                    fila_datos.extend([region, comuna, local])
                                    datos.append(fila_datos)
                                print("Datos obtenidos")
                except Exception as e:
                    print(f"Error al interactuar con la comuna {comunas[j].text}: {str(e)}")
            # Crea un DataFrame con los datos extraídos
            df = pd.DataFrame(datos, columns=columnas)
            df.to_excel(fr"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\tabla_servel_{i}.xlsx", index=False)
            print(f"La tabla ha sido exportada exitosamente a 'tabla_servel_{i}.xlsx'")
            datos=[]
            botones[0].click()
            time.sleep(1)
            regiones = driver.find_elements(By.XPATH, xpath)
except Exception as e:
    print(f"{str(e)}")
    
    

# Cierra el navegador
time.sleep(1)
#driver.quit()
