
# arxiv sanity preserver

This project is forked form Karpathy's original [arxiv sanity preserver](https://github.com/karpathy/arxiv-sanity-preserver) with following offline-use-oriented new features:

1. Some downloaded pdf files are corrupted and raise errors in later process, so adding a function to detect the integrity of downloaded pdf. It will be downloaded again if corrupted.

2. A new module `inject.py` is added in case that you want to add a few papers to the database by hand.
3. <ul><li>In localhost, the title of each paper redirects to a local pdf file rather than to the arxiv website, therefore papers can be opened immediately in a new browser tab</li><li>A minimal MathJax is added to the `/static` directory to show LaTeX formulas offline</li></ul>so arxiv-sanity can be used totally offline!
4. Allow searching by id according to [conor-f's commit](https://github.com/karpathy/arxiv-sanity-preserver/pull/89/commits/93530f972c46a8bec796f49bfe6c105176d1c403)
5. A Unix shell script is add for convenience


