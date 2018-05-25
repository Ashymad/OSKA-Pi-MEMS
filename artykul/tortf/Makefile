artykul.docx: artykul.html
	pandoc artykul.html\
	    -o artykul.docx

artykul.html: artykul.xml artykul.bib.xml
	latexmlpost artykul.xml\
	    --destination artykul.html\
	    --bibliography artykul.bib.xml 

artykul.xml: artykul.tex
	latexml artykul.tex \
	    --destination artykul.xml

artykul.bib.xml: artykul.bib
	latexml artykul.bib\
	    --inputencoding utf-8\
	    --destination artykul.bib.xml
