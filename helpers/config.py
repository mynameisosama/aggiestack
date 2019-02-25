def readConfigFile(_filename, _format, _ret_dict):
    try:
        with open(_filename, 'r') as __file:
            __elements = __file.readlines()[1:]
            __file.close()
    except (FileNotFoundError, IndexError) as __err:
        raise __err
    if (not __elements):
        raise AssertionError(
            'Invalid file format'
        )
    try:
        for __element in __elements:
            __temp = __element[:-1].split()
            if (len(__temp) != len(_format) + 1):
                raise AssertionError(
                    'Invalid file format'
                )
            _ret_dict[__temp[0]] = dict(
                zip(
                    _format,
                    __temp[1:]
                )
            )
    except (KeyError, IndexError) as __err:
        raise __err


def preprocessHardwareFile(_filename, _rk_filename, _hw_filename):
    with open(_filename) as __file:
        __data = __file.readlines()
        __file.close()
    __hw_data = list()
    __temp = __data[0]
    for __d in __data[1:]:
        if (not __d[:-1].isdigit()):
            __temp += __d
            continue
        __hw_data.append(__temp)
        __temp = __d
    __hw_data.append(__temp)
    for __i, __name in enumerate([_rk_filename, _hw_filename]):
        with open(__name, 'w') as __file:
            __file.writelines(__hw_data[__i])
            __file.close()


def postprocessRackData(_rk_dict):
    for __rack in _rk_dict:
        _rk_dict[__rack]["images"] = list()
