# Script to read a list of primary IDs and extract certain information to CSV, e.g., email and user_group.
import alma_api as alma
import csv


alma.MODE = "PROD"

id_file = "output/staff_uids.txt"
out_csv = "output/id_lookup.csv"


def main():

    with open(id_file, newline='') as f:
        reader = csv.reader(f)
        id_list = [r[0] for r in list(reader)]

    out_data = [["id", "email", "full_name", "user_group"]]

    for uid in id_list:
        user_data = alma.get_user_details(uid)
        print(f"UID: {str(uid)}")
        row = [uid,
               prop(prop(prop(prop(user_data, 'contact_info'), 'email'), 0),
                    'email_address'),
               prop(user_data, 'full_name'),
               prop(prop(user_data, 'user_group'), 'value'),
               ]
        out_data.append(row)

    with open(out_csv, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(out_data)


def prop(record, key):
    # extract property if it exists, without throwing errors if doesn't exist
    if record:
        try:
            return record[key]
        except (IndexError, KeyError):
            return None
    else:
        return None


if __name__ == '__main__':
    main()
