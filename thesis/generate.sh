#!/bin/bash
pbibtex main
platex main.tex
xdvipdfmx main.dvi
open main.pdf -a preview
cp main.pdf ~/Dropbox/Document/thesis.pdf
