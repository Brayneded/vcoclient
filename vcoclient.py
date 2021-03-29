import requests
import os
from datetime import datetime, timedelta


class VcoClient:
    def __init__(self, orchestrator_url):
        self.headers = {
            'Authorization' : "Token " + os.environ['VCO301APIKEY'],
            'Content-Type' : 'application/json'
        }
        self.vco = orchestrator_url

        # wrapper method around requests.POST
    def request(self, method, body):
        try:
            resp = requests.post(self.vco + '/portal/rest/' + method, headers=self.headers, json=body)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return resp

        # Generates a timestamp in the right format for the VCO
    def make_orchestrator_timestamp(self, timestamp):
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.000Z')


        # Gets a list of enterprises managed by a partner
    def get_enterprise_proxy_enterprises(self):
        resp = self.request('enterpriseProxy/getEnterpriseProxyEnterprises', {})
        return resp.json()

        # Gets a list of edges within an enterprise and returns a dict
    def getEnterpriseEdges(self, enterpriseId):
        resp = self.request('enterprise/getEnterpriseEdges', {"enterpriseId" : enterpriseId})
        return resp.json()

        # collects TSD data for an edge
    def getEdgeLinkSeries(self, enterpriseId, edgeId, **kwargs):

        interval = {"start": kwargs.get("start", self.make_orchestrator_timestamp(datetime.utcnow() - timedelta(hours=12))),
                     "end": kwargs.get("end", self.make_orchestrator_timestamp(datetime.utcnow()))}

        body = {"edgeId" : edgeId, "interval" : interval}
        body['enterpriseId'] = enterpriseId if enterpriseId is not None else 0

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        resp = self.request('metrics/getEdgeLinkSeries', body)
        return resp.json()

        # Collects a list of identifiable apps from the VCO
    def getIdentifiableApplications(self, enterpriseId):
        resp = self.request('configuration/getIdentifiableApplications',
                            {"enterpriseId": enterpriseId})
        return resp.json()

            # Collects a list of identifiable apps from the VCO
    def getEdgeConfigurationStack(self, enterpriseId, edgeId):
        resp = self.request('configuration/getIdentifiableApplications',
                            {"enterpriseId": enterpriseId, "edgeId": edgeId})
        return resp.json()

        # Gets a list of application TSD

    def get_edge_app_series(self, enterpriseId, edgeId, **kwargs):
        # Define the interval that we're pulling stats for
        interval = {"start": kwargs.get("start",
                                        self.make_orchestrator_timestamp(
                                            datetime.utcnow() - timedelta(hours=12)
                                            )
                                        ),
                    "end": kwargs.get("end",
                                      self.make_orchestrator_timestamp(
                                          datetime.utcnow()
                                          )
                                      )
                    }
        # Create the HTTP Request Body
        body = {"edgeId" : edgeId, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}
        body['enterpriseId'] = enterpriseId if enterpriseId is not None else 0

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        if kwargs.get("applications") is not None:
            body['applications'] =kwargs['applications']

        resp = self.request('metrics/getEdgeAppSeries', body)
        return resp.json()


        # Gets a list of application metrics

    def get_edge_app_metrics(self,enterpriseId, edgeId, **kwargs):
        # Define the interval that we're pulling stats for
        interval = {"start": kwargs.get("start",
                                        self.make_orchestrator_timestamp(
                                            datetime.utcnow() - timedelta(hours=12)
                                            )
                                        ),
                    "end": kwargs.get("end",
                                      self.make_orchestrator_timestamp(
                                          datetime.utcnow()
                                          )
                                      )
                    }
        # Create the HTTP Request Body
        body = {"edgeId" : edgeId, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}
        body['enterpriseId'] = enterpriseId if enterpriseId is not None else 0

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        resp = self.request('metrics/getEdgeAppMetrics', body)
        return resp.json()


