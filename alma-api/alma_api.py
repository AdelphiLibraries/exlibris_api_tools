import json
import requests
import os
from configparser import ConfigParser
from pprint import pprint
import csv
# import time

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)

CONFIG_PATH = os.path.join(MY_PATH, "config.ini")
config = ConfigParser()
config.read(CONFIG_PATH)

BASE_URL = config["URLS"]["alma"]

# Select which key to use. You can have multiple in the config file, e.g., sandbox, production, etc.
API_KEY_DEV = config["KEYS"]["almaDev"]
API_KEY = config["KEYS"]["alma"]

OUTPUT_DIR = config["PATHS"]["outputDir"]
OUTPUT_PATH = config["PATHS"]["outPath"]

PER_PAGE = int(config["DEFAULTS"]["perPage"])  # max 100
# DATE_FROM = config["DEFAULTS"]["dateFrom"]  # earliest date to harvest


# Set MODE = "DEV" to use the Dev API key for operations
MODE = "PROD"


DEFAULT_PARAMS = {
    'apikey': API_KEY_DEV if MODE == "DEV" else API_KEY,
}


def main():

    # Test code here
    quit()


def get_users():
    # TODO: document this
    # Warning: this can be very large!
    return iterate_response("users", "user")["user"]


def get_user_details(uid):
    # TODO: document this
    return get_data(BASE_URL, f"users/{str(uid)}", DEFAULT_PARAMS)


def get_po_lines():
    # TODO: document this
    return iterate_response("acq/po-lines", "po_line")["po_line"]


def iterate_response(endpoint, key, base_url=BASE_URL, params=DEFAULT_PARAMS):
    # sourcery skip: use-fstring-for-concatenation
    api_key = API_KEY_DEV if MODE == "DEV" else API_KEY
    cursor = 0
    params['offset'] = cursor
    params['apikey'] = api_key

    record_cnt = get_record_count(base_url, endpoint, params)
    print(f"Found {str(record_cnt)} records.")
    out_records = []

    while cursor <= record_cnt:
        params['offset'] = cursor
        params['limit'] = PER_PAGE

        upper_bound = record_cnt if (
            cursor + PER_PAGE) >= record_cnt else cursor + PER_PAGE
        print(
            (
                (f"*** Getting records {str(cursor + 1)}" + " to ")
                + str(upper_bound)
                + " ..."
            )
        )
        newdata = get_data(base_url,  endpoint, params)[key]
        out_records += newdata
        cursor += PER_PAGE

    return {"total_record_count": record_cnt,
            key: out_records}


def get_data(base_url, endpoint, params):
    """General API GET function

    Args:
        base_url (str): Base url
        endpoint (str): Endpoint name
        params (dict): Request params

    Returns:
        dict: JSON representation
    """
    params['format'] = 'json'
    url = base_url + endpoint
    try:
        print("*** GET_DATA *************")
        print(f'*** Request URL: {url}')
        print("Params:")
        print(params)
        print("***")
        r = requests.get(url, params=params)
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:
        print('*** ERROR: could not connect to API. Check configuration. ' + str(e))
        print(f'URL: {url}')
        exit()
    except json.decoder.JSONDecodeError as e:
        print('*** ERROR: JSON response was not as expected. ' + str(e))
        print(f'URL: {url}')
        exit()


def get_record_count(base_url, endpoint, params):
    """Get count of records only in a given API call.

    Args:
        base_url (str): Base url
        endpoint (str): Endpoint name
        params (dict): Request params

    Returns:
        int: Number of records to expect
    """
    params['limit'] = 1
    print("*** get_record_count *************")
    # print(base_url)
    # print(endpoint)
    # print(params)
    response = get_data(base_url, endpoint, params)
    # print(response)
    if 'totalRecordCount' in response:
        return response['totalRecordCount']
    elif 'total_record_count' in response:
        return response['total_record_count']
    else:
        return None


def save_data(data, output_path):
    """save output as JSON file

    Args:
        data (dict): JSON representation
        output_path (str): path to save JSON
    """
    print(f"Saving to {str(output_path)}...")
    with open(output_path, "w") as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
