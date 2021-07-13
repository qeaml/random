from random import choice, randint
from string import ascii_letters

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"

def generate_code(length):
	out = ""
	for _ in range(0, length):
		char = choice(CHARS)
		if not randint(0, 2):
			char = char.upper()
		out += char

if __name__ == '__main__':
	for i in range(5, 11):
		print(generate_code(i))