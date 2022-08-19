# Importing the required libraries
import xml.etree.ElementTree as ET
import pandas as pd
from pyvirtualdisplay import Display
from selenium import webdriver
from collections import OrderedDict
from xbrl import XBRLParser, GAAP, GAAPSerializer
from xml.parsers.expat import ParserCreate, ExpatError, errors
import dateparser
import xmltodict
import time
import os
import csv
import sys
import sqlite3
import logging
import shutil
import zipfile
import glob
import configparser
import marshal


def dict_to_list(d, row_template, rows):
    for key in d:
        if isinstance(d[key], OrderedDict):
            if '#text' in d[key]:
                row_template[key] = d[key]['#text']
            else:
                dict_to_list(d[key], row_template.copy(), rows)
    if row_template not in rows:
        rows.append(row_template)
    for key in d:
        if isinstance(d[key], list):
            for sub_d in d[key]:
                dict_to_list(sub_d, row_template.copy(), rows)
cols = ['INSTNAME', 'CUSIP','IRTD', 'CR', 'MD', 'PV', 'ISUD', 'IP', 'R', 'RAD', 'RAC','RT', 'RST', 'RTT', 'OAN', 'WST', 'ROL']
rows = []
def parse_xml(file_path):
    with open(file_path,'rb') as f:
        dict_data = xmltodict.parse(f.read())
    list_data_raw = []
    try:
        target_data = dict_data['xbrli:xbrl']['ROCRA']
    except KeyError:
        try:
            target_data = dict_data['xbrli:xbrl']['r:ROCRA']
        except KeyError:
            try:
                target_data = dict_data['xbrli:xbrl']['rt:ROCRA']
            except KeyError:
                target_data = dict_data['xbrli:xbrl']['ISD']
    dict_to_list(target_data, OrderedDict(), list_data_raw)
    max_len = max([len(r) for r in list_data_raw])
    list_data = [r for r in list_data_raw if len(r) == max_len]


    for j in range(len(target_data['ISD']['IND'])):  
        try:
            cusip = target_data['ISD']['IND'][j]['CUSIP']['#text']
        except KeyError:
            cusip = 0    
        try:
            instrument_name = target_data['ISD']['IND'][j]['INSTNAME']['#text:']
        except KeyError:
            instrument_name =0
        try:
            maturity_date=target_data['ISD']['IND'][j]['MD']['#text']
        except KeyError:
            maturity_date = 0
        try:
            par_value= target_data['ISD']['IND'][j]['PV']['#text']
        except KeyError:
            par_value = 0
        try:
            instrument_rate_type = target_data['ISD']['IND'][j]['IRTD']['#text']
        except KeyError:
            instrument_rate_type=0
        try:
            instrument_issuance_date=target_data['ISD']['IND'][j]['ISUD']['#text']
        except KeyError:
            instrument_issuance_date = 0
        try: 
            coupon_date = target_data['ISD']['IND'][j]['CR']['#text']
        except KeyError:
            coupon_date = 0

        for i in range(len(target_data['ISD']['IND'][j]['INRD'])):
            try:
                issued_paid= target_data['ISD']['IND'][j]['INRD'][i]['IP']['#text']
            except KeyError:
                issued_paid= 0
            try:
                rating=target_data['ISD']['IND'][j]['INRD'][i]['R']['#text']
            except KeyError:
                rating = 0
            try:
                rating_action_date = target_data['ISD']['IND'][j]['INRD'][i]['RAD']['#text']
            except KeyError:
                rating_action_date =0
            try:
                rating_action_class = target_data['ISD']['IND'][j]['INRD'][i]['RAC']['#text']
            except KeyError:
                rating_action_class =0
            try:
                rating_type = target_data['ISD']['IND'][j]['INRD'][i]['RT']['#text']
            except KeyError:
                rating_type=0
            try:
                rating_subtype = target_data['ISD']['IND'][j]['INRD'][i]['RST']['#text']
            except KeyError:
                rating_sub_type =0
            try:
                rating_type_term =target_data['ISD']['IND'][j]['INRD'][i]['RTT']['#text']
            except KeyError:
                rating_type_term =0
            try:
                other_announcement_type=target_data['ISD']['IND'][j]['INRD'][i]['OAN']['#text']
            except KeyError:
                other_announcement_type=0
            try:
                watch_status=target_data['ISD']['IND'][j]['INRD'][i]['WST']['#text']
            except KeyError:
                watch_status=0
            try:
                rating_outlook=target_data['ISD']['IND'][j]['INRD'][i]['ROL']['#text']
            except KeyError:
                rating_outlook=0
            
            rows.append({'INSTNAME':instrument_name,
                             'CUSIP':cusip,
                             'CR':coupon_date,
                             'MD':maturity_date,
                             'PV':par_value,
                             'ISUD': instrument_issuance_date,
                             'IRTD': instrument_rate_type,
                             'R': rating,
                             'IP':issued_paid,
                             'RAD':rating_action_date,
                             'RAC':rating_action_class,
                             'RT':rating_type,
                             'RST':rating_sub_type,
                             'RTT':rating_type_term,
                             'OAN':other_announcement_type,
                             'WST':watch_status,
                             'ROL':rating_outlook})


    df = pd.DataFrame(rows,columns=cols)
    df.to_csv('output.csv')


##result=pd.DataFrame()
##directory = os.chdir('/Users/dpham3/Dropbox/Duong/Moody-xbrl/test')
##for file in list(glob.glob('*.xml')):
##    data = marshal.dumps(file)
##    obj = marshal.loads(data)
##    parse_xml(obj)
##    df = pd.DataFrame(rows, columns=cols)
##    #result=result.append(df)
##    #result = pd.concat([result,pd.DataFrame.from_records(df)])
##    df.to_csv('output.csv')  
##path =r'/Users/dpham3/Dropbox/Duong/Moody-xbrl'
##old_type='xml'
##new_type='csv'
##files=os.listdir(path)
##for file in files:
##    if os.path.isfile(file):
##        temp = file.split('.')
##        if (len(temp)>1):
##            if (temp[-1]==old_type):
##                del temp[-1]
##    parse_xml(file)
##new_name=str('.'.join(temp)),
##
##os.rename(os.path.join(path,file),os.path.joim(path,f"{new_name}.{new_type}"))
#df = pd.DataFrame(rows, columns=cols)
#df.to_csv('output.csv')           

##    if 'FCD' not in list_data[0] and 'r:FCD' not in list_data[0] and 'rt:FCD' not in list_data[0]:
##        fcd = dict_data['xbrli:xbrl']['FCD']['#text']
##        for row in list_data:
##            row['FCD'] = fcd
##    if 'RAN' not in list_data[0] and 'r:RAN' not in list_data[0] and 'rt:RAN' not in list_data[0]:
##        ran = dict_data['xbrli:xbrl']['RAN']['#text']
##        for row in list_data:
##            row['RAN'] = ran
##    return list_data


