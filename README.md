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
6. [cooldown thread](https://github.com/QeaML/random#cooldown-thread)
7. [file dumper](https://github.com/QeaML/random#file-dumper)
8. [FileDumperClient](https://github.com/QeaML/random#filedumperclient)
9. [delta coding](https://github.com/QeaML/random#delta-coding)
10. ["repeat every" threads](https://github.com/QeaML/random#repeat-every-threads)
11. [eval server](https://github.com/QeaML/random#eval-server)
12. [JSON DB](https://github.com/QeaML/random#json-db)

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
from code_generator import generate_code
# prints a 15 character long code
print(generate_code(15))
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

Simple threads which wrap functions ran after a delay from the thread's `.start()` being called. All arguments passed to `start` will be passed to the wrapped function. A function can be wrapped by using the thread's decorator `.wrap`.

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

waiter.start()
waiter2.start(datetime.now()) # the datetime will be passed to waiter2_func
```

## cooldown thread
[*source*](cooldown_thread.py)

Simple thread which constantly decrements all values in an internal `dict`, emitting an event when one reaches zero. Also implements subsctipting.

Example:
```py
from cooldown_thread import CooldownThread

ct = CooldownThread()

@ct.event("cooldown_end")
def cooldown_end_event(cooldown):
	print(f"A cooldown has ended: {cooldown}")
	print(f"The cooldown 'end' will end in {ct['end']} seconds.")
	if cooldown == "restart":
		ct.set("restarted", 10.0)
	elif cooldown == "end":
		exit()

ct["restart"] = 5.0   # 5s
ct['end'] = 10500     # 10500ms == 10.5s
```

## file dumper
[*source*](filedumper.py)

Provides a simple thread-based system for socket-based connections, that allow to dump any utf-8 encoded data into a file through a very simple protocol. Packets are formed like this:

name | index in packet | length | meaning
-----|-----------------|--------|--------
op | `0` | 1 byte | opcode for packet (list below)
data | `1` | 0+ bytes | packet's data

Here's a list of opcodes:

opcode | name | description | has data?
-------|------|-------------|----------
`0x00` | start dump | Starts the file stream. Data is used as filename. | yes
`0x0F` | data | Writes data to the file stream. | yes
`0xFF` | end dump | Ends the file stream and saves all data to file. This also closes the connections | no

Example:
```py
from filedumper import ConnectionThr
from socket import create_server

sock = create_server(("localhost", 33787))
while True:
    c, i = sock.accept()
    ConnectionThr(c).start()
```

## FileDumperClient
[*source*](FileDumperClient.java)

A simple Java program that connects to a [filedumper](https://github.com/QeaML/random#file-dumper) instance (assumed to be running on `localhost:33787`) and allows you to specify a filename and contents of a file.

Usage:

```
javac FileDumperClient.java
java -cp . FileDumperClient
```

## delta coding
[*source*](delta_coding.py)

An implementation of [delta coding](https://en.wikipedia.org/wiki/Delta_encoding).

Example:
```py
from delta_coding import *
l = [10,13,10,6,7,8]
encoded = delta_encode(l)
decoded = delta_decode(encoded)
print(encoded, decoded)
```

## "repeat every" threads
[*source*](repeat_every_threads.py)

Simple threads, based on the [waiter threads](https://github.com/QeaML/random#waiter-threads), which run the wrapped function evey `n` seconds, rather than `n` seconds after the `.start()` call.

Example:
```py
import asyncio
from repeat_every_threads import *
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
```

## eval server
[*source*](eval_server.py)

A simple server which writes all input into a file and then uses a subprocess to evaluate it, then returning the result.

**WARNING:** This server lacks any kind of sandboxing, so watch out I guess.

Example:
```py
from eval_server import *
from socket import create_server

def handle_conn(c):
    ConnectionThr(c).start()
    
server = create_server(('localhost', 33797))
while True:
    c, _ = server.accept()
    handle_conn(c)
```

## JSON DB
[*source*](json_db.py)

A JSON-based serverless database. A cool feature is that the database instead of returning `dict`s as expected, it returns special `DBObject` objects, which function like any other dict, but modifying their contents also modifies their contents in the actual database. Thanks to this, you can make your way through deep these objects (eg. `db['this']['is']['a']['very']['long']['path']`) and all changes you make will be saved.

Example:
```py
from json_db import load

db = load('data.db')
db['key'] = 'value'
db['object'] = {'key':'another value'}
print(db['object']['key']) #another value
db['object']['key'] = 'different value'
print(db['object']['key']) #different value
```

## str to num
[*source*](str_to_num.cpp)

I've been training my C++ skills, so I made this litte program. All it does is ask you for a word and prints the ASCII value of every character.

Usage:
```console
g++ str_to_num.cpp -o str_to_num
str_to_num
```