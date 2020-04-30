import multitasking


def multicall(func, params, *args, **kwargs):
    """
    Calls the same api function several times
    at once and waits until all tasks complete
    before returning.

    :returns dictionary
        {parameter: api result}
    """
    out = {}
    for param in params:
        out[param] = _multitask(
            out, func, param, *args, **kwargs
        )
    multitasking.wait_for_tasks()
    return out


@multitasking.task
def _multitask(out, func, symbol, *args, **kwargs):
    """
    Utility for making the same api call several times
    at once with different parameters.

    :param out: dict: container for returned data
    :param func: api method to call
    :param symbol: the parameter in the api call that is changing
    :param args: arguments for api method
    :param kwargs: arguments for api method

    :return: None: Only populates the 'out' dictionary
    """
    result = func(symbol, *args, **kwargs)
    out[symbol] = result
