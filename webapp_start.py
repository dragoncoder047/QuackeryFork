# @@ORIGIN@@ will be replaced in Javascript

from pyodide.http import pyfetch
from os import mkdir
import re
import js
from itertools import count, chain

mkdir('sundry')
files = ['bigrat', 'extensions', 'turtleduck', 'sundry/cards', 'sundry/demo', 'sundry/fsm', 'sundry/heapsort']

for file in files:
    # N. B. top-level await is only allowed in Pyodide
    resp = await pyfetch(f'@@ORIGIN@@/{file}.qky')
    print(f'Downloading {file}.qky', flush=True)
    text = await resp.string()
    with open(f'{file}.qky', 'w') as f: f.write(text)

print('Downloading quackery.py', flush=True)
resp = await pyfetch('@@ORIGIN@@/quackery_OOP.py')
quackerytext = await resp.string()

# PATCH - make functions async

NO_INDENT_DEF_RE = re.compile(r'(?<!async )def (?P<name>[\w_][\w\d_]*)\(.*\):(?:\n+ {4}.*)+', re.M)
ONE_INDENT_DEF_RE = re.compile(r' {4}(?<!async )def (?P<name>[\w_][\w\d_]*)\(.*\):(?:\n+ {8}.*)+', re.M)
CALL_RE = r'(?<!await )(?:ctx\.|self\.)?%s\('

quackerytext = quackerytext.replace('input(', 'await ainput(').replace('current_item(', 'await current_item(')

done = False
asynced_functions = []
while not done:
    done = True
    for m in chain(NO_INDENT_DEF_RE.finditer(quackerytext), ONE_INDENT_DEF_RE.finditer(quackerytext)):
        name, body = m.group('name', 0)
        if 'await' in body:
            asynced_functions.append(name)
            print('Doing asyncing of', name, flush=True)
            quackerytext = quackerytext.replace(body, 'async ' + body)
            done = False
    for name in asynced_functions:
        quackerytext, change_count = re.subn(CALL_RE % name, quackerytext)
        if change_count > 0:
            done = False
            print('Doing await of', name, flush=True)

for w in ('async', 'await'):
    while f'{w} {w}' in quackerytext:
        quackerytext = quackerytext.replace(f'{w} {w}', w)


quackerytext = rf'''

import js

async def ainput(prompt):
    term = js.term
    term.resume()
    print('\u200c', end='', flush=True) # &zwnj;
    result = await term.read(prompt)
    term.pause()
    return result

{quackerytext}'''

print('Loading', flush=True)
with open('quackery.py', 'w') as f: f.write(fixedquackerytext)

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