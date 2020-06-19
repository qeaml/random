# random
*some random things I wrote*

## about

in this repo I upload singular files with some random bits of code I wrote, nothing special

I also try to make these usable as "libraries", but nothing's guaranteed

feel free to use these wherever you want (credited or not, but I'd prefer credited)

# table of contents

1. [chance](https://gihub.com/QeaML/random#chance)
2. [code generator](https://gihub.com/QeaML/random#code%20generator)
3. [discord cache](https://gihub.com/QeaML/random#discord%20cache)
4. [tuple from timedelta](https://gihub.com/QeaML/random#tuple%20from%20timedelta)
5. [waiter threads](https://gihub.com/QeaML/random#waiter%20threads)

## chance
A simple script allowing to generate 1 in `n` random bools.

## code generator
Generates an alphanumeric code of the given length.

## discord cache
Enumerates over files copied from Discord's cache and assigns them proper extensions based on the image header.

## tuple from timedelta
Using `divmod` extracts the amount of days, hours, minutes and seconds from a `timedelta` object using it's `total_seconds` method.

## waiter threads
Simple threads which wrap functions ran after a delay from the thread's `.run()` being called. All arguments passed to `run` will be passed to the wrapped function. A function can be wrapped by using the thread's decorator `.wrap`.
