import json_to_pandas as j2p
import pandas as pd
import json
import io
from json2txttree import json2txttree
import xml2json as x2j
from isolate_object import SearchPattern

xmlFile = './input/xml/input.xml'
jsonFile = 'input/json/output.json'

# convert the xml to json
x2j.convert(xmlFile, jsonFile)

# convert the json to pandas dataframe, export to excel and csv
excel_vertical_file = 'results/xlsx/IND_vertical.xlsx'
csv_vertical_file = 'results/csv/IND_vertical.csv'
excel_horizontal_file = 'results/xlsx/IND_horizontal.xlsx'
csv_horizontal_file = 'results/csv/IND_horizontal.csv'

tree = j2p.JSONtree(jsonFile)
# if you want to extract the table in a vertical format, uncomment the following line
tree.to_excel(excel_vertical_file)
tree.to_csv(csv_vertical_file)

# if you want to extract the table in a horizontal format, uncomment the following line
sp = SearchPattern(tree.df)
code = 'IND'
sp.to_excel(code, excel_horizontal_file)
sp.to_csv(code, csv_horizontal_file)