import os
from imghdr import what

print("Processing...")
for c in os.walk(".\\discord_cache"):
    for f in c[-1]:
        p = "discord_cache\\" + f
        if not f.startswith("f_"):
            os.remove(p)
            print("Removed " + f)
        else:
            t = what(p)
            if t is not None:
                print(f"Renamed {f} to {f}.{t}")
                os.rename(p, f"{p}.{t}")
            else:
                print("! Could not recognize filetype " + f)
print("\nDone!")
