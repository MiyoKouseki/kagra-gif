#! /bin/bash


usage_exit() {
    echo "Usage: $0 [-a] [-d dir] item ..." 1>&2
    exit 1
}

while getopts s:e:h OPT
do
    case $OPT in
	s)  GST=$OPTARG
	    ;;
	h)  usage_exit
	    ;;
	\?) usage_exit
	    ;;
    esac
done

shift $((OPTIND - 1))
DATATYPE=INMON
PLACE_LIST=("EXV_SEIS" "EYV_SEIS" "IXV_SEIS" "IMC_SEIS_MCI" "IMC_SEIS_MCE")
AXIS_LIST=('WE' 'NS' 'Z')
for PLACE in "${PLACE_LIST[@]}" ; do
    for AXIS in "${AXIS_LIST[@]}" ; do
	echo python main_plotDiary.py $GST K1:PEM-${PLACE}_${AXIS}_SENSINF_${DATATYPE}	
	python main_plotDiary.py $GST K1:PEM-${PLACE}_${AXIS}_SENSINF_${DATATYPE}	
    done
done
