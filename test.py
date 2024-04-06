import re
import win32gui

text = '$55 Early Battle [Progressive KO], $10K Gtd - 3,000/6,000 ante 700 - Tournament 3735020833 Table 6'



match = re.search(r'^(.*?),\s*\$', text)

if match:
    desired_string = match.group(1)
    print(desired_string)
else:
    print("Запятая или знак доллара не найдены в тексте.")