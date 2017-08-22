
# arxiv sanity preserver

This project is forked form Karpathy's original [arxiv sanity preserver](https://github.com/karpathy/arxiv-sanity-preserver) with following offline-use-oriented new features:

1. Some downloaded pdf files are corrupted and raise errors in later process, so adding a function to detect the integrity of downloaded pdf. It will be downloaded again if corrupted.

2. A new module `inject.py` is added in case that you want to add a few papers to the database by hand.
3. <ul><li>In localhost, the title of each paper redirects to a local pdf file rather than to the arxiv website, therefore papers can be opened immediately in a new browser tab</li><li>A minimal MathJax is added to the `/static` directory to show LaTeX formulas offline</li></ul>so arxiv-sanity can be used totally offline!
4. Allow searching by id according to [conor-f's commit](https://github.com/karpathy/arxiv-sanity-preserver/pull/89/commits/93530f972c46a8bec796f49bfe6c105176d1c403)
5. A Unix shell script is add for convenience


## usage

### prerequisites
follow this recommended order to install necessary packages

* download and install [Anaconda Python](https://www.continuum.io/downloads), the default python 2.7 on Mac is obsolete and lack useful packages
* open terminal and check whether `homebrew` is installed

```bash
$ brew
```
  if not, install `homebrew` through
  
  ```bash
 $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
* install and configure mongo database following [stackoverflow instructions](https://stackoverflow.com/questions/5596521/what-is-the-correct-way-to-start-a-mongod-service-on-linux-os-x)

* install `ImageMagic` 

```bash
$ brew install imagemagick
```

* install `pdftotext` according to [this page](http://macappstore.org/pdftotext/)

* `cd` to arxiv-sanity project directory and do

```bash
$ pip install -r requirements.txt

``` 

### start using
change some parameters before running:

* open `fetch_papers.py` with a text editor and find line 60 and 61, the two default values can be changed freely

```python
parser.add_argument('--max-index', type=int, default=3, help='upper bound on paper index we will fetch')
parser.add_argument('--results-per-iteration', type=int, default=3, help='passed to arxiv API')
```

* in line 85, the `offset` parameter controls where to begin downloading. If you set offset=0, then the script starts downloading from the newest article

```python
 offset = 0
```

* a simple shell script is created for convenience, `allinone.sh` performs a all-in-one job from fetching articles to downloading pdf files, and to setting up a localhost server. But before running this shell script you should give permission to it (in the same project directory):

```
$ chmod +x ./allinone.sh
```

now you have the permission to run, just do 

```
$ ./allinone.sh
```
this is equivalent to running all the python scripts one by one:

```bash
$ python fetch_papers.py
$ python download_pdfs.py
$ python parse_pdf_to_text.py
$ python thumb_pdf.py
$ python analyze.py
$ python buildsvm.py
$ python make_cache.py
$ python serve.py
```


