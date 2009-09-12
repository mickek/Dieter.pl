import re

def parse_quantity(value):
    
    pattern = re.compile(r"([0-9\.,]+)\s*(.*)")
    results = re.search(pattern, value)
    
    if not results: return None, None
    
    quantity, unit_type = float(results.group(1).strip()), results.group(2).strip()
    
    unit_types = {
        "g":          ["g", "gram"],
        "kg":         ["kilogram", "kilo", "kg"],
        "ml":         ["ml"],
        "l":          ["l","litr"],
    }

    for type, values in unit_types.items():
        if unit_type in values: return quantity, type 
    
    if unit_type == '': unit_type = None
    
    return quantity, unit_type