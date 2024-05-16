
with open('closed_tables.txt', 'r', encoding='utf-8') as ff:
    sdf = ff.read().split('\n')
    f = [a for a in sdf if a != '']
    print(f)