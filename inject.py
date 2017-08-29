"""
to add some papers that are not in the database yet,
so they can be downloaded the next time you run download_pdfs.py
"""


import os
import time
import pickle
import random
import argparse
import urllib.request
import feedparser
import re


from utils import Config, safe_pickle_dump
from bs4 import BeautifulSoup






def get_title(soup):
	return "<title>"+soup.find("h1", class_ = "title mathjax").find("span").next_sibling+"</title>"



def name_decoration(name):
	return "<author><name>"+name+"</name></author>"

def get_authors(soup):
	author_res=""
	authors = soup.find("div", class_ = "authors").find_all("a")

	for author in authors:
		author_res+=name_decoration(author.get_text())
	return(author_res)



def get_summary(soup):
	return "<summary>"+soup.find("blockquote", class_ = "abstract mathjax").find("span").next_sibling+"</summary>"


# published date and updated date
def extract_isoformat_date(timestring):
	#print(timestring)
	month_dic={'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
	#
	prog1 = re.compile(r"\d+")
	day_and_year = re.findall(prog1, timestring)
	day = day_and_year[0]
	if len(day)==1:
		day = '0'+day
	year = day_and_year[1]
	#
	prog2 = re.compile(r"[A-Z][a-z]{2}")
	month_word = re.findall(prog2, timestring)[0]
	month = month_dic[month_word]
	#
	return year + '-' + month + '-' + day + 'T18:00:09Z'

def get_date(soup):
	date_info = soup.find("div", class_ = "dateline").get_text()

	prog = re.compile(r"\d+\s\w+?\s\d{4}")
	result = re.findall(prog, date_info)
	if len(result)==2:
		# published date different from updated date
		published_date = extract_isoformat_date(result[0])
		updated_date = extract_isoformat_date(result[1])
	else:
		# still version 1, updated date is the same as published date
		published_date = extract_isoformat_date(result[0])
		updated_date = published_date
	return "<updated>"+updated_date+"</updated>"+"<published>"+published_date+"</published>"


def get_id(idversion):
	if idversion.find(".")!= -1:
		# more recent papers
		return "<id>http://arxiv.org/abs/"+idversion+"</id>"
	else:
		return "<id>http://arxiv.org/abs/hep-th/"+idversion+"</id>"
		#return "<id>http://arxiv.org/abs/"+idversion+"</id>"

def get_links(idversion):
	if idversion.find(".")!=-1:
		return """<link href="http://arxiv.org/abs/"""+idversion+"""" rel="alternate" type="text/html"/><link title="pdf" href="http://arxiv.org/pdf/"""+idversion+"""" rel="related" type="application/pdf"/>"""
	else:
		return """<link href="http://arxiv.org/abs/hep-th/"""+idversion+"""" rel="alternate" type="text/html"/><link title="pdf" href="http://arxiv.org/pdf/hep-th/"""+idversion+"""" rel="related" type="application/pdf"/>"""

# arxiv primary category
def get_pc(soup):
	cy = soup.find("div",class_ = "current").get_text()
	return "<arxiv:primary_category xmlns:arxiv='http://arxiv.org/schemas/atom' term='" +cy+ "' scheme=\"http://arxiv.org/schemas/atom\"/>"


def generate_article_link_cn(idversion):
	if idversion.find(".")!=-1:
		return "http://cn.arxiv.org/abs/"+idversion
	else:
		return "http://cn.arxiv.org/abs/hep-th/"+idversion

def get_tags(soup):
	cy = soup.find("div",class_ = "current").get_text()
	return "<tags>" + cy + "</tags>"

#def get_primary_cat(soup)

def get_soup(cn_url):
	time.sleep(1.5)
	print("fetching %s"%cn_url)
	f = urllib.request.urlopen(cn_url)
	response = f.read()
	soup = BeautifulSoup(response,'lxml')
	return soup


def get_xml(iv):
	cn_url = generate_article_link_cn(iv)
	soup = get_soup(cn_url)
	main_part= "<entry>"+get_id(iv)+get_date(soup)+get_pc(soup)+get_title(soup)+get_summary(soup)+get_tags(soup)+get_authors(soup)+get_links(iv)+ "</entry>"
	return main_part

def encode_feedparser_dict(d):
	""" 
	helper function to get rid of feedparser bs with a deep copy. 
	I hate when libs wrap simple things in their own classes.
	"""
	if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
		j = {}
		for k in d.keys():
		  j[k] = encode_feedparser_dict(d[k])
		return j
	elif isinstance(d, list):
		l = []
		for k in d:
		  l.append(encode_feedparser_dict(k))
		return l
	else:
		return d

def parse_arxiv_url(url):
	""" 
	examples is http://arxiv.org/abs/1512.08756v2
	we want to extract the raw id and the version
	"""
	ix = url.rfind('/')
	idversion = url[ix+1:] # extract just the id (and the version)
	parts = idversion.split('v')
	assert len(parts) == 2, 'error parsing url ' + url
	return parts[0], int(parts[1])

pre="""<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom"><link href="http://arxiv.org/api/query?search_query%3Dcat%3Ahep-th%26id_list%3D%26start%3D20%26max_results%3D1" rel="self" type="application/atom+xml"/><title type="html">ArXiv Query: search_query=cat:hep-th&amp;id_list=&amp;start=20&amp;max_results=1</title><id>http://arxiv.org/api/w7OBLXfq/5JLmD3NcNop0iAVzqE</id><updated>2017-08-20T00:00:00-04:00</updated><opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">118402</opensearch:totalResults><opensearch:startIndex xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">20</opensearch:startIndex><opensearch:itemsPerPage xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1</opensearch:itemsPerPage>"""
after="</feed>"



if __name__ == "__main__":
	#to_inject='1604.07818v1'
	to_inject = ['1511.04021v3','1412.6087v3','1611.07917v1']
	# the idversion
	# term problem need to be soved
	full_xml = ''
	for iv in to_inject:
		full_xml+=get_xml(iv)
	
	full_xml=pre+full_xml+after
	#print(full_xml)
	db = pickle.load(open(Config.db_path, 'rb'))
	parse = feedparser.parse(full_xml)
	num_added=0
	for e in parse.entries:
		j = encode_feedparser_dict(e)
		rawid, version = parse_arxiv_url(j['id'])
		#tag = j['tags']
		j['_rawid'] = rawid
		j['_version'] = version
		#print(j)
		#j['arxiv_primary_category'] = {'scheme': 'http://arxiv.org/schemas/atom','term': 'hep-th'}
		#j['tags']=[{'label': None, 'term': tag, 'scheme': 'http://arxiv.org/schemas/atom'}]
		if not rawid in db or j['_version'] > db[rawid]['_version']:
			db[rawid] = j
			num_added+=1
			print('Updated %s added %s' % (j['updated'].encode('utf-8'), j['title'].encode('utf-8')))
	
	if num_added>0:
		print('Saving database with %d papers to %s' % (len(db), Config.db_path))
		safe_pickle_dump(db, Config.db_path)












