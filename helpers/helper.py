from datetime import datetime


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