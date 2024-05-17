import itertools
import requests

def generate_links(length=4):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for code in itertools.product(characters, repeat=length):
        yield f"https://wdho.ru/{''.join(code)}"

generator = generate_links()

for i in range(10000):