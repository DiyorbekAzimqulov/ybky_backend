from datetime import datetime


def validate_date(date):
    """
    validate date is in the future
    date: 2003-02-22
    """
    try:
        date = get_datetime_obj_for_date(date).date()
        if date < datetime.now().date():
            return False
        return True
    except ValueError:
        return False


def validate_datetime(date):
    """
    validate date is in the future
    date: 2003-02-22 10:00:00
    """
    try:
        date = get_datetime_obj(date).date()
        if date < datetime.now().date():
            return False
        return True
    except ValueError:
        return False


def get_datetime_obj_for_date(date: str):
    """
    date: 2003-02-22
    """
    return datetime.strptime(date, '%Y-%m-%d')


def get_datetime_obj(date: str):
    """
    date: 2003-02-22 10:00:00
    """
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')