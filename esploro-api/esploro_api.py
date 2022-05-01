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

BASE_URL = config["URLS"]["esploro"]

# Select which key to use. You can have multiple in the config file, e.g., sandbox, production, etc.
API_KEY_DEV = config["KEYS"]["esploroDev"]
API_KEY = config["KEYS"]["esploro"]

OUTPUT_DIR = config["PATHS"]["outputDir"]
ASSETS_OUT_PATH = config["PATHS"]["assetsOutPath"]
RESEARCHERS_OUT_PATH = config["PATHS"]["researchersOutPath"]
ORGS_OUT_PATH = config["PATHS"]["orgsOutPath"]

PER_PAGE = int(config["DEFAULTS"]["perPage"])  # max 100
DATE_FROM = config["DEFAULTS"]["dateFrom"]  # earliest date to harvest


# Set MODE = "DEV" to use the Dev API key for operations
MODE = "PROD"

DEFAULT_PARAMS = {
    'apikey': API_KEY_DEV if MODE == "DEV" else API_KEY,
}


def main():
    # Test code here
    quit()


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


def get_assets(date_from=DATE_FROM):
    # TODO: document this
    params = DEFAULT_PARAMS
    params['update_date_from'] = date_from
    return iterate_response("assets", "records", params=params)["records"]


def get_researchers():
    # TODO: document this
    return iterate_response("researchers", "user")["user"]


def get_organizations():
    # TODO: document this
    return iterate_response("organizations/internal", "research_organization")["research_organization"]


def compile_researcher_ids(json_path):
    """Get a list of valid researcher ids

    Args:
        json_path (str): path to saved JSON researcher file from output_researchers()

    Returns:
        list: list of ids
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    # return [r['primary_id'] for r in data['records']]
    return [r['primary_id'] for r in data]


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
        save_json(x, out_path)


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
        res_data = json.load(f)
    return res_data


def save_json(data, output_path):
    """save output as json file

    Args:
        data (dict): JSON representation
        output_path (str): path to save JSON
    """
    print(f"Saving to {str(output_path)}...")
    with open(output_path, "w") as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
