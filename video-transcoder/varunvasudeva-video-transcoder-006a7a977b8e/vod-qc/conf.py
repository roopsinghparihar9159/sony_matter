dbHost="173.16.16.14"
dbUser="vod"
dbPass=""
dbName="vodTranscoder"
webhooklog="logs/webhook"
transcode_log="logs/transcode_log"
output_dir="/storage/data"
download_dir="%s/src" % (output_dir)
aws_access_key_id="AKIASTLI4S4OMLEZ2L6T"
aws_secret_access_key="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"
job_API = "http://webhook.multitvsolution.com:7005/qcjob_data"
db_update_API = "http://webhook.multitvsolution.com:7005/QCupdate_db" # content_id,app_id,value
qc_fileupdate = "http://webhook.multitvsolution.com:7005/QCupdate_file" # content_id,app_id,fn,value
QC_finalUpdateAPI = "http://webhook.multitvsolution.com:7005/QC_finalUpdate" # content_id,app_id,fn,gpuvalue, qcvalue
trans_details="103.253.175.105"