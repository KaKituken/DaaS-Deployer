DATA_TYPE = ['undefined', 'float32', 'uint8', 'int8', 'uint16', 'int16', 'int32', 'int64', 'string', 'boolean', 'float16', 'float64', 'uint32', 'undefined', 'uint64', 'complex128', 'bfloat16']

def parse_tensor(tensor):
    info = {}
    info['name'] = tensor.name
    info['dataType'] = DATA_TYPE[tensor.type.tensor_type.elem_type]
    dims = tensor.type.tensor_type.shape.dim
    shape = []
    for dim in dims:
        shape.append(dim.dim_value)
    info['shape'] = shape
    return info

def parse_fields(fields):
    res = []
    for input in fields:
        info = {}
        info['name'] = input.name
        info['optype'] = input.opType
        info['dataType'] = input.dataType
        info['valueRange'] = input.valuesAsString
        res.append(info)
    return res