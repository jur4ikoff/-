import requests

n = input()


def find_coord(n):
    req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
          + str(n) + "&format=json"
    resp = requests.get(req)
    if resp:
        json_resp = resp.json()
        find_coord = json_resp["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["boundedBy"]["Envelope"]["lowerCorner"]
        return find_coord


req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
      + str(find_coord(n)) + "&format=json&kind=metro"
response = requests.get(req)
if response:
    json_response = response.json()
    try:
        metro1 = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
        if 'метро' in metro1[4]["name"]:
            print(metro1[4]["name"])
        if 'метро' in metro1[5]["name"]:
            print(metro1[5]["name"])
    except IndexError:
        pass
else:
    print("Ошибка выполнения запроса:")
    print(req)
    print("Http статус:", response.status_code, "(", response.reason, ")")
