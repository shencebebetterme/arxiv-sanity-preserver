# standard imports
import os
import sys
import pickle
import re
# non-standard imports
import numpy as np
from sklearn import svm
from sqlite3 import dbapi2 as sqlite3
# local imports
from utils import safe_pickle_dump, strip_version, Config



sqldb = sqlite3.connect(Config.database_path)


def query_db(query, args=(), one=False):
  """Queries the database and returns a list of dictionaries."""
  cur = sqldb.execute(query, args)
  rv = cur.fetchall()
  return (rv[0] if rv else None) if one else rv


db = pickle.load(open(Config.db_path, 'rb'))

saved_ids = query_db('''select * from library''')
# something like[(1, '1708.00871', 1, 1503193837),(2, '1707.09589', 1, 1503281105),(3, '1708.05606', 1, 1503295637)]

ids=[]
for saved_id in saved_ids:
    ids.append(saved_id[1])

#idversions = [db[id]['_rawid'] +'v'+ str(db[id]['_version']) for id in ids]

#titles = [db[id]['title'] for id in ids]

if not os.path.exists(Config.lib_dir):
	os.makedirs(Config.lib_dir)
have = set(os.listdir(Config.lib_dir))
# returns a collection 


def parse_title(title):
	title = title.replace(':','')
	title = title.replace('\n','')
	return title


def move_to(frompath, topath):
	print("cp "+frompath+' '+topath.replace(' ','\ '))
	os.system("cp "+frompath+' '+topath.replace(' ','\ '))

def add_to_lib(id):
	idversion = db[id]['_rawid'] +'v'+ str(db[id]['_version'])
	title = db[id]['title']
	title = parse_title(title)
	title_pdf = title + '.pdf'
	print ("adding %s" %title_pdf)
	move_to(Config.pdf_dir+'/'+idversion+'.pdf' , Config.lib_dir+'/'+title_pdf)


for id in ids:
	if not (db[id]['title']+'.pdf') in have:
		add_to_lib(id)
















