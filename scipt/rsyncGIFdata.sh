#!/bin/bash
#******************************************#
#     File Name: rysncGIFdata.sh
#        Author: Kouseki Miyo
# Last Modified: 2018/04/10 
#******************************************#

function my_exit (){
    cat <<EOF

 usage: ikagraFileGet.sh [options] startGPS duration

   Arguments:
      startGPS:    Start GPS time in seconds
                   required startGPS >= 1000000000

      duration:    data length in seconds
                   required duration > 0

   Options: 
      -S server:   server name
                   default is k1fw0

      -d path:     save path on localhost 
                   default is ./"server"

      -u username: username on file server

      -D path:     file path on server (full path only)
                   default is /data/data_03 (betelgeuse, castor)
                              /data         (hyades, taurus, perseus)
                              /frames       (k1fw, other)

      -t type:     data type
                   default is full [science, minute, second, proc]

      -T length:   file length in seconds 
                   default is 32   (full, science, proc)
                              60   (minute)
                              3600 (second)

      -p prefix:   prefix of file name 
                   default is K-K1_C-       (full)
                              K-K1_R-       (science)
                              K-K1_M-       (minute)
                              K-K1_T-       (second)
                              K-K1_PROC_C00 (proc)

      -s suffix:   suffix of file name 
                   default is .gwf

      -h:          show this help

EOF
    exit ${CODE}
}

###  default param
FILE_SERVER=k1fw0
FILE_TYPE="full"
FILE_SUFFIX=".gwf"

### reserved param
SAVE_PATH=""
FILE_SIZE=""
FILE_PATH=""
FILE_PREFIX=""

### File param
FULL_PREF="K-K1_C-"
FULL_SIZE="32"
SCIENCE_PREF="K-K1_R-"
SCIENCE_SIZE="32"
MINUTE_PREF="K-K1_M-"
MINUTE_SIZE="3600"
SECOND_PREF="K-K1_T-"
SECOND_SIZE="60"
PROC_PREF="K-K1_PROC_C00-"
PROC_SIZE="32"

###  File path
HYADES_PATH="/data"
K1FW_PATH="/frames"
MOZUMI_PATH="/data"
KASHIWA_PATH="/data"
OSAKA_PATH="/data/data_03"


while getopts :d:S:u:t:T:D:p:s:h OPT
do
    case ${OPT} in
	d)  SAVE_PATH=${OPTARG}
	    ;;
        S)  FILE_SERVER=${OPTARG}
            ;;
        u)  USER_NAME=${OPTARG}
            ;;
        t)  FILE_TYPE=${OPTARG}
            ;;
        T)  FILE_SIZE=${OPTARG}
            ;;
	D)  FILE_PATH=${OPTARG}
	    ;;
	p)  FILE_PREFIX=${OPTARG}
	    ;;
	s)  FILE_SUFFIX=${OPTARG}
	    ;;
	h)  CODE=0 my_exit
	    ;;
        \?)  printf "\n[ \033[31mERROR\033[00m ] unknown option\n"
	    CODE=1 my_exit
            ;;
        ?)  printf "\n[ \033[31mERROR\033[00m ] few arguments\n"
	    CODE=1 my_exit
            ;;
    esac
done

shift $((OPTIND - 1))

#### type check
if test "${FILE_TYPE}" != "full" -a "${FILE_TYPE}" != "science" -a "${FILE_TYPE}" != "minute" -a "${FILE_TYPE}" != "second" -a "${FILE_TYPE}" != "proc"
then
    printf "\n[ \033[31mERROR\033[00m ] unknow data type\n"
    CODE=1 my_exit 
elif test "${FILE_TYPE}" = "full"
then
    if test "${FILE_SIZE}" = ""
    then
	FILE_SIZE="${FULL_SIZE}"
    fi
    if test "${FILE_PREFIX}" = ""
    then
	FILE_PREFIX="${FULL_PREF}"
    fi
elif test "${FILE_TYPE}" = "science"
then
    if test "${FILE_SIZE}" = ""
    then
	FILE_SIZE="${SCIENCE_SIZE}"
    fi
    if test "${FILE_PREFIX}" = ""
    then
	FILE_PREFIX="${SCIENCE_PREF}"
    fi
elif test "${FILE_TYPE}" = "minute"
then
    if test "${FILE_SIZE}" = ""
    then
	FILE_SIZE="${MINUTE_SIZE}"
    fi
    if test "${FILE_PREFIX}" = ""
    then
	FILE_PREFIX="${MINUTE_PREF}"
    fi
    FILE_TYPE="trend/${FILE_TYPE}"
elif test "${FILE_TYPE}" = "second"
then
    if test "${FILE_SIZE}" = ""
    then
	FILE_SIZE="${SECOND_SIZE}"
    fi
    if test "${FILE_PREFIX}" = ""
    then
	FILE_PREFIX="${SECOND_PREF}"
    fi
    FILE_TYPE="trend/${FILE_TYPE}"
elif test "${FILE_TYPE}" = "proc"
then
    if test "${FILE_SIZE}" = ""
    then
	FILE_SIZE="${PROC_SIZE}"
    fi
    if test "${FILE_PREFIX}" = ""
    then
	FILE_PREFIX="${PROC_PREF}"
    fi
fi

#### server check
if test "${FILE_PATH}" != ""
then
    :
elif test "${FILE_SERVER}" = "k1fw0" -o "${FILE_SERVER}" = "k1fw1"
then
    FILE_PATH="${K1FW_PATH}/${FILE_TYPE}"
elif test "${FILE_SERVER}" = "k1dm0" -o "${FILE_SERVER}" = "k1dm1"
then
    FILE_PATH="${HYADES_PATH}/${FILE_TYPE}"
elif test "${FILE_SERVER}" = "hyades-0" -o "${FILE_SERVER}" = "hyades-1"
then
    FILE_PATH="${HYADES_PATH}/${FILE_TYPE}"
elif test "${FILE_SERVER}" = "taurus-01" -o "${FILE_SERVER}" = "taurus-02"
then
    FILE_PATH="${MOZUMI_PATH}/${FILE_TYPE}"
elif test "${FILE_SERVER}" = "perseus-01" -o "${FILE_SERVER}" = "perseus-02"
then
    FILE_PATH="${KASHIWA_PATH}/${FILE_TYPE}"
elif test "${FILE_SERVER}" = "betelgeuse" -o "${FILE_SERVER}" = "castor"
then
    FILE_PATH="${OSAKA_PATH}/${FILE_TYPE}"
else
    FILE_PATH="${MOZUMI_PATH}/${FILE_TYPE}"
fi


#### arg check
if test ! ${2}
then
#    printf "\n[ \033[31mERROR\033[00m ] few arguments\n"
    CODE=1 my_exit 
elif test ${1} -lt 1000000000
then
    printf "\n[ \033[31mERROR\033[00m ] startGPS < 1000000000\n"
    CODE=1 my_exit
elif test ${2} -le 0
then
    printf "\n[ \033[31mERROR\033[00m ] duration <= 0)\n"
    CODE=1 my_exit
elif test "`echo ${FILE_PATH} | cut -c 1`" != "/"
then
    printf "\n[ \033[31mERROR\033[00m ] required full path (-D path)\n"
    CODE=1 my_exit
fi

if test "${SAVE_PATH}" = ""
then
    SAVE_PATH=${FILE_SERVER}
fi

###  GPS time
GPS_START=${1}                            # Start GPS time
GPS_DURATION=${2}                         # duration
let GPS_END=${GPS_START}+${GPS_DURATION}  # End GPS time

###  Temporary
HEAD_START=`echo ${GPS_START} | cut -c 1-5`
TAIL_START=`echo ${GPS_START} | cut -c 6-`
HEAD_END=`echo ${GPS_END} | cut -c 1-5`
TAIL_END=`echo ${GPS_END} | cut -c 6-`
TAIL_START_TMP=`expr ${TAIL_START} / ${FILE_SIZE} \* ${FILE_SIZE}`
TAIL_END_TMP=`expr ${TAIL_END} / ${FILE_SIZE} \* ${FILE_SIZE}`

###  GPS time (file)
FILE_START=${HEAD_START}`printf "%05d" ${TAIL_START_TMP}`
FILE_END=${HEAD_END}`printf "%05d" ${TAIL_END_TMP}`
let N_FILES=(${FILE_END}-${FILE_START})/${FILE_SIZE}+1

###  check
cat <<EOF

####################################################################
       Start GPS: ${GPS_START}
         End GPS: ${GPS_END}
        Duration: ${GPS_DURATION}

     Server name: ${FILE_SERVER}
       User name: ${USER_NAME}
       File path: ${FILE_PATH}
     File prefix: ${FILE_PREFIX}
     File suffix: ${FILE_SUFFIX}
   File duration: ${FILE_SIZE}

      Start File: ${FILE_PATH}/${HEAD_START}/${FILE_PREFIX}${FILE_START}-${FILE_SIZE}${FILE_SUFFIX}
        End File: ${FILE_PATH}/${HEAD_END}/${FILE_PREFIX}${FILE_END}-${FILE_SIZE}${FILE_SUFFIX}
 Number of files: ${N_FILES}

       Save path: ${SAVE_PATH}${FILE_PATH}
####################################################################

EOF

printf "Start transfer ? (Y/n): "
read YorN
while test "${YorN}" != "Y"
do
    if test "${YorN}" = "n"
    then
	echo "CANCELLED"
	exit 0
    fi
    printf "Start transfer ? (Y/n): "
    read YorN
done

HEAD_CURRENT=${HEAD_START}
while test ${HEAD_CURRENT} -le ${HEAD_END}
do
    mkdir -p ${SAVE_PATH}${FILE_PATH}/${HEAD_CURRENT} ### CMD"
    let HEAD_CURRENT=${HEAD_CURRENT}+1
done


if test "`echo ${SAVE_PATH} | cut -c 1`" = "/"
then
    TOP_DIR=""
else
    TOP_DIR=`pwd`"/"
fi
CUR_DIR=`pwd`
GPS_CURRENT=${FILE_START}
HEAD_CURRENT=`echo ${GPS_CURRENT} | cut -c 1-5`
echo "" > ${CUR_DIR}/tmp.batch

while test ${GPS_CURRENT} -le ${FILE_END}
do
    HEAD_BUFF=`echo ${GPS_CURRENT} | cut -c 1-5`
    echo "lcd ${TOP_DIR}${SAVE_PATH}${FILE_PATH}/${HEAD_CURRENT}" >> ${CUR_DIR}/tmp.batch
    while test ${HEAD_CURRENT} -eq ${HEAD_BUFF} -a ${GPS_CURRENT} -le ${GPS_END}
    do
	if test ! -e ${SAVE_PATH}/${FILE_PATH}/${HEAD_CURRENT}/${FILE_PREFIX}${GPS_CURRENT}-${FILE_SIZE}${FILE_SUFFIX}
	then
            echo "get ${FILE_PATH}/${HEAD_CURRENT}/${FILE_PREFIX}${GPS_CURRENT}-${FILE_SIZE}${FILE_SUFFIX}" >> ${CUR_DIR}/tmp.batch
	fi
	let GPS_CURRENT=${GPS_CURRENT}+${FILE_SIZE}
	HEAD_CURRENT=`echo ${GPS_CURRENT} | cut -c 1-5`
    done
    echo "" >> ${CUR_DIR}/tmp.batch
done

if test "${USER_NAME}" = ""
then
    sftp ${FILE_SERVER} < ${CUR_DIR}/tmp.batch ### CMD"
else
    sftp ${USER_NAME}@${FILE_SERVER} < ${CUR_DIR}/tmp.batch ### CMD"
fi

rm -f ${CUR_DIR}/tmp.batch

exit 0	
