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
#GST=1219330818
GST=1219244418
#GST=1219158018
#GST=1219071618
#GST=1218985218
#GST=1218898818
#GST=1218812418
#GST=1218726018
#GST=1218639618
#GST=1218553218
#GST=1218466818 
#GST=1218380418
#GST=1218294018
#GST=1218207618
#GST=1218121218
#GST=1218034818
#GST=1217948418
#GST=1217862018 # no data
#GST=1217775618 # no data
#GST=1217689218 # no data
#GST=1217602818 # no data
DATATYPE=INMON
PLACE_LIST=("EXV_SEIS" "EYV_SEIS" "IXV_SEIS" "IMC_SEIS_MCI" "IMC_SEIS_MCE")
AXIS_LIST=('WE' 'NS' 'Z')
for PLACE in "${PLACE_LIST[@]}" ; do
    for AXIS in "${AXIS_LIST[@]}" ; do
	echo python main_plotDiary.py $GST K1:PEM-${PLACE}_${AXIS}_SENSINF_${DATATYPE}	
	python main_plotDiary.py $GST K1:PEM-${PLACE}_${AXIS}_SENSINF_${DATATYPE}	
    done
done
