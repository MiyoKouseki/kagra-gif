#!/bin/bash
#******************************************#
#     File Name: checkFilter.sh
#        Author: Takahiro Yamamoto
# Last Modified: 2018/12/21 14:13:34
#******************************************#

#######################################################################################
### chans directory
#######################################################################################
CHANS=./chans

#######################################################################################
### suffix of the channel name related with filter bank
#######################################################################################
SUFFS=`cat <<EOF
INMON EXCMON TRAMP OFFSET GAIN LIMIT OUTMON OUT16 OUTPUT
SW1 SW2 RSET SW1R SW2R SW1S SW2S
Name00 Name01 Name02 Name03 Name04 Name05 Name06 Name07 Name08 Name09
SWSTAT SWREQ SWMASK SWSTR IN1 EXC IN2 OUT
IN1_DQ EXC_DQ IN2_DQ OUT_DQ
EOF`

#######################################################################################
### argument check 1:  
###     arg1 = filter_name or channel_name related with filter bank
###   EXIT:: When arg1 is blank
#######################################################################################
[ "${1}" = "" ] && echo "usage: $0 filter_name [reference_file]" && exit 1
CHANNEL="${1}"

#######################################################################################
### generate filter name:
###     remove prefix, "K1:", and suffix such as "_IN1_DQ".
#######################################################################################
for suff in `printf "${SUFFS}"`
do
    CHANNEL=`printf ${CHANNEL} | sed -e "s/_${suff}//g"`
done
channel=${CHANNEL#*:}

#######################################################################################
### search filter name in all foton files:
###   EXIT:: If filter name cannot be found in foton file
#######################################################################################
HEADER1=`grep -hI "### ${channel} " ${CHANS}/*.txt`
[ "${HEADER1}" = "" ] && channel=${channel#*-}
HEADER1=`grep -hI "### ${channel} " ${CHANS}/*.txt`
[ "${HEADER1}" = "" ] && echo "Can't find ${channel}" && exit 1

#######################################################################################
### pick up design value (zpk) and filter discription from foton file
#######################################################################################
DESIGN1=`grep -hI "${channel} " ${CHANS}/*.txt | grep DESIGN`
COEFF1=`grep -hI "^${channel} " ${CHANS}/*.txt | grep -v DESIGN`

#######################################################################################
### argument check 2:
###     arg2 = reference foton file
###   case1:: arg2 is blank      -> just only display the filter name and design
###   case2:: reference is found -> display the filter name and design, and take diff
###    EXIT:: If reference cannot be found
#######################################################################################
flag=0
[ "${2}" != "" -a ! -e "${2}" ] && echo "Can't find ${2}"
[ "${2}" != "" -a -e "${2}" ] && let flag=1 && HEADER2=`grep -hI "### ${channel}" "${2}"`
[ "${2}" != "" -a "${HEADER2}" = "" ] && echo "Can't find ${channel} on ${2}" && exit 1

#######################################################################################
### pick up design value (zpk) and filter discription from reference file
#######################################################################################
[ ${flag} -eq 1 ] && DESIGN2=`grep -hI "${channel} " ${2} | grep DESIGN`
[ ${flag} -eq 1 ] && COEFF2=`grep -hI "^${channel} " ${2} | grep -v DESIGN`


#######################################################################################
### show header
#######################################################################################
printf "${HEADER1}\n" | cut -d' ' -f-2

#######################################################################################
### show filter module numbered from 0 to 9
#######################################################################################
idx=0
while test ${idx} -le 9
do
    design1=`printf "${DESIGN1}\n" | grep "${channel} ${idx} " | awk '{print $5}'`
    name1=`printf "${COEFF1}\n" | grep "${channel} ${idx} " | awk '{printf("%-15s\n", $7)}'`

    [ ${flag} -eq 1 ] && design2=`printf "${DESIGN2}\n" | grep "${channel} ${idx} " | awk '{print $5}'` || design2=${design1}
    [ ${flag} -eq 1 ] && name2=`printf "${COEFF2}\n" | grep "${channel} ${idx} " | awk '{printf("%-15s\n", $7)}'` || name2=${name1}
    
    printf "  ${idx}: ${name1} ${design1}\n"
    [ "${name1}" != "${name2}" -o "${design1}" != "${design2}" ] && printf "\033[31m  ${idx}: ${name2} ${design2}\033[00m\n\n"
    let idx=${idx}+1
done
