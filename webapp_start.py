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
    print(f'Downloading {file}.qky... ', end='')
    # N. B. top-level await is only allowed in Pyodide
    resp = await pyfetch(f'@@ORIGIN@@/{file}.qky')
    text = await resp.string()
    with open(f'{file}.qky', 'w') as f: f.write(text)
    delay(10)
    print('done')

print('Downloading quackery_OOP.py... ', end='')
resp = await pyfetch('@@ORIGIN@@/quackery_OOP.py')
quackerytext = await resp.string()
with open('quackery.py', 'w') as f: f.write(quackerytext)
print('done')

async def ainput(prompt):
    term = js.term
    term.resume()
    print('\u200c', end='') # &zwnj;
    promise = term.read(prompt)
    term.history().enable()
    result = await promise
    term.pause()
    return result

print('Compiling builtins... ', end='')
from quackery import *
qc = QuackeryContext()
print('done')

quackery(r'''$ 'extensions.qky' dup name? not dip sharefile and iff [ say 'Compiling extensions... ' cr quackery say 'done' cr ] else drop''', qc)

print('Starting...')
delay(1000)
js.term.clear()

print(r'''
   ___                   _                      ___        _ _
  / _ \ _   _  __ _  ___| | _____ _ __ _   _   / _ \ _ __ | (_)_ __   ___
 | | | | | | |/ _` |/ __| |/ / _ \ '__| | | | | | | | '_ \| | | '_ \ / _ \
 | |_| | |_| | (_| | (__|   <  __/ |  | |_| | | |_| | | | | | | | | |  __/
  \__\_\\__,_|\__,_|\___|_|\_\___|_|   \__, |  \___/|_| |_|_|_|_| |_|\___|
                                       |___/
      Welcome to Quackery running on the Pyodide virtual machine.
      Don't type 'leave' or you'll break something.''')

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
        qc.to_stack([ord(char) for char in input])
        quackery('quackery 5 nesting put cr echostack nesting release', qc)
await shell_loop()
