from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import csv
import json

service = Service('driver/chromedriver.exe')

options = Options()
options.add_argument('--log-level=3')  # Reduce el nivel de log para evitar mensajes innecesarios
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-logging")



#Aqui se inicia el bot
bot = webdriver.Chrome(service=service)
bot.get('https://www.exito.com/')
time.sleep(2)
bot.maximize_window()
time.sleep(2)


#Aqui se busca el producto
input = 'Iphone'
busqueda = bot.find_element(By.XPATH, '//*[@id="header-page"]/section/div/div[1]/div[2]/form/input')
busqueda.send_keys(input)
time.sleep(2)
busqueda.send_keys(Keys.ENTER)
time.sleep(2)

#Quitar cookies
Cookies = bot.find_element(By.CSS_SELECTOR,"#__next > section > div > button")
time.sleep(2)       
Cookies.click()
time.sleep(2)


#Aqui se usa js para obligar a encontrar el boton de vendido por ti ya que ni el scroll ni el click funcionan
try:
    #Buscar botoon "Vendido por" en h4
    filtro = bot.find_element(By.XPATH, '//button[h4[text()="Vendido por"]]')
    #Hacer scroll 
    bot.execute_script("arguments[0].scrollIntoView();", filtro)
    time.sleep(1)
    bot.execute_script("arguments[0].click();", filtro)
    time.sleep(3)
except Exception as e:
    print("No se pudo abrir el filtro 'Vendido por'.")
    print("Error:", e)

try:
    checkbox = bot.find_element(By.XPATH, '//ul[@data-testid="store-list"]//li[label[h3[text()="Éxito"]]]/input')
    bot.execute_script("arguments[0].scrollIntoView();", checkbox)
    time.sleep(1)
    bot.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
except Exception as e:
    print("No se pudo seleccionar 'Éxito'.")
    print("Error:", e)


#Aplicar el filtro
Confirmar = bot.find_element(By.XPATH,'//*[@id="__next"]/main/section[3]/div/div[1]/div[2]/button')
time.sleep(2)       
Confirmar.click()
time.sleep(6)

#Ir siempre por el superior al primer elemento de la lista
descripcion = bot.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li[1]')

print("Descripción del primer Iphone encontrado:")
print(descripcion.text)



with open('primer_producto.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Descripción'])  # Cabecera
    writer.writerow([descripcion.text])  # Contenido del primer producto
    
    
precios = []

# Recolectar precios de la primera página
items_pagina_1 = bot.find_elements(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul')
for item in items_pagina_1:
    try:
        precio = item.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li[1]/article/div[1]/div[2]/div/div/div[2]')
        precios.append(precio.text)
    except:
        continue

# Ir a la segunda página
try:
    boton_siguiente = bot.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[3]/section/div/ul/li[2]')
    time.sleep(1)
    boton_siguiente.click()
    time.sleep(5)

    items_pagina_2 = bot.find_elements(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul')
    for item in items_pagina_2:
        try:
            precio = item.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li[1]/article/div[1]/div[2]/div/div/div[2]')
            precios.append(precio.text)
        except:
            continue
except:
    print("No se pudo acceder a la segunda página.")

# Guardar precios en JSON
with open('precios_iphones.json', mode='w', encoding='utf-8') as file:
    json.dump({'precios': precios}, file, indent=4, ensure_ascii=False)
        


bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(4)



botonInfo = bot.find_element(By.XPATH, '//*[@id="footerLayout"]/section[3]/div/div[1]/button')
botonInfo.click()
time.sleep(5)

#Ese boton realmente no hace nada, pero de igual forma le da click
whatsapp = bot.find_element(By.XPATH, '//*[@id="footerLayout"]/section[3]/div/section/div/div[1]/div[2]/div/p[2]')
whatsapp.click()
time.sleep(5)
bot.save_screenshot('ventas_whatsapp.png')


# Cerrar correctamente
bot.quit()




'''


#Filtrar por vendedor
Filtro = bot.find_element(By.XPATH,'//*[@id="desktop-store-filter-button--19"]')
time.sleep(2)       
Filtro.click()
time.sleep(1)


#Aplicar filtro
AplicarFiltro = bot.find_element(By.CSS_SELECTOR,"#__next > main > section.section.product-gallery_fs-product-listing__HKz9y.layout__content-full > div > div:nth-child(1) > div.Filter_applyButton__1Rk_l > button")
time.sleep(2)       
AplicarFiltro.click()
time.sleep(1)

'''