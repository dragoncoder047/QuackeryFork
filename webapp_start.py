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
resp = await pyfetch('@@ORIGIN@@/quackery_OOP.py')
quackerytext = await resp.string()
with open('quackery.py', 'w') as f: f.write(quackerytext)

js.term.clear()

async def ainput(prompt):
    term = js.term
    term.resume()
    print('\u200c', end='') # &zwnj;
    result = await term.read(prompt)
    term.pause()
    return result

from quackery import quackery, QuackeryContext
qc = QuackeryContext()
print(r'''
   ___                   _                      ___        _ _
  / _ \ _   _  __ _  ___| | _____ _ __ _   _   / _ \ _ __ | (_)_ __   ___
 | | | | | | |/ _` |/ __| |/ / _ \ '__| | | | | | | | '_ \| | | '_ \ / _ \
 | |_| | |_| | (_| | (__|   <  __/ |  | |_| | | |_| | | | | | | | | |  __/
  \__\_\\__,_|\__,_|\___|_|\_\___|_|   \__, |  \___/|_| |_|_|_|_| |_|\___|
                                       |___/
      Welcome to Quackery running on the Pyodide virtual machine.
      Don't type 'leave' or you'll break something.''')

quackery(r'''$ 'extensions.qky' dup name? not dip sharefile and iff [ cr say 'Building extensions...' cr quackery ] else drop''', qc)

async def shell_loop():
    while True:
        prompt = '/O> '
        input = ''
        while True:
            i = await ainput(prompt)
            input += i + '\n'
            prompt = '... '
            if not i:
                break
        ctx.to_stack([ord(char) for char in input])
        quackery('quackery 5 nesting put cr echostack nesting release')
await shell_loop()
