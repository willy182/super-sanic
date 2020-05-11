

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
