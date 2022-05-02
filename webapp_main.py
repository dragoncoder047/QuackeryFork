from browser import bind, worker, window

jQuery = window.jQuery
q_worker = worker.Worker('worker')

def finished_input(text):
    worker.send(text)
    term.set_prompt('')
    term.disable()

term = jQuery('#terminal').terminal(finished_input, {'greetings': '', 'prompt': ''})

@bind(q_worker, "message")
def output(e):
    if e.data.type = 'print':
        term.echo(e.data.text, {'newline': False})
    else:
        term.enable()
        term.set_prompt(e.data.text)
        
