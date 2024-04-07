import re
import win32gui

text = "T11111 No Limot Hlod'em $60 + $5 Table 40"


match = 'Table' + re.search(r'Table(.*)', text).group(1)


if match:
    desired_string = match
    print(desired_string)
else:
    print("Запятая или знак доллара не найдены в тексте.")