import re
import pyperclip

parser = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

rgb_color = input(">>> ")
while rgb_color != "-1":
    try:
        parsing_result = parser.search(rgb_color).groups()

        hex_color = "#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result))

        print(hex_color)
        pyperclip.copy(hex_color)
    except Exception as e:
        print(e)
    rgb_color = input(">>> ")