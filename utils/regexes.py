import re

def contains_non_numeric_char(input_string):
    """Checks if a string contains any non-numeric characters using regex."""
    return bool(re.search(r"[^0-9]", input_string))

def is_whitespace(input_string):
    t=' ','\t','\n','\r'
    return input_string.startswith(t) or input_string.endswith(t)
