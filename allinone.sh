#!/bin/sh
#cd /Users/cary/Documents/DesktopCopy/arXiv/arxiv-sanity-preserver-master
python fetch_papers.py
python download_pdfs.py
python parse_pdf_to_text.py
python thumb_pdf.py
python analyze.py
python buildsvm.py
python make_cache.py
python serve.py