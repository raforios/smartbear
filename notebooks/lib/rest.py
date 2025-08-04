'''
    Rest functions
'''

# import json
import logging
import pandas as pd
import requests as req

logging.basicConfig(level=logging.INFO,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_data(url: str,
    headers: dict = None, primary: int = 0,
    field: str = 'data') -> pd.DataFrame:
    '''
        Get data from SmartBear API
    '''
    if headers is None:
        headers = {}
    try :
        response = req.request(
            'GET',
            url = url,
            headers = headers,
            timeout = 600
        )
        status_code = response.status_code
        logging.info(response.status_code)
        if status_code >= 300 or status_code < 200:
            logging.error('ERROR!')
        else:
            logging.info('SUCCESS!')
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent = 4, sort_keys = True))
        # data_str = json.dumps(data, indent = 4)
        # print(data_str)
        if primary == 0:
            return pd.json_normalize(data[field])
        if primary == 1:
            return pd.json_normalize(data)

        return data
    except req.exceptions.HTTPError as http_err:
        error_msg = f'Error - HTTP: {http_err}'
        logging.error(error_msg)
        error_msg = f'Response Text: {response.text}'
        logging.error(error_msg, exc_info = True)
        raise http_err
    except req.exceptions.ConnectionError as conn_err:
        error_msg = f'Error -  Connection: {conn_err}. Microservice Unavailable'
        logging.error(error_msg, exc_info = True)
        raise conn_err
    except Exception as error :
        error_msg = f'ERROR FROM get_data. This is why: {error}'
        logging.critical(error_msg, exc_info = True)
        raise error

def post_data(url: str, data: dict,
    headers: dict = None) -> dict:
    '''
        Post data into SmartBear API
    '''
    if headers is None:
        headers = {}
    try :
        response = req.post(
            url = url,
            json = data,
            headers = headers,
            timeout = 600
        )
        status_code = response.status_code
        logging.info(response.status_code)
        if status_code >= 300 or status_code < 200:
            logging.error('ERROR!')
        else:
            logging.info('SUCCESS!')
        response.raise_for_status()
        data = response.json()
        return data
    except req.exceptions.HTTPError as http_err:
        error_msg = f'Error - HTTP: {http_err}'
        logging.error(error_msg)
        error_msg = f'Response Text: {response.text}'
        logging.error(error_msg, exc_info = True)
        raise http_err
    except req.exceptions.ConnectionError as conn_err:
        error_msg = f'Error -  Connection: {conn_err}. Microservice Unavailable'
        logging.error(error_msg, exc_info = True)
        raise conn_err
    except Exception as error :
        error_msg = f'ERROR FROM get_data. This is why: {error}'
        logging.critical(error_msg, exc_info = True)
        raise error

def put_data(url: str, data: dict,
    headers: dict = None) -> dict:
    '''
        Put data into SmartBear API
    '''
    if headers is None:
        headers = {}
    try :
        response = req.put(
            url = url,
            data = data,
            headers = headers,
            timeout = 600
        )
        status_code = response.status_code
        logging.info(response.status_code)
        if status_code >= 300 or status_code < 200:
            logging.error('ERROR!')
        else:
            logging.info('SUCCESS!')
        response.raise_for_status()

        return {'message: ': 'Process succesfully!'} if response.text == '' else response.json()
    except req.exceptions.HTTPError as http_err:
        error_msg = f'Error - HTTP: {http_err}'
        logging.error(error_msg)
        error_msg = f'Response Text: {response.text}'
        logging.error(error_msg, exc_info = True)
        raise http_err
    except req.exceptions.ConnectionError as conn_err:
        error_msg = f'Error -  Connection: {conn_err}. Microservice Unavailable'
        logging.error(error_msg, exc_info = True)
        raise conn_err
    except Exception as error :
        error_msg = f'ERROR FROM get_data. This is why: {error}'
        logging.critical(error_msg, exc_info = True)
        raise error

def delete_data(url: str, data: dict,
    headers: dict = None) -> str:
    '''
        Delete data into SmartBear API
    '''
    if headers is None:
        headers = {}
    try :
        response = req.delete(
            url = url,
            json = data,
            headers = headers,
            timeout = 600
        )
        status_code = response.status_code
        logging.info(response.status_code)
        if status_code >= 300 or status_code < 200:
            logging.error('ERROR!')
        else:
            logging.info('SUCCESS!')
        response.raise_for_status()
        return response.json()
    except req.exceptions.HTTPError as http_err:
        error_msg = f'Error - HTTP: {http_err}'
        logging.error(error_msg)
        error_msg = f'Response Text: {response.text}'
        logging.error(error_msg, exc_info = True)
        raise http_err
    except req.exceptions.ConnectionError as conn_err:
        error_msg = f'Error -  Connection: {conn_err}. Microservice Unavailable'
        logging.error(error_msg, exc_info = True)
        raise conn_err
    except Exception as error :
        error_msg = f'ERROR FROM get_data. This is why: {error}'
        logging.critical(error_msg, exc_info = True)
        raise error
