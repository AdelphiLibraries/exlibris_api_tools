import esploro_api as api
import csv

# Example script to read the combined researcher output and generate
# a CSV of all user_identifier values, e.g., ORCID

# The file to read
researcher_json_path = "output/prod/esploro_researchers_PROD.json"

# The file to write to
csv_path = "output/prod/output_researchers_orcid.csv"


def process_researcher(id, data):
    # Put logic for extracting the data you want here
    return [[id, uid['id_type']['value'], uid['value']] for uid in data['user_identifier']]


# This reads the JSON and outputs the desired data in CSV
the_ids = api.compile_researcher_ids(researcher_json_path)
out_data = []
for r in the_ids:
    res_data = api.read_researcher_data(r, dir="output/prod")
    if 'user_identifier' in res_data:
        out_data.extend(process_researcher(r, res_data))
with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(out_data)
