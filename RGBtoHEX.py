import re

parser = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

while True:
    rgb_color = input()

    parsing_result = parser.search(rgb_color).groups()

    hex_color = "#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result))

    print(hex_color)