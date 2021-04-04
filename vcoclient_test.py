import pytest
import os
from datetime import datetime

from .vcoclient import VcoClient

APIKEY = 'abcd'
AUTHTOKEN = f'Token {APIKEY}'
ORCHESTRATOR = 'https://localhost'
HEADERS = {
        'Authorization' : AUTHTOKEN,
        'Content-Type' : 'application/json'
    }

TIMESTAMP = datetime(2021, 4, 4, 12, 0, 30)

def test_vcoclient_init_env():
    """
    Testing initializing a VcoClient using environmental variables
    """
    os.environ['VCOAPIKEY'] = APIKEY
    client = VcoClient(orchestrator_url=ORCHESTRATOR)

    assert client.vco == ORCHESTRATOR
    assert client.headers == HEADERS


def test_vcoclient_init_arg():
    """
    Testing initializing a VcoClient using parameter
    """
    if os.getenv('VCOAPIKEY'): # pragma: no cover
        del os.environ['VCOAPIKEY']
    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    assert client.vco == ORCHESTRATOR
    assert client.headers == HEADERS

def test_vcoclient_init_missing_key():
    """
    Testing that raising a VcoClient without an api_key raises an exception
    """
    if os.getenv('VCOAPIKEY'): # pragma: no cover
        del os.environ['VCOAPIKEY']
    with pytest.raises(ValueError):
        VcoClient(orchestrator_url=ORCHESTRATOR)

def test_make_orchestrator_timestamp():
    """
    Testing generating an orchstrator friendly timestamp
    """
    date_str = '2021-04-04T12:00:30.000Z'
    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.make_orchestrator_timestamp(TIMESTAMP)

    assert date_str == resp


