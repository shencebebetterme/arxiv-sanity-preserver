import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen,Request

from utils import Config

timeout_secs = 15 # after this many seconds we give up on a paper
if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))
myheaders={}
myheaders["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"

def test_and_download_pdf(pdf_url, fname):
	time.sleep(1.5 + random.uniform(0,1))
	pdf_url_cn = pdf_url
	pdf_url_in = pdf_url.replace('cn','in')#indian mirror
	pdf_url_de = pdf_url.replace('cn','de')#german mirror
	pdf_url_es = pdf_url.replace('cn','es')#spanish mirror

	current_pdf_url = pdf_url_cn
	print('fetching %s into %s' % (current_pdf_url, fname))
	response = get_response(current_pdf_url)
	#print("Forbidden by all arxiv mirrors, try downloading after 20mins")
	#time.sleep(60*20)
	with open(fname, 'wb') as fp:
		shutil.copyfileobj(response, fp)
	# if the pdf file is corrupted
	if os.system("pdfinfo "+fname)==256:
		test_and_download_pdf(current_pdf_url,fname)
	

def get_response(current_pdf_url):
	req = Request(current_pdf_url, None, myheaders)
	return urlopen(req)



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
		else:
			print('%s exists, skipping' % (fname, ))
		numok+=1
	except Exception as e:
		print('error downloading: ', pdf_url)
		print(e)
	
	print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))
	
print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))

