import os
import click
import socketio
from colored import fg, attr, stylize
from api import (
    create_session,
    submit_solution,
    session_summary_raw,
    session_summary_table,
    session_summary_graph
)

BASE_URL = None
STYLES = {
    'success': fg(10) + attr(1),
    'important': fg(220) + attr(1),
    'progress': fg(214),
    'info': fg(87),
    'error': fg(9),
    'normal': ''
}

def log(s, style='success', end='\n'):
    print(stylize(s, STYLES[style]), end=end)

@click.group()
@click.option('-b', '--base-url', help='Server base url.', default='http://localhost:5000', type=str)
def cli(base_url):
    '''Log(N)ice CLI tool!'''
    global BASE_URL
    BASE_URL = base_url
    pass

@cli.command()
@click.option('-f', '--filepath', help='Validator (test cases) filepath.', required=True, type=str)
def create(filepath):
    '''Create a new session.'''
    if not os.path.exists(filepath):
        log('File does not exist.', 'error')
        return

    r = create_session(filepath, BASE_URL)
    if r['status'] == 'error':
        log(r['message'], 'error')
        return

    log('Session id:', end=' ')
    log(r['result']['session_id'], 'important')

@cli.command()
@click.option('-s', '--session-id', help='Session id you are submitting to.', required=True, type=str)
@click.option('-u', '--username', help='Your username, must be unique.', required=True, type=str)
@click.option('-f', '--filepath', help='Validator (test cases) filepath.', required=True, type=str)
@click.option('-t', '--token', help='Token from previous submission.', required=False, type=str)
def submit(session_id, username, filepath, token=None):
    '''Submit a solution to a session.'''
    sio = socketio.Client()

    def disconnect():
        sio.emit('unregister', {
            'session_id': session_id,
            'username': username
        })
        sio.disconnect()

    @sio.event
    def connect():
        log('Connection with server established.')
        log('Registering...', 'progress')
        sio.emit('register', {
            'session_id': session_id,
            'username': username
        })

    @sio.on('register')
    def on_registered(is_registered):
        if not is_registered:
            disconnect()
            return

        log('Submitting...', 'progress')
        r = submit_solution(session_id, username, filepath, token, BASE_URL)
        if r['status'] == 'error':
            log(r['message'], 'error')
            disconnect()
            return

        if 'token' in r['result']:
            log('Use that token for next submissions in this session:', end=' ')
            log(r['result']['token'], 'important')
        log('Waiting for evaluation...', 'progress')

    @sio.on('task_finished')
    def on_evaluated(data):
        blocker = data['blocker']
        if blocker:
            log('You didn\'t pass the following test case:', 'error')
            log('Input: %s' % ', '.join(['%s=%s' % (k, str(v)) for k, v in blocker['input'].items()]), 'info')
            log('Expected output: %s' % blocker['expected'], 'info')
            log('Your output: %s' % blocker['output'], 'info')
        else:
            log('You passed all', end=' ')
            log(data['passed'], 'important', ' ')
            log('test cases!')
            log('CPU Time in %s:' % data['time']['unit'], 'normal', ' ')
            log(data['time']['value'], 'important')
        disconnect()

    if not os.path.exists(filepath):
        log('File does not exist.', 'error')
        return

    sio.connect(BASE_URL)

@cli.command()
@click.option('-s', '--session-id', help='Session id for which you want a summary.', required=True, type=str)
def summary(session_id):
    '''Returns submission results for a given session id.'''
    r = session_summary_table(session_id, BASE_URL)
    if r['status'] == 'error':
        log(r['message'], 'error')
        return

    print(r['result'])

@cli.command()
@click.option('-s', '--session-id', help='Session id for which you want a graph summary.', required=True, type=str)
def graph(session_id):
    '''Download a graph summary for a given session id.'''
    filename = session_summary_graph(session_id, BASE_URL)
    print('Image saved in %s' % filename)

if __name__ == '__main__':
    cli()
