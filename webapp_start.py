from pyodide.http import pyfetch
from os import mkdir
async def get(file):
    response = await pyfetch(f"${ORIGIN}/{file}")
    with open(file, "wb") as f:
        f.write(await response.bytes())

files1 = ['quackery.py', 'bigrat.qky', 'extensions.qky', 'turtleduck.qky']
for file in files1:
    # N. B. top-level await is only allowed in Pyodide
    await get(file)

mkdir('sundry')
files2 = ['cards.qky', 'demo.qky', 'fsm.qky', 'heapsort.qky']
for file in files2:
    await get(f'sundry/{file}')

from quackery import quackery

quackery(r'''
say "Welcome to Quackery running on the Pyodide virtual machine." cr

$ 'extensions.qky' dup name? not
dip sharefile and iff
    [ cr say 'Building extensions.' cr quackery ]
else drop

shell''')