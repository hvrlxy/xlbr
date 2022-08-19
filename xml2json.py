#importing the modules
import xmltodict
import json

xmlFile = open('./input/xml/input.xml', 'r')
xmlString = xmlFile.read()
xmlDict = xmltodict.parse(xmlString)
jsonString = json.dumps(xmlDict)
jsonFile = open('./input/json/output.json', 'w+')
jsonFile.write(jsonString)
jsonFile.close()
xmlFile.close()
print('Conversion completed')