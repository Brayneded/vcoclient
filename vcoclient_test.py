import pytest
import os
import requests
from requests.exceptions import HTTPError
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

def test_request_success(requests_mock):
    """
    Testing sucessful HTTP Request
    """
    test_body = {"test" : "test"}
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/test',
                       json=test_body
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.request(method='test', body=test_body)

    assert resp.json() == test_body

def test_request_absent(requests_mock):
    """
    Testing 404 HTTP response
    """
    test_body = {"test" : "test"}
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/test',
                       status_code=404
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.request(method='test', body=test_body)

    assert resp is None


def test_request_error(requests_mock):
    """
    Testing 500 HTTP response
    """
    test_body = {"test" : "test"}
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/test',
                       status_code=503
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    with pytest.raises(HTTPError):
        client.request(method='test', body=test_body)

def test_get_enterprise_proxy_enterprises_success(requests_mock):
    """
    Testing successful HTTP response to get_enterprise_proxy_enterprises
    """
    test_body = {"test" : "test"}
    test_response = [{"enterpriseId" : 1}, {"enterpriseId" : 2}]
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/enterpriseProxy/getEnterpriseProxyEnterprises',
                        json=test_response
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.get_enterprise_proxy_enterprises()

    assert resp == test_response

def test_get_enterprise_proxy_enterprises_absent(requests_mock):
    """
    Testing 404 HTTP response to get_enterprise_proxy_enterprises
    """

    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/enterpriseProxy/getEnterpriseProxyEnterprises',
                       status_code=404
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.get_enterprise_proxy_enterprises()

    assert resp is None

def test_get_enterprise_edges_success_partner(requests_mock):
    """
    Testing successful HTTP response to get_enterprise_proxy_enterprises
    """

    test_response = [{"edgeId" : 1}, {"edgeId" : 2}]
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/enterprise/getEnterpriseEdges',
                       json=test_response
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.get_enterprise_edges(enterprise_id = 1)

    assert resp == test_response

def test_get_enterprise_edges_success_enterprise(requests_mock):
    """
    Testing successful HTTP response to get_enterprise_edges
    """

    test_response = [{"edgeId" : 1}, {"edgeId" : 2}]
    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/enterprise/getEnterpriseEdges',
                       json=test_response
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.get_enterprise_edges()

    assert resp == test_response

def test_get_enterprise_edges_absent(requests_mock):
    """
    Testing 404 HTTP response to get_enterprise_edges
    """

    requests_mock.post(f'{ORCHESTRATOR}/portal/rest/enterprise/getEnterpriseEdges',
                       status_code=404
                       )

    client = VcoClient(orchestrator_url=ORCHESTRATOR, api_key=APIKEY)

    resp = client.get_enterprise_edges(enterprise_id = 1)

    assert resp is None
