#importing the modules
import xmltodict
import json

def convert(xml_file, json_file):
    xmlFile = open(xml_file, 'r')
    xmlString = xmlFile.read()
    xmlDict = xmltodict.parse(xmlString)
    jsonString = json.dumps(xmlDict)
    jsonFile = open(json_file, 'w+')
    jsonFile.write(jsonString)
    jsonFile.close()
    xmlFile.close()
    print('Conversion completed')