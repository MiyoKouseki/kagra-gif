#!/bin/bash
mdls -name kMDItemFSName -name kMDItemNumberOfPages  ./*.pdf | cut -d= -f 2 | paste - -
