import asyncio
import time
from threading import Thread

class RepeatEveryThread(Thread):
    def __init__(self, delay):
        super(RepeatEveryThread, self).__init__()
        self.delay = delay
        self.repeats = 0
        self._alive = True
        
    def wrap(self, func):
        self.func = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
        
    def run(self):
        while self._alive:
            time.sleep(self.delay)
            self.repeats += 1
            self.func()

    def stop(self):
        if self._alive:
            self._alive = False
        else:
            raise RuntimeError("attempt to stop a dead thread.")
        
class AsyncRepeatEveryThread(Thread):
    # the only difference between RepeatEveryThread and AsyncRepeatEveryThread 
    # is that AsyncWaiterThread can wrap a coroutine, whereas RepeatEveryThread 
    # can't
    def __init__(self, delay, loop):
        super(AsyncRepeatEveryThread, self).__init__()
        self.delay = delay
        self.loop = loop
        self.repeats = 0
        self._alive = True
        
    def wrap(self, coro):
        self.coro = coro
        async def wrapper(*args, **kwargs):
            return await self.coro(*args, **kwargs)
        return wrapper
        
    def run(self):
        while self._alive:
            task = self.loop.create_task(self.coro())
            time.sleep(self.delay)
            self.repeats += 1
            self.loop.run_until_complete(task)
        
    def stop(self):
        if self._alive:
            self._alive = False
        else:
            raise RuntimeError("attempt to stop a dead thread.")

# example usage / testing
if __name__ == '__main__':
    from datetime import datetime
    
    loop = asyncio.get_event_loop()
    ret = RepeatEveryThread(5)
    @ret.wrap
    def print1():
        print(f"{datetime.now()} - this should happen every 5 seconds"
        f" (# {ret.repeats})")
        
    aret = AsyncRepeatEveryThread(7, loop)
    @aret.wrap
    async def print2():
        print(f"{datetime.now()} - this should happen every 7 seconds" 
        f" (# {aret.repeats})")
        
    print(f"{datetime.now()} - start")
    ret.start()
    aret.start()
    