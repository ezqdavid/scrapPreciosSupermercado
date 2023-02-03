import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.cotodigital3.com.ar/sitios/cdigi/browse?Nf=product.endDate%7CGTEQ+1.6747776E12%7C%7Cproduct.startDate%7CLTEQ+1.6747776E12&Nr=AND%28product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR%28product.siteId%3ACotoDigital%29%29"
productosFinal = []
i = 0
while url != None:
    print(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        products = soup.find('ul', {'id': 'products'}).find_all('li')
    except:
        break
    for product in products:
        name = product.find('span', {'class': 'span_productName'}).text
        while name.find('\n') != -1:
            name = name.replace('\n', '')
        while name.find('\t') != -1:
            name = name.replace('\t', '')
        price = product.find('span', {'class': 'atg_store_newPrice'}).text
        while price.find('\n') != -1:
            price = price.replace('\n', '')
        while price.find('\t') != -1:
            price = price.replace('\t', '')
        while price.find(' ') != -1:
            price = price.replace(' ', '')
        productosFinal.append({'Nombre': name, 'Precio': price})
    try:
        url = "https://www.cotodigital3.com.ar" +soup.find('a', {'title': 'Siguiente'})['href']
    except:
        break
    i += 1

df = pd.DataFrame(productosFinal)
df.drop_duplicates(inplace=True)
df.to_excel('productosCoto.xlsx', index=False)


    