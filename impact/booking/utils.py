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


def validate_start_end_datetime_same_day(start_time, end_time):
    """
    validate start_time and end_time are in the same day and end time is after start time
    date: 2003-02-22 10:00:00
    """

    try:
        start_time = get_datetime_obj(start_time)
        end_time = get_datetime_obj(end_time)
        if start_time.date() != end_time.date():
            return False
        if start_time >= end_time:
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


def change_date_format(date: str):
    """
    date: 01-02-2021 or 20-02-2021 10:00:00
    return 2021-02-01 or 2021-02-20 10:00:00
    """
    if len(date) == 10:
        return datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    return datetime.strptime(date,
                             '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


def reverse_change_date_format(date: str):
    """
    date: 2021-02-01 or 2021-02-20 10:00:00
    return 01-02-2021 or 20-02-2021 10:00:00
    """
    if len(date) == 10:
        return datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
    return datetime.strptime(date,
                             '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')


def get_datetime_str(date: datetime):

    return datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
