#!/bin/sh
#chmod +x test_pdf.sh

cd data/pdf
for f in *.pdf; do
	if pdfinfo "$f" >/dev/null; then
		: Nothing
	else
		echo "$f" is broken
		echo deleting "$f"
		rm "$f"
	fi
done