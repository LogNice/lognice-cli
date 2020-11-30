import os
import requests

def create_session(filepath, url_base):
    return requests.post('%s/create' % url_base, files={
        'validator': open(filepath, 'rb')
    }).json()

def submit_solution(session_id, username, filepath, token, url_base):
    data = {'username': username}
    if token:
        data['token'] = token
    return requests.post('%s/submit/%s' % (url_base, session_id), data=data, files={
        'solution': open(filepath, 'rb')
    }).json()

def session_summary_raw(session_id, url_base):
    return requests.get('%s/summary/%s' % (url_base, session_id)).json()

def session_summary_table(session_id, url_base):
    return requests.get('%s/summary/table/%s' % (url_base, session_id)).json()

def session_summary_graph(session_id, url_base):
    url = '%s/summary/graph/%s' % (url_base, session_id)
    filename = '%s.png' % session_id
    open(filename, 'wb').write(requests.get(url).content)
    return filename
