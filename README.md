# table of contents

- [chance](https://github.com/qeaml/random#chance)
- [code generator](https://github.com/qeaml/random#code-generator)
- [discord cache](https://github.com/qeaml/random#discord-cache)
- [tuple from timedelta](https://github.com/qeaml/random#tuple-from-timedelta)
- [waiter threads](https://github.com/qeaml/random#waiter-threads)
- [cooldown thread](https://github.com/qeaml/random#cooldown-thread)
- [file dumper](https://github.com/qeaml/random#file-dumper)
- [FileDumperClient](https://github.com/qeaml/random#filedumperclient)
- [delta coding](https://github.com/qeaml/random#delta-coding)
- ["repeat every" threads](https://github.com/qeaml/random#repeat-every-threads)
- [eval server](https://github.com/qeaml/random#eval-server)
- [JSON DB](https://github.com/qeaml/random#json-db)
- [dictfile](https://github.com/qeaml/random#dictfile)
- [File Corruptor](https://github.com/qeaml/random#file-corruptor)
- [HumanDir](https://github.com/qeaml/random#humandir)
- [WAV Reader](https://github.com/qeaml/random#wav-reader)
- [GoEval](https://github.com/qeaml/random#goeval)
- [LOC](https://github.com/qeaml/random#loc)

[top]: https://github.com/qeaml/random#table-of-contents

## chance

[_source_](python/chance.py)

A simple script allowing to generate 1 in `n` random bools.

Example:

```py
from chance import *
if chance(15):
    print("this has a 1 in 15 chance of being printed")
```

[_back to top_][top]

## code generator

[_source_](python/code_generator.py)

Generates an alphanumeric code of the given length.

Example:

```py
from code_generator import generate_code
# prints a 15 character long code
print(generate_code(15))
```

[_back to top_][top]

## discord cache

[_source_](python/discordcache.py)

Enumerates over files copied from Discord's cache and assigns them proper extensions based on the image header.

[_back to top_][top]

## tuple from timedelta

[_source_](python/get_timedelta_tuple.py)

Using `divmod` extracts the amount of days, hours, minutes and seconds from a `timedelta` object using it's `total_seconds` method.

Example:

```py
from get_timedelta_tuple import *
from datetime import timedelta
delta = timedelta(hours=49,minutes=44,seconds=13)
print(get_timedelta_tuple(delta))
```

[_back to top_][top]

## waiter threads

[_source_](python/waiter_threads.py)

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

[_back to top_][top]

## cooldown thread

[_source_](python/cooldown_thread.py)

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

[_back to top_][top]

## file dumper

[_source_](filedumper2.go)

Allows you to dump any bytes into a file via a socket on port 33787. Originally
written in Python, but rewrittern in Go. [_see the old version_](python/filedumper.py)

Packet structure.

| name | index in packet | length   | meaning                        |
| ---- | --------------- | -------- | ------------------------------ |
| op   | `0`             | 1 byte   | opcode for packet (list below) |
| data | `1`             | 0+ bytes | packet's data                  |

Opcodes:

| opcode | name     | description                                                     | has data? |
| ------ | -------- | --------------------------------------------------------------- | --------- |
| `0x00` | filename | Sets the filename to the provided data.                         | yes       |
| `0x0F` | data     | Appends it's data to the internal buffer.                       | yes       |
| `0xFF` | dump     | Dumps the internal buffer into the file. Closes the connection. | no        |

Usage:

```shell
go run filedumper2.go
```

[_back to top_][top]

## FileDumperClient

[_source_](FileDumperClient.java)

A simple Java program that connects to a [filedumper](https://github.com/qeaml/random#file-dumper) instance (assumed to be running on `localhost:33787`) and allows you to specify a filename and contents of a file.

Usage:

```shell
javac FileDumperClient.java
java -cp . FileDumperClient
```

[_back to top_][top]

## delta coding

[_source_](python/delta_coding.py)

An implementation of [delta coding](https://en.wikipedia.org/wiki/Delta_encoding).

Example:

```py
from delta_coding import *
l = [10,13,10,6,7,8]
encoded = delta_encode(l)
decoded = delta_decode(encoded)
print(encoded, decoded)
```

[_back to top_][top]

## "repeat every" threads

[_source_](python/repeat_every_threads.py)

Simple threads, based on the [waiter threads](https://github.com/qeaml/random#waiter-threads), which run the wrapped function evey `n` seconds, rather than `n` seconds after the `.start()` call.

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

[_back to top_][top]

## eval server

[_source_](python/eval_server.py)

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

[_back to top_][top]

## JSON DB

[_source_](python/json_db.py)

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

[_back to top_][top]

## dictfile

[_source_](python/dictfile.py)

Simple, cached dict-access to a simply formatted file.

A dictfile looks something like this:

```txt
@ this is a comment

@ empty lines are also ignored

value: "this is str"
this is int: 123
a float: 12.3
my list: ["hello", "world"]

@ all values are python literals
```

Example:

```py
from dictfile import dictfile

df["value"]   # cache miss, will be read from file
df["a float"] # cache miss
df["value"]   # cache hit, since 30 seconds didn't pass

# -- after 30 seconds --
df["value"]   # cache hit, but it's stale, so will read from file
```

[_back to top_][top]

## File Corruptor

[_source_](python/file_corruptor.py)

A simple script that corrupts a portion of any file. You are free to specify how
much corruption you want in your file. The original file remains untouched, and
a second, `.bin` version of the file gets created with the corruption applied.
Use on a `.wav` file for some cool effects!

Example:

```py
from file_corruptor import corrupt

fn = input("Filename to corrupt:\n").strip()
amt = float(input("How much corruption? (%)\n").strip()) / 100
corrupt(fn, amt)
```

[_back to top_][top]

## HumanDir

[_source_](python/humandir.py)

A more human-friendly way to interact with directories. Can create subdirectories,
files and subdirectory hierarchiies. Also allows to run commands from the
directory object itself.

Example:

```py
from humandir import directory

projname = input("Project name?\n")

# get the root folder our project will be stored in
root = directory.from_str("/projects")
# create the project directory
projdir = root.ensure_dir(projname)
# create multiple directories within the project directory
projdir.ensure_all_dirs("src", "data")
# create an empty file
projdir.ensure_file(".gitignore")
# create and write to a file
projdir.dump_file_str("README.md", f"# {projname}")
# initialize a git repo in the directory
projdir.cmd("git","init")
# start VS Code
projdir.cmd("code", ".")

print("Done :)")
```

[_back to top_][top]

## WAV Reader

[_source_](wavreader.go)

A program that reads RIFF WAVE files. You simply provide it with a filename to
open and it'll display some basic information about the file.

Usage:

```sh
go run wavreader.go
```

[_back to top_][top]

## GoEval

[_source_](goeval.go)

A program that is essentially a REPL for Go. You launch it, give it a handful
of lines of code and it quickly runs it. It's not stupid either! It fully
supports imports (via `//+import ...`, watch out with `_` and `.` though!), and
automatically `get`s external packages (from GitHub, gopkg.in, etc.).

Usage:

```sh
go run goeval.go
```

Example usage:

```sh
$ go run goeval.go
GoEval v1
>> //+import fmt
Added import: fmt
>> fmt.Println("Hello")
>>
creating module...
go: creating new go.mod: module goeval
go: to add module requirements and sums:
        go mod tidy
getting external packages...
running code...
==================================================
Hello
```

[_back to top_][top]

## loc

[_source_](loc.c)

LOC is a tiny C/C++ program to calculate the line count of any files. It
only counts blank lines and lines with content. Comment line counting might
be implemented at a later date.

Using the program is simple. Every argument passed to the program will be used
as a name of a directory to count.

```sh
$ loc loc
qeaml's loc v2
File,Blank,Comment,Content
loc/dir.cpp,2,0,9
loc/dir.h,6,0,11
loc/loc.c,21,0,90
*,29,0,110
```

```sh
$ loc loc > loc.csv
$ cat loc.csv
File,Blank,Comment,Content
loc/dir.cpp,2,0,9
loc/dir.h,6,0,11
loc/loc.c,21,0,90
*,29,0,110
```

The output is a CSV sheet containing per-file information and the totals for
all files (under `*`).

LOC is split into 2 parts: the main program written in C and the directory
iteration written in C++. You have to compile them separately, but link them
together into one.

```sh
# For example, with Clang:
# Compile dir.o
clang -O3 -o dir.o -c dir.cpp
# Then compile and link loc.c with the compiled dir.o
clang -O3 -o loc loc.c dir.o
```

[_back to top_][top]
