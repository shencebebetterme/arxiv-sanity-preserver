#!/bin/sh
#chmod +x test_pdf.sh

# clear corrupted pdfs

#cd static/pdf
#for f in *.pdf; do
#	#
#	if pdfinfo "$f" >/dev/null; then
#		: Nothing
#	else
#		echo "$f" is broken
#		echo deleting "$f"
#		rm "$f"
#	fi
#done

# clear corrupted thumbs

cd static/thumbs
for filename in *.jpg; do
	file_size=`du -k "$filename" | cut -f1`
	if [ "$file_size" -eq 8 ]
	then
		echo "$filename" is broken, removing "$filename"
		rm "$filename"
	else
		: Nothing
	fi
done

# clear corrupted txt files

#cd data/txt
#for filename in *; do
#	filesize=`du -k "$filename" | cut -f1`
#	if [ "$filesize" -eq 0 ]; then
#		echo "$filename" corrupted, removing "$filename"
#		rm "$filename"
#	else
#		: Nothing
#	fi
#done








