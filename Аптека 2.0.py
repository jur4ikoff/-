import requests
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
response_geo = requests.get(geocoder_api_server, params=geocoder_params)
if not response_geo:
    # обработка ошибочной ситуации
    pass
json_response = response_geo.json()
coord_start = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
    "boundedBy"]["Envelope"]
coord_start_low = coord_start["lowerCorner"]
coord_start_low1 = coord_start_low.replace(' ', ',')

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
search_api_server = "https://search-maps.yandex.ru/v1/"
address_ll = ','.join(coord_start_low.split(' '))
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    # ...
    pass

json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_coord = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(org_coord[0], org_coord[1])
coord_point = "{0} {1}".format(org_coord[0], org_coord[1])
delta = chk_spn(coord_start_low, coord_point)
delta0, delta1 = delta
if float(delta0) < 0.01 or float(delta1) < 0.01:
    delta0 += 0.01
    delta1 += 0.01
map_params = {
    "ll": address_ll,
    "spn": ",".join([str(delta0), str(delta1)]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl~{1},pm2dgl".format(org_point, coord_start_low1)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
