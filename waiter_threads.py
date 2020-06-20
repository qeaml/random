import asyncio
import time
from threading import Thread

class WaiterThread(Thread):
	def __init__(self, delay):
		super(WaiterThread, self).__init__()
		self.delay = delay
		self._args = ()
		self._kwargs = {}
		
	def wrap(self, func):
		self.func = func
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)
		return wrapper
		
	def run(self):
		time.sleep(self.delay)
		self.func(*self._args, **self._kwargs)
	
	# we have to overwrite the start() function to start the thread whilst
	# alowing us to pass arguments from here to the wrapped func
	def start(self, *args, **kwargs):
		self._args = args
		self._kwargs = kwargs
		super(WaiterThread, self).start()
		
class AsyncWaiterThread(Thread):
	# the only difference between a WaiterThread and an AsyncWaiterThread is
	# that AsyncWaiterThread can wrap a coroutine, whereas a WaiterThread can't
	def __init__(self, delay, loop):
		super(AsyncWaiterThread, self).__init__()
		self.delay = delay
		self.loop = loop
		self._args = ()
		self._kwargs = {}
		
	def wrap(self, coro):
		self.coro = coro
		async def wrapper(*args, **kwargs):
			return await self.coro(*args, **kwargs)
		return wrapper
		
	def run(self):
		task = self.loop.create_task(self.coro(*self._args, **self._kwargs))
		time.sleep(self.delay)
		self.loop.run_until_complete(task)
		
	def start(self, *args, **kwargs):
		self._args = args
		self._kwargs = kwargs
		super(AsyncWaiterThread, self).start()

# example usage / testing
if __name__ == '__main__':
	from datetime import datetime
	
	loop = asyncio.get_event_loop()
	wt = WaiterThread(5)
	@wt.wrap
	def print1(arg):
		print(f"{arg}, {datetime.now()} - this should happen after 5 seconds")
		
	awt = AsyncWaiterThread(7, loop)
	@awt.wrap
	async def print2(arg):
		print(f"{arg}, {datetime.now()} - this should happen after 7 seconds")
		
	print(f"{datetime.now()} - start")
	wt.start("hello")
	awt.start("hi")
	