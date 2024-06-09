import re

a = '30% Progressive KO, $11 NLHE [Turbo, Deep Stacks], $1.5K - 100/200 - Tournament 3757079248 Table 9'


print(re.search(r'^(.*), \$(.*)K', a).group(1))