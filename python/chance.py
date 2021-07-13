from random import randint

def chance_bounds(n):
	lower = -(n // 2)
	upper = n // 2 + n % 2
	return lower, upper
	
def chance(n):
	bounds = chance_bounds(n)
	num = randint(*bounds)
	# will return True if num == 0
	return not num
	
if __name__ == '__main__':
	chances = []
	for _ in range(0, 101):
		chances.append(chance(100))
		
	total = 0
	truthy = 0
	falsey = 0
	for i in chances:
		total += 1
		if i:
			truthy += 1
		else:
			falsey += 1
			
	print(
		f"""Here, have some stats:
		Total: {total}
		Truthy: {truthy}
		Falsey: {falsey}"""
	)
