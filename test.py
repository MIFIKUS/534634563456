import re

a = '$5.50 NLHE, $1K'

pattern = r", \$(.*?)K"

# Ищем все совпадения и берём последнее
matches = re.search(r", \$(.*?)K", a).group(0)
matches.replace(' ', '')
matches.replace(',', '')


print(result)