// modified from the Pyodide console (https://pyodide.org/en/stable/console.html), since it already uses jQuery.terminal

const ORIGIN = 'https://dragoncoder047.github.io/QuackeryFork'

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s));
}

window.addEventListener('DOMContentLoaded', async function main() {


    var term = $("#terminal").terminal(() => {}, {
        greetings: '',
        prompt: '',
        completionEscape: false,
        pauseEvents: false
    });
    term.pause();
    window.term = term;
    await sleep(500);
    term.echo('Quackery (and Python) are loading...');
    var c = setTimeout(() => term.echo('this may take a while...'), 5000);
    try {
        globalThis.pyodide = await loadPyodide({
            homedir: '/quackery',
            stderr: line => { clearTimeout(c); term.error(line) },
            stdout: line => { clearTimeout(c); term.echo(line) },
            stdin: window.prompt,
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
        term.echo();
        term.echo('Until this problem is resolved, to run Quackery you can go to');
        term.echo('https://www.pythonanywhere.com/embedded3/ and paste in this code:')
        term.echo();
        term.echo('from requests import get');
        term.echo('def load(url):');
        term.echo('    c = compile(get(url).text, url, \'exec\')');
        term.echo('    exec(c, globals(), globals())');
        term.echo('load(\'https://raw.githubusercontent.com/GordonCharlton/Quackery/main/quackery.py\')');
        term.echo();
        term.pause();
        throw e;
    }
});
