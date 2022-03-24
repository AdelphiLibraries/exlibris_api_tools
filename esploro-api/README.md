# esploro-api

Python functions to interact with the ExLibris [Esploro API](https://developers.exlibrisgroup.com/esploro/apis/).

## Requirements

- Exlibris Developer API Key(s) with Esploro permissions
- Python >= 3.7
- requests library


## How to use

- Edit the config file and rename as config.ini. Include API keys, URL (if different), and default configuration values. 
- The API limits pagination to 100, so any number greater will be ignored.
- To get all assets or researchers you need at least a beginning date (dateFrom). To get all records set this date to before your earliest record creation.

### Data storage

Some functions allow you to save output locally as JSON. You will need to designate a location. See function-level documentation. 

### Calling functions

The main functions are in esploro_api.py. You can import them into another script and call them as needed. See sample.py for examples. See the docstrings in the functions for info about each function.

So far there are only GET functions, no POST. This is just intended to extract data for external use, e.g., in an analytics framework or to do QC in spreadsheets. 