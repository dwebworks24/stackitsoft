from apps.home.models import *
from django.db.models import Max


def generate_shop_number():
    max_value = Users.objects.aggregate(max_value=Max('id'))
    if max_value['max_value'] is None:
        id = 1
        shop_number = f'rcb-{id}'
    else:
        id = max_value['max_value'] + 1
        shop_number = f'rcb-{id}'

    return shop_number 
