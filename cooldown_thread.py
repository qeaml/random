from time import sleep
from threading import Thread

class CooldownThread(Thread):
	def __init__(self):
		super(CooldownThread, self).__init__()
		self.name = f"CooldownThread@{id(self)}"
		
		self._cooldowns = dict()
		self._events = dict()

	def __getitem__(self, key):
		return self.get(key)
		
	def __setitem__(self, key, value):
		return self.set(key, value)

	def _register_event(self, name, func):
		if not name in self._events:
			self._events[name] = []
		self._events[name].append(func)

	def _call_event(self, name, *args):
		if not name in self._events:
			return
		for func in self._events[name]:
			func(*args)

	def event(self, *args):
		def decorator(func):
			if len(args) > 0:
				name = args[0]
			else:
				name = func.__name__
			
			self._register_event(name, func)
				
			def wrapper(*args):
				func(*args)
			return wrapper
		return decorator
	
	def set(self, name, amount):
		if isinstance(amount, float):
			amount = int(amount * 100)
		elif isinstance(amount, int):
			pass
		else:
			raise ValueError(
				"from CooldownThread: "
				f"amount must be `int` or `float`, not {type(amount)}!"
			)
		
		self._cooldowns[name] = amount
		
	def get(self, name):
		if not name in self._cooldowns:
			return 0.0

		return self._cooldowns[name] / 100
	
	def run(self):
		while True:
			if len(self._cooldowns.keys()) == 0:
				pass
				
			keys = list(self._cooldowns.keys())
			
			for key in keys:
				self._cooldowns[key] -= 1
				if self._cooldowns[key] == 0:
					del self._cooldowns[key]
					self._call_event("cooldown_end", key)
			sleep(0.01)
				

if __name__ == '__main__':
	ct = CooldownThread()
	
	@ct.event("cooldown_end")
	def cooldown_end_event(cooldown):
		print(f"The cooldown '{cooldown}' has ended.")
		
		if cooldown == "hello":
			print(f"The value of the cooldown 'world' is {ct['world']}.")
		elif cooldown == "world":
			exit()
		
	ct.start()
		
	ct.set("hello", 1.0)
	ct["world"] = 2.0