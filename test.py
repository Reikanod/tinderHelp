import requests

responce = requests.get(r'https://oyda.ru/wp-content/uploads/2023/12/mash-milash-maksim-1.webp')
url = responce.url

print(url)