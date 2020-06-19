import asyncio
import time
from threading import Thread

class WaiterThread(Thread):
	def __init__(self, delay):
		super(WaiterThread, self).__init__()
		self.delay = delay
		
	def wrap(self, func):
		self.func = func
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)
		return wrapper
		
	def run(self, *args, **kwargs):
		time.sleep(self.delay)
		self.func(*args, **kwargs)
		
class AsyncWaiterThread(Thread):
	def __init__(self, delay):
		super(AsyncWaiterThread, self).__init__()
		self.delay = delay
		
	def wrap(self, coro):
		self.coro = coro
		async def wrapper(*args, **kwargs):
			return await self.coro(*args, **kwargs)
		return wrapper
		
	async def run(self, *args, **kwargs):
		await asyncio.sleep(self.delay)
		await self.coro(*args, **kwargs)

# example usage / testing
if __name__ == '__main__':
	from datetime import datetime
	
	loop = asyncio.get_event_loop()
	wt = WaiterThread(5)
	@wt.wrap
	def print1():
		print(f"{datetime.now()} - this should happen after 5 seconds")
		
	awt = AsyncWaiterThread(5)
	@awt.wrap
	async def print2():
		print(f"{datetime.now()} - this should happen after another 5 seconds")
		
	print(f"{datetime.now()} - start")
	wt.run()
	loop.run_until_complete(awt.run())
	