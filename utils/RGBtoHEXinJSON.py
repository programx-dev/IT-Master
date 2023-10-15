import json
import re

def rgb_to_hex_rex(dct):
    for key, val in dct.items():
        if isinstance(val, dict): 
            rgb_to_hex_rex(val)
        else:
            parsing_result = parser.search(val)

            if parsing_result is not None:
                parsing_result = parsing_result.groups()

                dct[key] = "#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result))

parser = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")
            
with open("file.json", "r+", encoding = "utf-8") as file:
    data = json.load(file)

    file.truncate(0)
    file.seek(0)

    rgb_to_hex_rex(data)

    json.dump(data, file, indent = 2, ensure_ascii = False)