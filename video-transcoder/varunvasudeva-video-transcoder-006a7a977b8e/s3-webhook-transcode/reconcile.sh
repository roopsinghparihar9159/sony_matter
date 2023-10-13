#!/bin/bash

#Syntax: bash reconcile.sh YYYY-mm-dd
dt=$1
if [[ "$dt" == "" ]]; then
        echo "Enter date in yyyy-mm-dd"
        exit
fi
#| dt                  | bucketname  | path        | qc     | isTranscoded | filename                                                                | isUploaded |
#insert into s3transcoder values('%s','%s','%s','%s','%s','%s','%s') on duplicate key update dt='%s',bucketname='%s',path='%s',qc='%s',isTranscoded='%s',isUploaded=%s" % (dt,bucketName,filePath,qc,isTranscoded,fn,isUploaded,dt,bucketName,filePath,qc,isTranscoded,isUploaded
files=`aws s3 ls s3://pti-octopus/pti-octopus/ | grep $dt | awk '{print $4}'`
for fn in $files
do
        echo "mysql -u vod vodTranscoder -e \"insert into s3transcoder values(\"$dt\",\"pti-octopus\",\"pti-octopus\",'0','0',\"$fn\");\"" #on duplicate key update dt=\"$dt\",bucketname='pti-octopus',path='pti-octopus',qc='0',isTranscoded='0',isUploaded='0');\""
        mysql -u vod vodTranscoder -e "insert into s3transcoder values('$dt','pti-octopus','pti-octopus','0','0','$fn','0');" #on duplicate key update dt=\"$dt\",bucketname='pti-octopus',path='pti-octopus',qc='0',isTranscoded='0',isUploaded='0');"
done