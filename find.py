import sys
from check_coord import check_spn as chk_spn
from io import BytesIO
import requests
from PIL import Image

adress_input = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": adress_input,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    # обработка ошибочной ситуации
    pass
json_response = response.json()
toponym1 = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
    "boundedBy"]["Envelope"]
low_corn, upper_corn = toponym1["lowerCorner"], toponym1["upperCorner"] # размеры объекта
delta_spn = chk_spn(low_corn, upper_corn)
print(delta_spn)
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы