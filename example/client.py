#!/usr/bin/env python3
'''
    Demo client for perx-testcase application

'''
import os
import requests
import json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR,'.token')
TOKEN_LENGTH = 40

TESTDIR = os.path.join(BASE_DIR, '..', 'tests/testdata')
DATADIR = os.path.join(BASE_DIR, '..', 'data')

def read_token(token_filename):
    try:
        with open(token_filename, 'r') as fi:
            token = fi.readline()
            token = token.strip('\n')
    except IOError:
        return None

    if len(token) != TOKEN_LENGTH:
        return None

    return token


def list_xlsx(docs_dir):
    for (_, _, filenames) in os.walk(docs_dir): 
        for filename in filenames:
            if filename.endswith('.xlsx'):
                yield filename


UPLOAD_URL = 'http://localhost:8000/api/upload/{}'
STATUS_URL = 'http://localhost:8000/api/status/{}'

def main():
    token = read_token(TOKEN_FILE)
    if not token:
        print(f'Put your token to {TOKEN_FILE}, see README.md for details')
        exit(0)

    headers = {
        'Authorization': f'Token {token}',
    }

    uuids = list()
    target_dir = TESTDIR

    # upload
    for docname in list_xlsx(target_dir):
        url = UPLOAD_URL.format(docname)
        response = requests.put(url, 
                data=open(os.path.join(target_dir, docname), 'rb'),
                headers=headers)
        if response.status_code != 200:
            print(docname, response.text, response.status_code)
            continue

        answer = json.loads(response.text)
        if answer['error'].lower() != 'ok':
            print(docname, answer)
            continue
        
        uuid = answer[docname]
        uuids.append(uuid)

    # check
    DELAY = 0.2
    while uuids:
        for uuid in uuids:
            status_url = STATUS_URL.format(uuid)
            response = requests.get(status_url, headers=headers)
            answer = json.loads(response.text)
            if answer['error'].lower() == 'ok':
                if answer['status'].lower() == 'finished':
                    print(uuid, answer['result'], answer['finished_at'])
                    uuids.remove(uuid)
                else:
                    print(uuid, answer['status'])
            else:
                print(uuid, answer['error'])
        time.sleep(DELAY)
    

if __name__ == '__main__':
    main()


