import json_to_pandas as j2p
import pandas as pd
import json
import io
from json2txttree import json2txttree
import xml2json as x2j

xmlFile = './input/xml/input.xml'
jsonFile = 'input/json/output.json'

# convert the xml to json
x2j.convert(xmlFile, jsonFile)

# convert the json to pandas dataframe, export to excel and csv
excel_file = 'results/data.xlsx'
csv_file = 'results/data.csv'

tree = j2p.JSONtree(jsonFile)
tree.to_excel(excel_file)
tree.to_csv(csv_file)