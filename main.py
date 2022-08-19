import json_to_pandas as j2p
import pandas as pd
import json
import io
from json2txttree import json2txttree

jsonFile = 'input/json/output.json'
excel_file = 'results/data.xlsx'
csv_file = 'results/data.csv'

tree = j2p.JSONtree(jsonFile)
tree.to_excel(excel_file)
tree.to_csv(csv_file)