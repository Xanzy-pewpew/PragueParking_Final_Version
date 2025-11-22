DLM_V = '#'
DLM_S = '|'    

def encode(v):
    return f"{v.type_code}{DLM_V}{v.reg_nr}"

def decode(slot_str):
    if not slot_str: return []
    v_strs = slot_str.split(DLM_S)
    return [tuple(v_str.split(DLM_V)) for v_str in v_strs if DLM_V in v_str]

def find_in_slot(slot_str, reg_nr):
    reg_nr = reg_nr.upper()
    for v_type, v_reg_nr in decode(slot_str):
        if v_reg_nr == reg_nr:
            return v_type
    return None