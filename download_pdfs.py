import os
import time
import pickle
import shutil
import random
import re
from  urllib.request import urlopen,Request

from utils import Config

timeout_secs = 25 # after this many seconds we give up on a paper
if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))

myheaders={}
myheaders["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
pdf_url_pool=[]


def test_and_download_pdf(pdf_url, fname):
  if not pdf_url in pdf_url_pool:
    pdf_url_pool.append(pdf_url)
    Config.pdf_download_count=0
  print('fetching %s into %s' % (pdf_url, fname))
  basename = pdf_url.split('/')[-1]
  time.sleep(0.2 + random.uniform(0,1))
  #req = urlopen(Request(pdf_url, None, myheaders))
  #req = urlopen(pdf_url, None, timeout_secs)
  req = urlopen(Request(pdf_url,None,myheaders),None,timeout_secs)
  with open(fname, 'wb') as fp:
    shutil.copyfileobj(req, fp)
  # if the pdf file is corrupted
  if (os.system("pdfinfo "+fname)==256) and (Config.pdf_download_count<6):
    Config.pdf_download_count+=1
    test_and_download_pdf(pdf_url,fname)
  # download v1 instead 
  elif (os.system("pdfinfo "+fname)==256) and re.sub(r'v\d','v1',pdf_url) not in pdf_url_pool:
    new_pdf_url=re.sub(r'v\d','v1',pdf_url)
    # v1 already tried
    # v1 not tried, try downloading now
    Config.pdf_download_count=0
    test_and_download_pdf(new_pdf_url,fname)

  elif os.system("pdfinfo "+fname)==256:
    #Config.error_pdfs.append(pdf_url)
    # save the corrupted file info
    print("%s corrupted"%fname)
    os.system("touch data/corrupted_file/"+fname[11:])
  


for pid,j in db.items():
  pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
  assert len(pdfs) == 1
  pdf_url = pdfs[0] + '.pdf'
  pdf_url=pdf_url[:7]+'cn.'+pdf_url[7:]
  #print(pdf_url)
  basename = pdf_url.split('/')[-1]
  fname = os.path.join(Config.pdf_dir, basename)

  # try retrieve the pdf
  numtot += 1
  try:
    if not basename in have:
      print(pdfs)
      
      test_and_download_pdf(pdf_url,fname)
      #print('fetching %s into %s' % (pdf_url, fname))
      #req = urlopen(pdf_url, None, timeout_secs)
      #with open(fname, 'wb') as fp:
      #    shutil.copyfileobj(req, fp)
      #time.sleep(0.1 + random.uniform(0,0.1))
      print('\033[34m%d\033[0m/%d of %d downloaded ok.' % (numok, numtot, len(db)))
    #else:
      #print('%s exists, skipping' % (fname, ))
    numok+=1
  except Exception as e:
    print('\n\n\033[31merror downloading: %s\033[0m\n'%pdf_url)
    time.sleep(2)
    print(e)
  
  #print('\033[34m%d\033[0m/%d of %d downloaded ok.' % (numok, numtot, len(db)))


f=open("err_pdfs.txt","w")
f.write(str(Config.error_pdfs))
print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))

