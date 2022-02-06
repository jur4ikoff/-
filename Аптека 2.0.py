import requests
import sys
import math
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
response2 = requests.get(search_api_server, params=search_params)
if not response2:
    # ...
    pass

json_response = response2.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_coord = organization["geometry"]["coordinates"]
adress = json_response["features"][0]["properties"]["description"]
name = json_response["features"][0]["properties"]["name"]
shedule = json_response["features"][0]["properties"]["CompanyMetaData"]["Hours"]["text"]
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


def get_distance(lat_1, lng_1, lat_2, lng_2):
    lat_1, lng_1, lat_2, lng_2 = float(lat_1), float(lng_1), float(lat_2), float(lng_2)
    d_lat = float(lat_2) - float(lat_1)
    d_lng = float(lng_2) - float(lng_1)

    temp = (
            math.sin(d_lat / 2) ** 2
            + math.cos(lat_1)
            * math.cos(lat_2)
            * math.sin(d_lng / 2) ** 2
    )
    a = 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))
    a = str(a).split('.')
    return a[0] + " метров"


lat = coord_start_low.split(' ')
lat_1, lng_1 = lat
lat2 = coord_point.split(' ')
lat_2, lng_2 = lat2
meters = get_distance(lat_1, lng_1, lat_2, lng_2)

print(adress, name, shedule, meters, sep="; ")
map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
