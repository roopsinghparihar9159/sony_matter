dbHost="173.16.16.14"
dbUser="vod"
dbPass=""
dbName="vodTranscoder"
scriptdir="/opt/s3-webhook-transcode"
webhooklog="logs/webhook"
transcode_log="logs/transcode_log"
output_dir="/data/transcoder"
download_dir="%s/src" % (output_dir)
aws_access_key_id="AKIASTLI4S4OMLEZ2L6T"
aws_secret_access_key="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"
apiURL="https://www.ptivideos.com/pti"
transcode_profile=["200000|416:234|64k|0","1400000|640:480|96k|0","2200000|720:576|128k|1"] #,"4000000|1920:1080|128k|0"]
#transcode_profile=["200000|416:234|64k","1400000|640:480|96k","4000000|1920:1080|128k"]