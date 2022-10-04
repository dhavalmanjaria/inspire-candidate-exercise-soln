def format_post(request_body):
    if not len(request_body):
        return {}
    request_body = str(request_body)
    all_params = request_body.split('&')

    retval = {}
    for params in all_params:
        item = params.split('=')
        key = item[0]
        val = item[1]
        retval[key] = val

    return retval


