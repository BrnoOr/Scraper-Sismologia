from bs4 import BeautifulSoup
import requests
from lxml import etree
from datetime import datetime, timedelta
import re
import pandas as pd
import time

init_date = datetime(2000,1,1)
finish_date = datetime(2024,11,30)

date_list = [(init_date+ timedelta(days=i)).strftime('%Y-%m-%d')
             for i in range((finish_date-init_date).days+1)]
dic_date = {
    f"{fecha}":[
        fecha[0:4],
        fecha[5:7],
        fecha[8:10],
        re.sub('-','',fecha)
    ]
    for fecha in date_list
}
url_list = [f'https://sismologia.cl/sismicidad/catalogo/{periodo[0]}/{periodo[1]}/{periodo[3]}.html' for periodo in dic_date.values()]
del date_list,dic_date, init_date,finish_date

data = pd.DataFrame(columns=['Fecha Local / Lugar', 'Fecha UTC', 'Latitud / Longitud', 'Profundidad','Magnitud (2)'])
init_time = time.time()
for url in url_list:
    
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        dom = etree.HTML(str(soup))
        element = dom.xpath('//*[@id="page"]/article/table')
        tabla = pd.read_html(etree.tostring(element[0], method="html"))[0]
        data = pd.concat([data,tabla])
    except:
        print('URL con problemas:',url)
        continue
end_time = time.time()
print('tiempo del proceso:',round((end_time-init_time)/60,2),'Seg')
