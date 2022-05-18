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

print('Downloading quackery.py')
resp = await pyfetch('@@ORIGIN@@/quackery_OOP.py')
quackerytext = await resp.string()

# PATCH - make functions async

NO_INDENT_DEF_RE = re.compile(r'(?<!async )def (?P<name>(?!__)[\w_][\w\d_]*)\(.*\):(?:\n+ {4}.*)+', re.M)
ONE_INDENT_DEF_RE = re.compile(r' {4}(?<!async )def (?P<name>(?!__)[\w_][\w\d_]*)\(.*\):(?:\n+ {8}.*)+', re.M)
CALL_RE = r'(?<!await )((?:ctx\.|self\.)?%s\()'

quackerytext = quackerytext.replace('input(', 'await ainput(').replace('current_item(', 'await current_item(')

asynced_functions = []
for it in count(1):
    done = True
    print('Iteration' it)
    for m in chain(NO_INDENT_DEF_RE.finditer(quackerytext), ONE_INDENT_DEF_RE.finditer(quackerytext)):
        name, body = m.group('name', 0)
        if 'await' in body:
            asynced_functions.append(name)
            print('Doing asyncing of', name)
            quackerytext = quackerytext.replace(body, 'async ' + body)
            done = False
    for name in asynced_functions:
        quackerytext, change_count = re.subn(CALL_RE % name, r'await \1', quackerytext)
        if change_count > 0:
            done = False
            print('Doing await of', name)
    delay(100)
    if done:
        break

for w in ('async', 'await'):
    while f'{w} {w}' in quackerytext:
        print('XX>>', w)
        delay(100)
        quackerytext = quackerytext.replace(f'{w} {w}', w)


quackerytext = rf'''

import js

async def ainput(prompt):
    term = js.term
    term.resume()
    print('\u200c', end='') # &zwnj;
    result = await term.read(prompt)
    term.pause()
    return result

{quackerytext}'''

print('Loading')
with open('quackery.py', 'w') as f: f.write(quackerytext)

#js.term.clear()

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