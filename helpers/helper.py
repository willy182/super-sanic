from datetime import datetime

import math


def get_value(field, data, default):
    """
    get value from field is exist in data
    and return default value if doesn't
    :param field:
    :param data:
    :param default:
    :return:
    """
    return data[field] if field in data and data[field] != None else default

def get_result_subtraction_time(time1, time2):
    """
    get time from subtraction two times
    :param time1:
    :param time2:
    :return:
    """
    format = '%H:%M:%S.%f'
    times = datetime.strptime(str(time2), format) - datetime.strptime(str(time1), format)
    list_times = str(times).split(':')
    sec, milsec = list_times[len(list_times) - 1].split('.')

    if int(sec) > 0:
        str_time = '{}.{}s'.format(int(sec), int(milsec))
    else:
        str_time = '{}ms'.format(int(milsec))

    return str_time

def meta_data(query, data):
    return {
        'totalRecords': query.total,
        'totalPages': math.ceil(query.total / data.get('limit', 25)),
        'limit': data.get('limit', 25),
        'page': query.current_page,
        'count': query.count()
    }

def get_value_from_dict(adict, key, default):
    return adict.get(key, default)