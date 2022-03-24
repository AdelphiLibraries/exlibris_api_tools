import json
import requests
import os
from configparser import ConfigParser
# from pprint import pprint
import csv
# import time

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)

CONFIG_PATH = os.path.join(MY_PATH, "config.ini")
config = ConfigParser()
config.read(CONFIG_PATH)

BASE_URL = config["URLS"]["esploro"]

# Select which key to use. You can have multiple in the config file, e.g., sandbox, production, etc.
API_KEY_DEV = config["KEYS"]["esploroDev"]
API_KEY = config["KEYS"]["esploro"]

OUTPUT_DIR = config["PATHS"]["outputDir"]
ASSETS_OUT_PATH = config["PATHS"]["assetsOutPath"]
RESEARCHERS_OUT_PATH = config["PATHS"]["researchersOutPath"]

PER_PAGE = int(config["DEFAULTS"]["perPage"])  # max 100
DATE_FROM = config["DEFAULTS"]["dateFrom"]  # earliest date to harvest


# Set MODE = "DEV" to use the Dev API key for operations
MODE = "DEV"


def main():

    # test code here
    quit()


def compile_researcher_ids(json_path):
    """Get a list of valid researcher ids

    Args:
        json_path (str): path to saved JSON researcher file from output_researchers()

    Returns:
        list: list of ids
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    return [r['primary_id'] for r in data['records']]


def get_researcher(researcher_id, base_url=BASE_URL):
    """Get single researcher from API

    Args:
        researcher_id (str): id
        base_url (str, optional): Base url. Defaults to BASE_URL.

    Returns:
        dict: JSON representation
    """
    api_key = API_KEY_DEV if MODE == "DEV" else API_KEY
    params = {
        'apikey': api_key,
        'view': 'full'
    }
    return get_data(base_url, f"researchers/{str(researcher_id)}", params)


def get_researchers(base_url=BASE_URL):
    # sourcery skip: use-fstring-for-concatenation
    """Get set of researchers from API and save as JSON.

    Args:
        base_url (str, optional): Base url. Defaults to BASE_URL.
    """
    api_key = API_KEY_DEV if MODE == "DEV" else API_KEY
    cursor = 0
    params = {
        'offset': cursor,
        'limit': PER_PAGE,
        'apikey': api_key,
    }
    record_cnt = get_record_count(base_url, "researchers", params)
    print("Found " + str(record_cnt) + " records.")
    out_records = []

    while cursor <= record_cnt:
        params['offset'] = cursor
        params['limit'] = PER_PAGE

        upper_bound = record_cnt if (
            cursor + PER_PAGE) >= record_cnt else cursor + PER_PAGE
        print("*** Getting records " + str(cursor + 1) +
              " to " + str(upper_bound) + " ...")
        out_records += get_data(base_url,  "researchers", params)['user']
        cursor += PER_PAGE

    return {"totalRecordCount": record_cnt,
            "records": out_records}


def save_researchers(data, output_path=RESEARCHERS_OUT_PATH):
    """save output from get_researchers() as json file

    Args:
        data (dict): JSON representation
        output_path (str): path to save JSON
    """
    print(f"Saving to {str(output_path)}...")
    with open(output_path, "w") as f:
        json.dump(data, f)


def get_assets(base_url=BASE_URL, date_from=DATE_FROM):
    # sourcery skip: use-fstring-for-concatenation
    """Get all assets matching date criteria.

    Args:
        base_url (str, optional): Base url. Defaults to BASE_URL.
        date_from (str, optional): Date in format YYYY-MM-DD. Defaults to DATE_FROM.
    """

    api_key = API_KEY_DEV if MODE == "DEV" else API_KEY
    cursor = 0
    params = {
        'offset': cursor,
        'update_date_from': date_from,
        'limit': PER_PAGE,
        'apikey': api_key,
    }

    record_cnt = get_record_count(base_url, "assets", params)
    print("Found " + str(record_cnt) + " records.")

    out_records = []

    while cursor <= record_cnt:
        params['offset'] = cursor
        params['limit'] = PER_PAGE

        upper_bound = record_cnt if (
            cursor + PER_PAGE) >= record_cnt else cursor + PER_PAGE
        print("*** Getting records " + str(cursor + 1) +
              " to " + str(upper_bound) + " ...")
        out_records += get_data(base_url,  "assets", params)['records']
        cursor += PER_PAGE

    return {"totalRecordCount": record_cnt,
            "records": out_records}


def save_assets(data, output_path=ASSETS_OUT_PATH):
    """save output from get_assets() as JSON file

    Args:
        data (dict): JSON representation
        output_path (str): path to save JSON
    """
    print(f"Saving to {str(output_path)}...")
    with open(output_path, "w") as f:
        json.dump(data, f)


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
    except requests.exceptions.RequestException as e:
        print('*** ERROR: could not connect to API. Check configuration. ' + str(e))
        print(f'URL: {url}')
        exit()

    return json.loads(r.content)


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


def output_researchers(json_file, dir=OUTPUT_DIR):
    """Save individual researcher data in one JSON file each.

    Args:
        json_file (str): Path to source JSON file as created by output_researchers()
        dir (str, optional): Directory to save files. Defaults to OUTPUT_DIR.
    """
    res_ids = compile_researcher_ids(json_file)
    for r in res_ids:
        out_path = os.path.join(dir, f'esploro_researcher_{r}.json')
        print(f"getting researcher id {str(r)}")
        x = get_researcher(r)
        with open(out_path, "w") as f:
            json.dump(x, f)


def read_researcher_data(id, dir=OUTPUT_DIR):
    """Read individual researcher data from saved JSON file. Must be run after output_researchers() has run. 

    Args:
        id (str): Researcher id
        dir (str, optional): Folder containing the JSON files. Defaults to OUTPUT_DIR.

    Returns:
        dict: JSON data 
    """
    filename = f'esploro_researcher_{str(id)}.json'
    filepath = os.path.join(dir, filename)
    with open(filepath, "r") as f:
        res_data = json.load(f)['researcher']
    return res_data


if __name__ == '__main__':
    main()
