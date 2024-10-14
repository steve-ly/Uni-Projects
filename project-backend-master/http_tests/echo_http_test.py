import pytest
import requests
import json
from src import config

def test_echo():
    '''
    A simple test to check echo
    '''
    try:
        resp = requests.get(config.url + 'echo', params={'data': 'hello'})
    except requests.exceptions.ConnectionError:
        raise Exception("Server is configured badly on local machine") from None
    assert json.loads(resp.text) == {'data': 'hello'}
