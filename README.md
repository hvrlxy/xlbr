# xlbr Converter

This is a small project I made for Duong, my ex-roommate, for her research in econometrics.

This program takes a xml file with xlbr format as input, parse it, and return the information in a readable format. To start the program, open the **main.py** file and change the name of the input file, and the output file name:

```
...

xmlFile = #insert file name here
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

...
```

After that, indicating the field name that you want to extract information from:

```
...

# if you want to extract the table in a horizontal format, uncomment the following line
sp = SearchPattern(tree.df)
code = #insert field name
sp.to_excel(code, excel_horizontal_file)
sp.to_csv(code, csv_horizontal_file)
```

After changing all the necessary information, simply run the **main.py** file:
```
python3 main.py
```

This is the sample output if you run the program on field "IND": [csv](https://github.com/hvrlxy/xlbr/blob/main/results/csv/IND_horizontal.csv), [excel](https://github.com/hvrlxy/xlbr/blob/main/results/xlsx/IND_horizontal.xlsx)

