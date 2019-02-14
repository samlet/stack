def abbrev(data, l=15):
    if data is None:
        return ""

    info = (data[:l] + '..') if len(data) > l else data
    return info
