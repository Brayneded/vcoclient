import requests
import os
from datetime import datetime, timedelta


class VcoClient:
    """
    A class that provides a client for interacting with the Velocloud orchestrator_url

    ...

    Attributes:
    -----------
    orchestrator_url : str
        URL of the velocloud orchestrator

    """
    def __init__(self, orchestrator_url: str, **kwargs):
        api_key = kwargs.get('api_key', os.getenv('VCOAPIKEY'))

        if api_key is None:
            raise ValueError('api_key is required. Either pass it in as an argument'\
                             ' or use the VCOAPIKEY environmental variable')

        self.headers = {
            'Authorization' : f"Token {api_key}",
            'Content-Type' : 'application/json'
        }
        self.vco = orchestrator_url

    def request(self, method: str, body: dict) -> requests.Response:
        """
        Wraps around requests.post()
        """
        try:
            resp = requests.post(f'{self.vco}/portal/rest/{method}',
                                 headers=self.headers,
                                 json=body)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return resp


    @staticmethod
    def make_orchestrator_timestamp(timestamp: datetime) -> str:
        """
        Returns a timestamp in a format that the Velocloud Orchestrator will accept

            Parameters:
                timestamp (datetime): A datetime object

            Returns:
                (str): A formatted timestamp string
        """
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.000Z')


    def get_enterprise_proxy_enterprises(self) -> list:
        """
        Returns a list of Enterprises associated with an EnterpriseProxy (MSP/Partner)

        Returns:
            (list) : A list of Enterprise dicts
        """
        resp = self.request('enterpriseProxy/getEnterpriseProxyEnterprises', {})
        return resp.json()

    # Gets a list of edges within an enterprise and returns a list
    def get_enterprise_edges(self, enterprise_id: int = 0) -> list:
        body = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}

        resp = self.request('enterprise/getEnterpriseEdges', body)
        return resp.json()

    # collects TSD data for an edge
    def get_edge_link_series(self, enterprise_id: int, edge_id: int, **kwargs) -> list:
        """
        Returns a python object containing the link series data for an edge during a given interval

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise
            edge_id (int): The velocloud ID for an edge
            metrics (dict): A dictionary containing a list of metrics to return from the orchestrator.
                            Default behaviour is  to return all metrics
            start (datetime): The start time for the time series data  interval
            end (datetime): The end time for the time series data  interval

        Returns:
            json (object): A python object representing the JSON response
        """
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

        body = {"edgeId" : edge_id, "interval" : interval}
        if enterprise_id != 0:
            body['enterpriseId'] = enterprise_id

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        resp = self.request('metrics/getEdgeLinkSeries', body)
        return resp.json()

    # Collects a list of identifiable apps from the VCO
    def get_identifiable_applications(self, enterprise_id: int) -> list:
        resp = self.request('configuration/getIdentifiableApplications',
                            {"enterpriseId": enterprise_id})
        return resp.json()

            # Collects a list of identifiable apps from the VCO
    def get_edge_configuration_stack(self, enterprise_id: int, edge_id: int) -> list:
        resp = self.request('configuration/getIdentifiableApplications',
                            {"enterpriseId": enterprise_id, "edgeId": edge_id})
        return resp.json()

        # Gets a list of application TSD

    def get_edge_app_series(self, enterprise_id: int, edge_id: int, **kwargs) -> list:
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
        body = {"edgeId" : edge_id, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}
        if enterprise_id != 0:
            body['enterpriseId'] = enterprise_id

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        if kwargs.get("applications") is not None:
            body['applications'] = kwargs['applications']

        resp = self.request('metrics/getEdgeAppSeries', body)
        return resp.json()


    # Gets a list of application metrics
    def get_edge_app_metrics(self, enterprise_id: int, edge_id: int, **kwargs) -> list:
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
        body = {"edgeId" : edge_id, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}
        if enterprise_id != 0:
            body['enterpriseId'] = enterprise_id

        if kwargs.get("metrics") is not None:
            body['metrics'] = kwargs['metrics']

        resp = self.request('metrics/getEdgeAppMetrics', body)
        return resp.json()

        # Get a list of link metrics

    def get_link_quality_events(self,  edgeId, enterpriseId, **kwargs):
        pass

