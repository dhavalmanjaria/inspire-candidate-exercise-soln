def get_sanitized_value(val):
    val = val.replace('--', '')
    val = val.replace(';', '')

    return val