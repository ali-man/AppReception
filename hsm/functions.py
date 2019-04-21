import datetime

import arrow


def int_to_str(x):
    return {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Вс'
    }[x]


def change_date_num(x):
    # x == '03 05 2019'
    list_x = x.split(' ')
    result = [int(i) for i in list_x]
    # result[0] = result[0][1] if result[0][0] == '0' else result[0]
    # result[1] = result[1][1] if result[1][0] == '0' else result[1]
    return " ".join(result)


def date_list():
    date_format = "%d-%m-%Y"
    today = datetime.datetime.now()

    dates = {
        'full_date': [],
        'timestamp': [],
        'today': F'{today.strftime(date_format)}, {int_to_str(today.weekday())}'
    }
    for i in range(-3, 12):
        date = today + datetime.timedelta(days=i)
        timestamp_format = '%Y, %m, %d'
        dt = [int(i) for i in date.strftime(timestamp_format).split(', ')]
        ts = arrow.get(dt[0], dt[1], dt[2]).timestamp
        weekday_num = date.weekday()
        dates['full_date'].append([
            F'{date.strftime(date_format)}, {int_to_str(weekday_num)}',
            ts
        ])
    return dates
