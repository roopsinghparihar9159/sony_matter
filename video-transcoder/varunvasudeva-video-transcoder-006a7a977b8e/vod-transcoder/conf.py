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
# NS_HOSTNAME = 'alt-nsu.akamaihd.net'
# NS_KEYNAME = 'manojbhadana'
# NS_KEY = 'LNLO6GaOZckuFM3xh7jG6QF4EK7s90frhVkQiSqP' # Don't expose NS_KEY on public repository.
# NS_CPCODE = '1436641'
job_API = "http://webhook.multitvsolution.com:7005/transcoderjob_data/%s"
db_update_API = "http://webhook.multitvsolution.com:7005/update_db"
complete_tmAPI = "http://webhook.multitvsolution.com:7005/updatetime/%s"
trans_details="103.253.175.105"