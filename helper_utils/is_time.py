import re

def is_time_check(time):
    pattern = r"^\d{1,2}\.\d{1,2}\.\d{4}\.\d{1,2}:\d{2}$"
    return bool(re.fullmatch(pattern, time))