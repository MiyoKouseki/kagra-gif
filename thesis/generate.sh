#!/bin/bash
pbibtex main
platex main.tex
platex abstract.tex
xdvipdfmx main.dvi
xdvipdfmx abstract.dvi
open main.pdf -a preview
#open abstract.pdf -a preview
cp main.pdf ~/Dropbox/Document/thesis.pdf
cp abstract.pdf ~/Dropbox/Document/abstract.pdf
