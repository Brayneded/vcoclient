import requests
import os
import logging
import uuid
from datetime import datetime, timedelta
from requests.exceptions import HTTPError

log = logging.getLogger(__name__)

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
        request_id = uuid.uuid4()
        log.info(f'request_id: {request_id} - making POST request to '\
                 f'{self.vco}/portal/rest/{method}'
                 )
        try:
            resp = requests.post(f'{self.vco}/portal/rest/{method}',
                                 headers=self.headers,
                                 json=body)
            resp.raise_for_status()
        except HTTPError as err:
            log.error(f'request_id: {request_id} - {err}')

            # If it's just a 404 return None
            if resp.status_code == 404:
                return None

            raise err
        return resp


    @staticmethod
    def _make_orchestrator_timestamp(timestamp: datetime) -> str:
        """
        Returns a timestamp in a format that the Velocloud Orchestrator will accept

            Parameters:
                timestamp (datetime): A datetime object

            Returns:
                (str): A formatted timestamp string
        """
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    @classmethod
    def _make_interval(cls, start: datetime, end: datetime) -> dict:
        """
        Returns a dict containing an interval which is required for a number of metrics
        """
        start_str = cls._make_orchestrator_timestamp(start)
        end_str = cls._make_orchestrator_timestamp(end)

        return {"start" : start_str, "end" : end_str}

    def get_enterprise_proxy_enterprises(self) -> list:
        """
        Returns a list of Enterprises associated with an EnterpriseProxy (MSP/Partner)

        Returns:
            (list) : A list of Enterprise dicts
        """
        resp = self.request('enterpriseProxy/getEnterpriseProxyEnterprises', {})
        return resp.json() if resp is not None else None

    def get_enterprise_edges(self, enterprise_id: int = 0) -> list:
        """
        Returns a list of Edges associated with an Enterprise (End user)

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise

        Returns:
            (list) : A list of Enterprise dicts
        """
        body = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}

        resp = self.request('enterprise/getEnterpriseEdges', body)
        return resp.json() if resp is not None else None

    def get_edge_link_series(self,
                             edge_id: int,
                             start: datetime,
                             end: datetime,
                             enterprise_id: int = 0,
                             **kwargs) -> list:
        """
        Returns a python object containing the link time series data for an edge
        during a given interval

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise
            edge_id (int): The velocloud ID for an edge
            metrics (dict): A dictionary containing a list of metrics to return
                            from the orchestrator. Default behaviour is  to return
                            all metrics
            start (datetime): The start time for the time series data  interval
            end (datetime): The end time for the time series data  interval

        Returns:
            json (list): A python object representing the JSON response
        """
        interval = self._make_interval(start=start, end=end)


        body = {"edgeId" : edge_id, "interval" : interval}
        enterprise = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}
        metrics = kwargs.get("metrics", {})

        body.update(enterprise)
        body.update(metrics)

        resp = self.request('metrics/getEdgeLinkSeries', body)
        return resp.json() if resp is not None else None

    def get_identifiable_applications(self, enterprise_id: int = 0) -> list:
        """
        Returns a list of identifiable applications associated with an Enterprise (End user)

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise

        Returns:
            (list) : A list of application dicts
        """

        body = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}
        resp = self.request('configuration/getIdentifiableApplications',
                            body
                            )
        return resp.json() if resp is not None else None


    def get_edge_configuration_stack(self, edge_id: int, enterprise_id: int = 0) -> list:
        """
        Returns a list of configurations associated with an Edges

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise
            edge_id (int): The velocloud ID for an edge

        Returns:
            (list) : A list of configuration dicts
        """
        body = {"edgeId": edge_id}

        enterprise = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}

        body.update(enterprise)

        resp = self.request('configuration/getIdentifiableApplications',
                            body
                            )

        return resp.json() if resp is not None else None


    def get_edge_app_series(self,
                            enterprise_id: int,
                            edge_id: int,
                            start: datetime,
                            end: datetime,
                            **kwargs) -> list:
        """
        Returns a python object containing the application time series data for
        from an edge during a given interval

        Parameters:
            enterprise_id (int): The velocloud ID for an enterprise
            edge_id (int): The velocloud ID for an edge
            metrics (dict): A dictionary containing a list of metrics to return
                            from the orchestrator. Default behaviour is  to return
                            all metrics
            start (datetime): The start time for the time series data  interval
            end (datetime): The end time for the time series data  interval

        Returns:
            json (list): A python object representing the JSON response
        """
        interval = self._make_interval(start=start, end=end)

        body = {"edgeId" : edge_id, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}

        enterprise = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}
        metrics = kwargs.get("metrics", {})
        apps = kwargs.get("applications", {})

        body.update(enterprise)
        body.update(metrics)
        body.update(apps)

        resp = self.request('metrics/getEdgeAppSeries', body)
        return resp.json() if resp is not None else None


    # Gets a list of application metrics
    def get_edge_app_metrics(self,
                             enterprise_id: int,
                             edge_id: int,
                             start: datetime,
                             end: datetime,
                             **kwargs) -> list:
        # Define the interval that we're pulling stats for
        interval = self._make_interval(start=start, end=end)

        # Create the HTTP Request Body
        body = {"edgeId" : edge_id, "interval" : interval,
                "resolveApplicationNames": True, "limit" : -1}

        enterprise = {} if enterprise_id == 0 else {"enterpriseId" : enterprise_id}
        metrics = kwargs.get("metrics", {})

        body.update(enterprise)
        body.update(metrics)

        resp = self.request('metrics/getEdgeAppMetrics', body)
        return resp.json() if resp is not None else None

        # Get a list of link metrics

    def get_link_quality_events(self, edge_id: int, enterprise_id: int = 0, **kwargs):
        pass

