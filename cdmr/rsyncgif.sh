#!/bin/sh
rsync -av --include="*/" --include="*.STRAIN" --exclude="*" -e ssh GIF@172.16.32.201:/data1/PHASE/50000Hz/2018/08/27/* /Users/miyo/Dropbox/KagraData/gif/data1/PHASE/50000Hz/2018/08/27/
