# @@ORIGIN@@ will be replaced in Javascript

from pyodide.http import pyfetch
from os import mkdir
async def get(file):
    response = await pyfetch(f"@@ORIGIN@@/{file}")
    with open(file, "wb") as f:
        f.write(await response.bytes())

files1 = ['quackery.py', 'bigrat.qky', 'extensions.qky', 'turtleduck.qky']
for file in files1:
    # N. B. top-level await is only allowed in Pyodide
    await get(file)

mkdir('sundry')
files2 = ['cards.qky', 'demo.qky', 'fsm.qky', 'heapsort.qky']
for file in files2:
    await get(f'@@ORIGIN@@/sundry/{file}')

from quackery import quackery

quackery(r'''
say "
   ___                   _                      ___        _ _            
  / _ \ _   _  __ _  ___| | _____ _ __ _   _   / _ \ _ __ | (_)_ __   ___ 
 | | | | | | |/ _` |/ __| |/ / _ \ '__| | | | | | | | '_ \| | | '_ \ / _ \
 | |_| | |_| | (_| | (__|   <  __/ |  | |_| | | |_| | | | | | | | | |  __/
  \__\_\\__,_|\__,_|\___|_|\_\___|_|   \__, |  \___/|_| |_|_|_|_| |_|\___|
                                       |___/" cr
say "Welcome to Quackery running on the Pyodide virtual machine." cr

$ 'extensions.qky' dup name? not
dip sharefile and iff
    [ cr say 'Building extensions.' cr quackery ]
else drop

shell''')