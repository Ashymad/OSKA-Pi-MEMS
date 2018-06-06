.PHONY: pdf odt clean

SHELL := $(shell which bash)

IMAGES = ./bitgraphics/schemat_svg.png\
	 ./bitgraphics/pi.png\
	 ./bitgraphics/struktura.png\
	 ./bitgraphics/pom_2_cut.jpg\
	 ./bitgraphics/pom_1.jpg\
	 ./plots/accel_x.png\
	 ./plots/ghost_x.png\
	 ./plots/accel_2_xyz.png

IMGOUT = $(patsubst %.png, %.xbb, $(patsubst %.jpg, %.xbb, $(IMAGES)))

pdf: artykul.m4.pdf

odt: artykul.odt

clean:
	rm -f -- *.{tmp,4*,aux,blg,bcf,bbl,dvi,idv,lg,log,odt,out,run.xml,xref,toc,pdf} artykul.tex $(IMGOUT)

artykul.m4.pdf: artykul.m4.aux  artykul.m4.bbl artykul.m4.tex
	pdflatex artykul.m4.tex

%.bbl: bibliografia.bib %.aux
	biber $*
    
%.aux: %.tex
	pdflatex $?

artykul.odt: artykul.tex artykul.bbl $(IMGOUT)
	make4ht -uf odt artykul.tex

artykul.tex: artykul.m4.tex
	m4 -D m4_BUILD_TARGET=odt -P artykul.m4.tex > artykul.tex

$(IMGOUT): %.xbb: $(IMAGES)
	ebb -x $?
