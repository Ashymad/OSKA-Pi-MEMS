#!/bin/sh
cp artykul.tex artykul.tmp.tex
sed '/\\input{.*\.pgf}/s/input/includegraphics/g; s/\.pgf/\.png/g' -i artykul.tmp.tex

pandoc --filter pandoc-citeproc\
    artykul.tmp.tex -f latex -t docx\
    --default-image-extension=pdf\
    --bibliography=bibliografia.bib\
    --dpi 11200\
    -o artykul.docx
rm artykul.tmp.tex
