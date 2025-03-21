import re


def is_id(matn):
    pattern = r"^-?\d+$"
    if re.fullmatch(pattern, matn) and matn[0] == "-":
        return True
    else:
        return False
