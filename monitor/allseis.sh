#! /bin/bash


usage_exit() {
    echo "Usage: $0 [-a] [-d dir] item ..." 1>&2
    exit 1
}

while getopts ad:h OPT
do
    case $OPT in
	a)  FLAG_A=$OPTARG
	    ;;
	d)  VALUE_D=$OPTARG
	    ;;
	h)  usage_exit
	    ;;
	\?) usage_exit
	    ;;
    esac
done


shift $((OPTIND - 1))



GST=1218466818
GET=1218553217
DATATYPE=INMON
PLACE_LIST=("EXV" "EYV" "IXV")
AXIS_LIST=('WE' 'NS' 'Z')
for PLACE in "${PLACE_LIST[@]}" ; do
    for AXIS in "${AXIS_LIST[@]}" ; do
	echo python main.py $GST $GET K1:PEM-${PLACE}_SEIS_${AXIS}_SENSINF_${DATATYPE}
	python main.py $GST $GET K1:PEM-${PLACE}_SEIS_${AXIS}_SENSINF_${DATATYPE}	
    done
done
