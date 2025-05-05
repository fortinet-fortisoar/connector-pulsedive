"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import requests
from connectors.core.connector import Connector, get_logger, ConnectorError

error_msg = {
    401: 'Authentication failed due to invalid credentials',
    429: 'Rate limit was exceeded',
    403: 'Token is invalid or expired',
    "ssl_error": 'SSL certificate validation failed',
    'time_out': 'The request timed out while trying to connect to the remote server',
}

logger = get_logger("pulsedive")


def make_request(config, endpoint=None, params=None, data=None, method='GET', headers=None, json_data=None):
    server_url = config.get('server_url', '').strip().strip('/')
    if not server_url.startswith('http') or not server_url.startswith('https'):
        server_url = 'https://' + server_url
    api_key = config.get("api_key")
    verify_ssl = config.get("verify_ssl")

    try:
        headers = {"Content-Type": "application/json"}
        url = server_url + endpoint
        logger.info(f"Making {method} request to URL: {url}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Params: {params}")
        logger.info(f"Data: {data}")
        logger.info(f"JSON Data: {json_data}")
        params.update({'key': '{0}'.format(api_key)})
        response = requests.request(method=method, url=url,
                                    headers=headers, data=data, json=json_data, params=params,
                                    verify=verify_ssl)
        if response.ok:
            if 'json' in str(response.headers):
                return response.json()
            else:
                return response.text
        else:
            logger.error("Error: {0}".format(response.json()))
            raise ConnectorError('{0}'.format(error_msg.get(response.status_code, response.text)))
    except requests.exceptions.SSLError as e:
        logger.exception('{0}'.format(e))
        raise ConnectorError('{0}'.format(error_msg.get('ssl_error')))
    except requests.exceptions.ConnectionError as e:
        logger.exception('{0}'.format(e))
        raise ConnectorError('{0}'.format(error_msg.get('time_out')))
    except Exception as e:
        logger.error('{0}'.format(e))
        raise ConnectorError('{0}'.format(e))


def _check_health(config):
    try:
        endpoint = "/api/info.php"
        params = {"indicator": "google.com"}
        response = make_request(config, endpoint=endpoint, params=params)
        if response:
            return True
    except Exception as e:
        raise Exception(e)


def get_domain_reputation(config: dict, params: dict):
    try:
        endpoint = "/api/info.php"  # edit endpoint
        response = make_request(config, endpoint=endpoint, params=params)
        return response
    except Exception as e:
        raise Exception(e)


def get_ip_reputation(config: dict, params: dict):
    try:
        endpoint = "/api/info.php"  # edit endpoint
        response = make_request(config, endpoint=endpoint, params=params)
        return response
    except Exception as e:
        raise Exception(e)


def get_links_of_indicator(config: dict, params: dict):
    try:
        endpoint = "/api/info.php"  # edit endpoint
        params.update({'get': 'link'})
        response = make_request(config, endpoint=endpoint, params=params)
        return response
    except Exception as e:
        raise Exception(e)


operations = {
    "get_ip_reputation": get_ip_reputation,
    "get_links_of_indicator": get_links_of_indicator,
    "get_domain_reputation": get_domain_reputation,
}
