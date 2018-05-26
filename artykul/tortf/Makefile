all: xml html docx
docx: artykul.docx
html: artykul.html
xml: artykul.xml artykul.bib.xml

artykul.docx: artykul.html
	pandoc artykul.html\
	    -o artykul.docx

artykul.html: artykul.xml artykul.bib.xml
	latexmlpost artykul.xml\
	    --format html5\
	    --destination artykul.html\
	    --javascript='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=MML_CHTML'\
	    --bibliography artykul.bib.xml 

artykul.xml: artykul.tex
	latexml artykul.tex \
	    --destination artykul.xml

artykul.bib.xml: artykul.bib
	latexml artykul.bib\
	    --inputencoding utf-8\
	    --destination artykul.bib.xml

clean:
	rm -f *.xml *.cache *.css *.html *.docx
