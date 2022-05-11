# @@ORIGIN@@ will be replaced in Javascript

from pyodide.http import pyfetch
from os import mkdir
import ast
import js

mkdir('sundry')
files = ['bigrat', 'extensions', 'turtleduck', 'sundry/cards', 'sundry/demo', 'sundry/fsm', 'sundry/heapsort']

for file in files:
    # N. B. top-level await is only allowed in Pyodide
    resp = await pyfetch(f'@@ORIGIN@@/{file}.qky')
    print(f'Downloading {file}.qky ...')
    text = await resp.string()
    with open(f'{file}.qky', 'w') as f: f.write(text)

resp = await pyfetch('@@ORIGIN@@/quackery.py')
quackerytext = await resp.string()

# PATCH - make functions async

def has_await(node):
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Await): return True
    return False

class FixFirst(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            name = node.func.id
        if name == 'input' or name == 'current_item':
            print('\tAwaiting function', name)
            if name == 'input':
                print('\tRenaming input')
                node.func.id = 'async_patched_input'
            return ast.Await(node)

changed = False
asynced_functions = ['async_patched_input', 'current_item']
class MakeFunctionAsyncValid(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        name = node.func.id
        if has_await(node):
            print('\tFound bad function', name, '> fixing')
            return ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list
            )
            asynced_functions.append(name)
            changed = True
        else:
            return node

class ApplyAwaitsToAsyncedFunctions(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            name = node.func.id
        if node in asynced_functions:
            print('\tNow awaiting call of', name)
            return ast.Await(node)
        else:
            return node

tree = ast.parse(quackerytext)

fixed_tree = FixFirst().visit(tree)

a = MakeFunctionAsyncValid()
b = ApplyAwaitsToAsyncedFunctions()

while True:
    changed = False
    fixed_tree = b.visit(a.visit(fixed_tree))
    if changed is False:
        break

fixedquackerytext = f'''

import js

async def async_patched_input(prompt):
    term = js.term
    term.resume()
    result = await term.read(prompt)
    term.pause()
    return result

{ast.unparse(fixed_tree)}'''

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
      Welcome to Quackery running on the Pyodide virtual machine.

''')
await quackery(r'''

$ 'extensions.qky' dup name? not
dip sharefile and iff
    [ cr say 'Building extensions...' cr quackery ]
else drop

shell

''')