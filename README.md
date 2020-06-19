# random
*some random things I wrote*

## about

in this repo I upload singular files with some random bits of code I wrote, nothing special

I also try to make these usable as "libraries", but nothing's guaranteed

feel free to use these wherever you want (credited or not, but I'd prefer credited)

# table of contents

1. [chance](https://github.com/QeaML/random#chance)
2. [code generator](https://github.com/QeaML/random#code-generator)
3. [discord cache](https://github.com/QeaML/random#discord-cache)
4. [tuple from timedelta](https://github.com/QeaML/random#tuple-from-timedelta)
5. [waiter threads](https://github.com/QeaML/random#waiter-threads)

## chance
[*source*](chance.py)

A simple script allowing to generate 1 in `n` random bools.

Example:
```py
from chance import *
if chance(15):
    print("this has a 1 in 15 chance of being printed")
```

## code generator
[*source*](code_generator.py)

Generates an alphanumeric code of the given length.

Example:
```py
from code_generator import *
# prints a seven character long code
print(c(7))
```

## discord cache
[*source*](discordcache.py)

Enumerates over files copied from Discord's cache and assigns them proper extensions based on the image header.

## tuple from timedelta
[*source*](get_timedelta_tuple.py)

Using `divmod` extracts the amount of days, hours, minutes and seconds from a `timedelta` object using it's `total_seconds` method.

Example:
```py
from get_timedelta_tuple import *
from datetime import timedelta
delta = timedelta(hours=49,minutes=44,seconds=13)
print(get_timedelta_tuple(delta))
```

## waiter threads
[*source*](waiter_threads.py)

Simple threads which wrap functions ran after a delay from the thread's `.run()` being called. All arguments passed to `run` will be passed to the wrapped function. A function can be wrapped by using the thread's decorator `.wrap`.

Example:
```py
from waiter_threads import *
from datetime import datetime

waiter = WaiterThread(7) # will wait for 7 seconds
waiter2 = WaiterThread(0.5) # will wait for half a second

@waiter.wrap
def waiter_func():
    print("7 seconds have passed!")

@waiter2.wrap
def waiter2_func(dt):
    print(f"half a second has passed since {dt}")

waiter.run()
waiter2.run(datetime.now()) # the datetime will be passed to waiter2_func
```
