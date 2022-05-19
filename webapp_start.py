# @@ORIGIN@@ will be replaced in Javascript

from pyodide.http import pyfetch
from os import mkdir
import re
import js
from itertools import count, chain

async def delay(time):
    await js.Promise.new(lambda resolve, reject: js.setTimeout(resolve, time))

mkdir('sundry')
files = ['bigrat', 'extensions', 'turtleduck', 'sundry/cards', 'sundry/demo', 'sundry/fsm', 'sundry/heapsort']

for file in files:
    # N. B. top-level await is only allowed in Pyodide
    resp = await pyfetch(f'@@ORIGIN@@/{file}.qky')
    print(f'Downloading {file}.qky')
    text = await resp.string()
    with open(f'{file}.qky', 'w') as f: f.write(text)

print('Downloading quackery_OOP_ASYNC.py')
resp = await pyfetch('@@ORIGIN@@/quackery_OOP_ASYNC.py')
quackerytext = await resp.string()
with open('quackery.py', 'w') as f: f.write(quackerytext)

js.term.clear()

from quackery import quackery
print(r'''
   ___                   _                      ___        _ _
  / _ \ _   _  __ _  ___| | _____ _ __ _   _   / _ \ _ __ | (_)_ __   ___
 | | | | | | |/ _` |/ __| |/ / _ \ '__| | | | | | | | '_ \| | | '_ \ / _ \
 | |_| | |_| | (_| | (__|   <  __/ |  | |_| | | |_| | | | | | | | | |  __/
  \__\_\\__,_|\__,_|\___|_|\_\___|_|   \__, |  \___/|_| |_|_|_|_| |_|\___|
                                       |___/
      Welcome to Quackery running on the Pyodide virtual machine.''')
await quackery(r'''$ 'extensions.qky' dup name? not
dip sharefile and iff [
    cr say 'Building extensions...' cr
    quackery
] else
    drop
shell''')