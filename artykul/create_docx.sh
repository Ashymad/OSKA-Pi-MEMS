#!/bin/sh
cp artykul.tex artykul.tmp.tex
sed '/\\input{.*\.pgf}/s/input/includegraphics/g; s/\.pgf/\.pdf/g' -i artykul.tmp.tex

pandoc --filter pandoc-citeproc\
    artykul.tmp.tex -f latex -t markdown\
    --default-image-extension=pdf\
    --bibliography=bibliografia.bib\
    --dpi 11200\
    -o artykul.md
rm artykul.tmp.tex
