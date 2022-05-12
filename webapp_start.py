# @@ORIGIN@@ will be replaced in Javascript

from pyodide.http import pyfetch
from os import mkdir
import ast
import js
from itertools import count

mkdir('sundry')
files = ['bigrat', 'extensions', 'turtleduck', 'sundry/cards', 'sundry/demo', 'sundry/fsm', 'sundry/heapsort']

for file in files:
    # N. B. top-level await is only allowed in Pyodide
    resp = await pyfetch(f'@@ORIGIN@@/{file}.qky')
    print(f'Downloading {file}.qky', flush=True)
    text = await resp.string()
    with open(f'{file}.qky', 'w') as f: f.write(text)

print('Downloading quackery.py', flush=True)
resp = await pyfetch('@@ORIGIN@@/quackery.py')
print('Started download', flush=True)
quackerytext = await resp.string()

# PATCH - make functions async

def has_await(node):
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Await): return True
    return False

def get_name(node):
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    elif isinstance(func, ast.Name):
        return func.id
    else:
        return None

class FixFirst(ast.NodeTransformer):
    def visit_Call(self, node):
        name = get_name(node)
        if name is None:
            return node
        if name == 'input' or name == 'current_item':
            print('\tAwaiting function', name)
            if name == 'input':
                print('\tRenaming input')
                node.func.id = 'async_patched_input'
            return ast.Await(
                value=node,
                lineno=node.lineno,
                col_offset=node.col_offset,
                end_lineno=node.end_lineno,
                end_col_offset=node.end_col_offset + 6
            )
        else:
            return node

changed = False
asynced_functions = ['async_patched_input', 'current_item']
class MakeFunctionAsyncValid(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        global changed, asynced_functions
        name = node.name
        if has_await(node):
            print('\tFound bad function', name, '> fixing')
            return ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                lineno=node.lineno,
                col_offset=node.col_offset,
                end_lineno=node.end_lineno,
                end_col_offset=node.end_col_offset
            )
            asynced_functions.append(name)
            changed = True
        else:
            return node

class ApplyAwaitsToAsyncedFunctions(ast.NodeTransformer):
    def visit_Call(self, node):
        name = get_name(node)
        if name is None:
            return node
        if node in asynced_functions:
            print('\tNow awaiting call of', name)
            return ast.Await(
                value=node,
                lineno=node.lineno,
                col_offset=node.col_offset,
                end_lineno=node.end_lineno,
                end_col_offset=node.end_col_offset + 6
            )
        else:
            return node

print('Parsing', flush=True)
tree = ast.parse(quackerytext)

print('Patching', flush=True)
fixed_tree = FixFirst().visit(tree)

a = MakeFunctionAsyncValid()
b = ApplyAwaitsToAsyncedFunctions()

for it in count(1):
    print('Fixing, iteration', it, flush=True)
    changed = False
    fixed_tree = b.visit(a.visit(fixed_tree))
    if changed is False:
        break

print('Unparsing', flush=True)
fixedquackerytext = f'''

import js

async def async_patched_input(prompt):
    term = js.term
    term.resume()
    print('\\u200c', end='', flush=True) # &zwnj;
    result = await term.read(prompt)
    term.pause()
    return result

{ast.unparse(fixed_tree)}'''

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
      Welcome to Quackery running on the Pyodide virtual machine.

''')
await quackery(r'''

$ 'extensions.qky' dup name? not
dip sharefile and iff
    [ cr say 'Building extensions...' cr quackery ]
else drop

shell

''')