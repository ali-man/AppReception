import datetime

from django.shortcuts import render
from django.views.generic.base import View

from hsm.models import TypeRoom


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
    if list(x)[0] == '0':
        return list(x)[1]
    else:
        return x


def date_list():
    date_format = "%d"
    today = datetime.datetime.now()

    dates = {'date_and_weekday': [], 'date': []}
    for i in range(-3, 12):
        date = today + datetime.timedelta(days=i)
        weekday_num = date.weekday()
        dates['date_and_weekday'].append(F'{int_to_str(weekday_num)} {change_date_num(date.strftime(date_format))}')
        dates['date'].append(change_date_num(date.strftime(date_format)))

    return dates


class ChessViews(View):
    @staticmethod
    def get(request):
        type_rooms = TypeRoom.objects.all()
        dates = date_list()

        context = {
            'type_rooms': type_rooms,
            'weekdays': dates['date_and_weekday'],
            'dates': dates['date'],
            'today': datetime.datetime.now().strftime("%b %Y")
        }
        return render(request, 'chess.html', context=context)

    @staticmethod
    def post(request):
        pass
