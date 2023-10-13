#!/bin/bash

download_dir="/storage/data/src"
base="/home/transcoder/video-transcoder/vod-transcoder"
files=`mysql -N -s -h 173.16.16.14 -uvod vodTranscoder -e "select filename from LOC_transcoder where isTranscoded='-1';"`
logDir="${base}/logs"

hhmmss_to_secs() {
        time=$1
        seconds=`echo "$time" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 + ($4 / 25)}'`
        echo $seconds
}

for fn in $files
do
        basefn=`echo $fn | awk -F'.' '{print $1}'`
        src_duration=`ffprobe -hide_banner -v error -show_format -show_entries format=duration -of flat -i ${download_dir}/${fn} | head -1 | awk -F'=' '{print $2}' | sed 's/\"//g' | awk -F'.' '{print $1}'`
        elapsed_time=`cat ${logDir}/${basefn}.log | sed 's/\r/\n/g' | tail -n -1 | awk -F'=' '{print $9}' | awk -F'.' '{print $1}'`
        if [[ "$elapsed_time" == "" ]]; then
                exit
        fi
        elapsed_time=`hhmmss_to_secs ${elapsed_time}`
        complete_percentage=`echo "$elapsed_time/$src_duration * 100" | bc -l | awk -F'.' '{print $1}'`
        echo ${fn},${complete_percentage}
        mysql -N -s -h 173.16.16.14 -uvod vodTranscoder -e "update LOC_transcoder set percentage='${complete_percentage}%' where filename='${fn}';"
done