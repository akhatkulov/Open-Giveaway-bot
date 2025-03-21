from datetime import datetime


def is_past_time(day, month, year, time_str):
    given_time = datetime.strptime(f"{day} {month} {year} {time_str}", "%d %m %Y %H:%M")
    return given_time < datetime.now()
