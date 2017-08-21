import os
import time
import pickle
import random
import argparse
import urllib.request
import feedparser
import urllib.request
import re

from utils import Config, safe_pickle_dump
from bs4 import BeautifulSoup
from inject import generate_j_dic




def dump_rawid(rawid,dumpdic):
    db = pickle.load(open(Config.db_path, 'rb'))
    if not rawid in db or j['_version'] > db[rawid]['_version']:
    	db[rawid]=dumpdic
    	safe_pickle_dump(db, Config.db_path)

#db = pickle.load(open(Config.db_path, 'rb'))
#idversion_array = ['1604.07818']
idversion_array=['1604.07818']
#del db['1604.07818']
for idversion in idversion_array:
	j = generate_j_dic(idversion)
	rawid = j['_rawid']
	dump_rawid(rawid,j)





