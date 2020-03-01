import os
from imghdr import what
from distutils.dir_util import copy_tree

print('Renaming and removing files...')
for c in os.walk('.\\discord_cache'):
  for f in c[-1]:
    p = 'discord_cache\\'+f
    if not f.startswith('f_'):
      os.remove(p)
      print('Removed '+f)
    else:
      t = what(p)
      if t is not None:
        print(f'Renamed {f} to {f}.{t}')
        os.rename(p, f'{p}.{t}')
      else:
        os.remove(p)
        print('Removed '+f)
print('Done!')