// modified from the Pyodide console (https://pyodide.org/en/stable/console.html), since it already uses jQuery.terminal

const ORIGIN = 'https://dragoncoder047.github.io/QuackeryFork/'

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s));
}

window.addEventListener('DOMContentLoaded', async function main() {

    var term = $("#terminal").terminal(_ => { }, {
        greetings: '',
        prompt: '',
        completionEscape: false,
        pauseEvents: false
    });
    term.pause();
    window.term = term;
    try {
        globalThis.pyodide = await loadPyodide({
            homedir: '/home/quackery',
            stderr: line => term.error(line),
            stdout: line => term.echo(line, { newline: false }),
            stdin: async prompt => {
                term.resume();
                var input = await term.read(prompt);
                term.pause();
                await sleep(10);
                return input;
            },
        });


        pyodide._api.on_fatal = async (e) => {
            term.error("AAAAH!! You crashed Python! Please report this error:");
            term.exception(e);
            term.error("Look in the browser console for more details.");
            term.pause();
            await sleep(15);
            term.pause();
        };

        var resp = await fetch('webapp_start.py');
        var py = await resp.text();


        await pyodide.runPythonAsync(py.replaceAll('@@ORIGIN@@', ORIGIN));

        term.error('Reload the page to run Quackery again.');
    }
    catch (e) {
        term.clear();
        term.error('An error occurred loading Quackery:')
        term.exception(e);
        term.error('Please report this error if it continues to occur.');
        term.error('https://github.com/dragoncoder047/QuackeryFork/issues');
    }
});
