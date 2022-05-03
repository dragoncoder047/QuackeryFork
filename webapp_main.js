// modified from the Pyodide console (https://pyodide.org/en/stable/console.html), since it already uses jQuery.terminal

const ORIGIN = 'https://dragoncoder047.github.io/QuackeryFork'

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s));
}

window.addEventListener('DOMContentLoaded', async function main() {

    var stdin_queue = [];
    var term = $("#terminal").terminal(input => {
        var lines = input.split('\n');
        lines.forEach(line => stdin_queue.push(line));
    }, {
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
            stdout: line => term.echo(line),
            stdin: prompt => {
                term.resume();
                term.set_prompt(prompt);
                var line;
                while ((line = stdin_queue.splice(1, 1)[0]) === undefined) /*noop*/;
                term.pause();
                return line;
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
        term.error('A fatal error occurred while loading Quackery.')
        term.error('Please report this error if it continues to occur.');
        term.error('https://github.com/dragoncoder047/QuackeryFork/issues');
        term.echo();
        term.exception(e);
        term.pause();
    }
});
