import esploro_api as api
import csv
from pprint import pprint

# Example script to read the combined researcher output and generate
# a lookup CSV of ids and primary email address

# The file to read
researcher_json_path = "output/prod/esploro_researchers_PROD.json"

# The file to write to
csv_path = "output/prod/output_researchers_info.csv"


def process_researcher(id, data):
    # Put logic for extracting the data you want here
    return [id, data['contact_info']['email'][0]['email_address']]


# This reads the JSON and outputs the desired data in CSV
the_ids = api.compile_researcher_ids(researcher_json_path)
out_data = []
for r in the_ids:
    print(r)
    res_data = api.read_researcher_data(r, dir="output/prod")
    out_data.append(process_researcher(r, res_data))
print(out_data)
with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(out_data)
