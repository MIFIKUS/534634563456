import re

a = '30% Progressive KO, $11 NLHE [Turbo, Deep Stacks], $1.5K - 100/200 - Tournament 3757079248 Table 9'


print(', '.join(re.split(r', | \$', a)[0:-1]))
#print(a.split(', $'))