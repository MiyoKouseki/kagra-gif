#!/bin/bash

platex main.tex
xdvipdfmx main.dvi
open main.pdf -a preview
