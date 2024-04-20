import os

df = 'E:\\Projects\\PokerStarsParser\\deals_files'

dfdfdf = os.listdir(df)

for i in dfdfdf:
    print(i)
    with open(f'{df}\\{i}', 'w') as a:
        a.write('123')