from pandas import Series, DataFrame
from _pandasujson import loads, dumps

@classmethod
def from_json(cls, json, orient="index", dtype=None, numpy=True):
    """
    Convert JSON string to Series

    Parameters
    ----------
    json : The JSON string to parse.
    orient : {'split', 'records', 'index'}, default 'index'
        The format of the JSON string
        split : dict like
            {index -> [index], name -> name, data -> [values]}
        records : list like [value, ... , value]
        index : dict like {index -> value}
    dtype : dtype of the resulting Series
    nupmpy: direct decoding to numpy arrays. default True but falls back
        to standard decoding if a problem occurs.

    Returns
    -------
    result : Series
    """
    s = None

    if dtype is not None and orient == "split":
        numpy = False

    if numpy:
        try:
            if orient == "split":
                decoded = loads(json, dtype=dtype, numpy=True)
                decoded = dict((str(k), v) for k, v in decoded.iteritems())
                s = Series(**decoded)
            elif orient == "columns" or orient == "index":
                s = Series(*loads(json, dtype=dtype, numpy=True,
                                  labelled=True))
            else:
                s = Series(loads(json, dtype=dtype, numpy=True))
        except ValueError:
            numpy = False
    if not numpy:
        if orient == "split":
            decoded = dict((str(k), v)
                           for k, v in loads(json).iteritems())
            s = Series(dtype=dtype, **decoded)
        else:
            s = Series(loads(json), dtype=dtype)

    return s
Series.from_json = from_json

def to_json(self, orient="index", double_precision=10, force_ascii=True):
    """
    Convert Series to a JSON string

    Note NaN's and None will be converted to null and datetime objects
    will be converted to UNIX timestamps.

    Parameters
    ----------
    orient : {'split', 'records', 'index'}, default 'index'
        The format of the JSON string
        split : dict like
            {index -> [index], name -> name, data -> [values]}
        records : list like [value, ... , value]
        index : dict like {index -> value}
    double_precision : The number of decimal places to use when encoding
        floating point values, default 10.
    force_ascii : force encoded string to be ASCII, default True.

    Returns
    -------
    result : JSON compatible string
    """
    return dumps(self, orient=orient, double_precision=double_precision,
                 ensure_ascii=force_ascii)
Series.to_json = to_json


@classmethod
def from_json(cls, json, orient="columns", dtype=None, numpy=True):
    """
    Convert JSON string to DataFrame

    Parameters
    ----------
    json : The JSON string to parse.
    orient : {'split', 'records', 'index', 'columns', 'values'},
             default 'columns'
        The format of the JSON string
        split : dict like
            {index -> [index], columns -> [columns], data -> [values]}
        records : list like [{column -> value}, ... , {column -> value}]
        index : dict like {index -> {column -> value}}
        columns : dict like {column -> {index -> value}}
        values : just the values array
    dtype : dtype of the resulting DataFrame
    nupmpy: direct decoding to numpy arrays. default True but falls back
        to standard decoding if a problem occurs.

    Returns
    -------
    result : DataFrame
    """
    df = None

    if dtype is not None and orient == "split":
        numpy = False

    if numpy:
        try:
            if orient == "columns":
                args = loads(json, dtype=dtype, numpy=True, labelled=True)
                if args:
                    args = (args[0].T, args[2], args[1])
                df = DataFrame(*args)
            elif orient == "split":
                decoded = loads(json, dtype=dtype, numpy=True)
                decoded = dict((str(k), v) for k, v in decoded.iteritems())
                df = DataFrame(**decoded)
            elif orient == "values":
                df = DataFrame(loads(json, dtype=dtype, numpy=True))
            else:
                df = DataFrame(*loads(json, dtype=dtype, numpy=True,
                                      labelled=True))
        except ValueError:
            numpy = False
    if not numpy:
        if orient == "columns":
            df = DataFrame(loads(json), dtype=dtype)
        elif orient == "split":
            decoded = dict((str(k), v)
                           for k, v in loads(json).iteritems())
            df = DataFrame(dtype=dtype, **decoded)
        elif orient == "index":
            df = DataFrame(loads(json), dtype=dtype).T
        else:
            df = DataFrame(loads(json), dtype=dtype)

    return df
DataFrame.from_json = from_json


def to_json(self, orient="columns", double_precision=10,
            force_ascii=True):
    """
    Convert DataFrame to a JSON string.

    Note NaN's and None will be converted to null and datetime objects
    will be converted to UNIX timestamps.

    Parameters
    ----------
    orient : {'split', 'records', 'index', 'columns', 'values'},
             default 'columns'
        The format of the JSON string
        split : dict like
            {index -> [index], columns -> [columns], data -> [values]}
        records : list like [{column -> value}, ... , {column -> value}]
        index : dict like {index -> {column -> value}}
        columns : dict like {column -> {index -> value}}
        values : just the values array
    double_precision : The number of decimal places to use when encoding
        floating point values, default 10.
    force_ascii : force encoded string to be ASCII, default True.

    Returns
    -------
    result : JSON compatible string
    """
    return dumps(self, orient=orient, double_precision=double_precision,
                 ensure_ascii=force_ascii)
DataFrame.to_json = to_json

def maybe_to_json(obj=None):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    return obj
