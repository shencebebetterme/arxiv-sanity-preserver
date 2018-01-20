"""
Queries arxiv API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.
"""

import os
import time
import pickle
import random
import argparse
import urllib.request
import feedparser

from utils import Config, safe_pickle_dump



to_add='1801.00010,1801.04936'




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


if __name__ == "__main__":

  # parse input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--search-query', type=str,
                      #default='cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML',
                      default='cat:hep-th',
                      #default='au:Edward%20Witten'  
                      #default='ti:quantum%20chaos'
                      help='query used for arxiv API. See http://arxiv.org/help/api/user-manual#detailed_examples')
  parser.add_argument('--id-list', type=str, default=to_add)

  parser.add_argument('--start-index', type=int, default=0, help='0 = most recent API result')
  parser.add_argument('--max-index', type=int, default=500, help='upper bound on paper index we will fetch')
  parser.add_argument('--results-per-iteration', type=int, default=100, help='passed to arxiv API')
  parser.add_argument('--wait-time', type=float, default=5.0, help='lets be gentle to arxiv API (in number of seconds)')
  parser.add_argument('--break-on-no-added', type=int, default=1, help='break out early if all returned query papers are already in db? 1=yes, 0=no')
  args = parser.parse_args()

  # misc hardcoded variables
  base_url = 'http://export.arxiv.org/api/query?' # base api query url
  #print('Searching arXiv for %s' % (args.search_query, ))
  print('adding papers from arXiv: %s' % (args.id_list, ))

  # lets load the existing database to memory
  try:
    db = pickle.load(open(Config.db_path, 'rb'))
  except Exception as e:
    print('error loading existing database:')
    print(e)
    print('starting from an empty database')
    db = {}

  # -----------------------------------------------------------------------------
  # main loop where we fetch the new results
  print('database has %d entries at start' % (len(db), ))
  
  
  query = 'id_list=%s' % (args.id_list)
  #return #(max_results) results, starting from i+offset
  with urllib.request.urlopen(base_url+query) as url:
    response = url.read()
  parse = feedparser.parse(response)
  num_added = 0
  num_skipped = 0
  for e in parse.entries:
    #print("\n\n\n",e,"\n\n\n")
    j = encode_feedparser_dict(e)
    #
    # extract just the raw arxiv id and version for this paper
    rawid, version = parse_arxiv_url(j['id'])
    j['_rawid'] = rawid
    j['_version'] = version
    #
    # add to our database if we didn't have it before, or if this is a new version
    #if not rawid in db or j['_version'] > db[rawid]['_version']:
    if not rawid in db:
      # save a big dictionary j to the database
      db[rawid] = j
      #print(j['tags'])
      print('Updated %s added %s' % (j['updated'].encode('utf-8'), j['title'].encode('utf-8')))
      num_added += 1
      num_added_total += 1
    else:
      num_skipped += 1
  #
  # print some information
  print('Added %d papers, already had %d.' % (num_added, num_skipped))

#http://export.arxiv.org/api/query?search_query=cat:hep-th&sortBy=lastUpdatedDate&start=1&max_results=5
#http://export.arxiv.org/api/query?search_query=cat:hep-th&start=25000&max_results=5
#http://export.arxiv.org/api/query?id_list=1801.00010,0706.1230
#http://export.arxiv.org/api/query?search_query=au:edward%20witten




