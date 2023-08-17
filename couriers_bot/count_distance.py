import sys


import mpu

""" функция считает выдает отфильтрованный список ближайших к введенному коду курьеров """
def find_nearest_couriers(zip_code_sf, zip_codes_4, couriers_):

    black_list_status = ['Problem', 'Problems', 'DIE', 'Проблемный', 'Suspicious', 'HOT', 'Проблемы', 'Недоступен', 'RIP', 'Dead', 'Not in work']

    couriers = []
    for courier in couriers_:
      if courier[5] not in black_list_status:

        """ если зип код через тире 2421-241, обрезает все после - """
        if '-' in courier[3]:
            zip_code__ = courier[3].split('-')[0]
            
        else:
            zip_code__ = courier[3]
        couriers.append({
          'town': courier[1],
          'state': f'{courier[2]}',
          'zip_code': f'{zip_code__}',
          'expired': courier[4],
          'status': courier[5],
          'service': courier[6]
        })

    """ получается ширину и долготу введенного курьера, используя данные файла data/zip_codes_usa.json """
    zip_codes_n_distances_list = []
    zip_codes_list = list(zip_codes_4)
    lat_1 = zip_codes_4[zip_code_sf]["lat"]
    lng_1 = zip_codes_4[zip_code_sf]["lng"]
    for zip_code in zip_codes_list:
        lat_2 = zip_codes_4[zip_code]["lat"]
        lng_2 = zip_codes_4[zip_code]["lng"]
        """ считает дистанцию между введенным зип кодом и каждым из списка """
        distance = mpu.haversine_distance((lat_1, lng_1), (lat_2, lng_2))
        zip_codes_n_distances_list.append(
            {
                "zip_code": zip_code,
                "distance": distance
            }
        )

    """ сортирует полученный список по дистанции """
    zip_codes_n_distances_list.sort(key=lambda x: x["distance"])
    nearest_couriers = []

    """ добавляет в список ближайших """
    for zip_code_n_distance in zip_codes_n_distances_list:
        if len(nearest_couriers) == 20:
            break
        for courier in couriers:
            if courier['zip_code'] == zip_code_n_distance["zip_code"]:
                courier["distance"] = zip_code_n_distance["distance"]
                nearest_couriers.append(courier)


    return nearest_couriers
