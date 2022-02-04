import sys, os
import requests


def who_is_south(dict_city):
    sorted_values = sorted(dict_city.values())
    city_coord = sorted_values[0]

    for key in dict_city:
        if city_coord == dict_city[key]:
            return key


req_list = []
a = str(input()).replace(' ', '')
a = a.split(',')
for i in a:
    req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
          + str(i) + "&format=json"
    req_list.append(req)
coord_list = {}
for out in req_list:
    response = requests.get(out)
    if response:
        json_response = response.json()
        try:
            city = json_response["response"]["GeoObjectCollection"]["metaDataProperty"][
                "GeocoderResponseMetaData"]["request"]  # город
            find_coord = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["boundedBy"]["Envelope"]["lowerCorner"]
            need_coord = find_coord.split()[1]  # координата
            coord_list[city] = need_coord
        except Exception as e:
            print("Города " + city + " не существует")
            print(json_response)
            print(e)
    else:
        print("Ошибка выполнения запроса:")
        print(out)
        print("Http статус:", response.status_code, "(", response.reason, ")")

print(who_is_south(coord_list))
