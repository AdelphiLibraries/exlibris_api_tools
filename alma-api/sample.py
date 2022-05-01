import alma_api as alma
from pprint import pprint


alma.MODE = "DEV"

# uid = "1817899"
uid = "1901408"
pprint(alma.get_user_details(uid))

pprint(alma.get_po_lines())

quit()
