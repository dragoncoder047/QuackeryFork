// modified from the Pyodide console (https://pyodide.org/en/stable/console.html), since it already uses jQuery.terminal

const ORIGIN = 'https://dragoncoder047.github.io/QuackeryFork/'

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s));
}

window.addEventListener('DOMContentLoaded', async function main() {

    var inputDone;
    var term = $("#terminal").terminal(inputDone, {
        greetings: '',
        prompt: '',
        completionEscape: false,
        pauseEvents: false,
        completion: function (command, callback) {
            callback(pyconsole.complete(command).toJs()[0]);
        },
    });
    term.pause();
    window.term = term;

    globalThis.pyodide = await loadPyodide({
        homedir: '/home/quackery',
        stderr: line => term.error(line),
        stdout: line => term.echo(line),
        stdin: async prompt => {
            term.set_prompt(prompt);
            term.resume();
            var input = await new Promise(resolve => (inputDone = resolve));
            term.pause();
            await sleep(10);
            return input;
        },
    });


    pyodide._api.on_fatal = async (e) => {
        term.error("AAAAH!! You crashed Python! Please report this error:");
        term.error(e);
        term.error("Look in the browser console for more details.");
        term.pause();
        await sleep(15);
        term.pause();
    };

    var old_open = pyodide.globals.get('open');
    pyodide.globals.set('open', function fetch_opener(filename, mode) {
        throw 'fixme';
    });

    await pyodide.runPythonAsync(`
        from pyodide.http import pyfetch
        response = await pyfetch("${ORIGIN}/quackery.py")
        with open("quackery.py", "wb") as quackeryfile:
            quackeryfile.write(await response.bytes())

        from quackery import quackery
        quackery('''
        say "Welcome to Quackery running on the Pyodide virtual machine."
        shell
        ''')
    `)
});
