from quart import request

'''
    custom_args filled with dict
    example = {
        "name": "query_param_name",
        "default_value": "default_value_when_args_missing"
    }
'''
async def get_args(custom_args = []):
    args = request.args

    # default query params
    page = args.get("page") if args.get("page") is not None else 1
    limit = args.get("limit") if args.get("limit") is not None else 10
    keywords = args.get("keywords") if args.get("keywords") is not None else ""

    # offset logic
    offset = 0
    page = int(page)
    limit = int(limit)
    if page > 0 and limit > 0:
        offset = (page * limit) - limit

    data = {
        "page": page,
        "offset": offset,
        "limit": limit,
        "keywords": keywords
    }

    # add custom args
    for v in custom_args:
        data[v.get("name")] = args.get(v.get("name")) if args.get(v.get("name")) is not None else v.get("default_value")

    return data