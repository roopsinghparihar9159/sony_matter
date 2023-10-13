import requests
import subprocess
import os


# def curl_request(url):
    
#     # Define the command to execute using curl
#     command = ['curl', url]

#     # Execute the curl command and capture the output
#     result = subprocess.run(command, capture_output=True, text=True)
    
#     # Return the stdout of the curl command
#     return result.stdout

# # Make a curl request to https://www.google.com/
# response = curl_request("https://sony247channels.akamaized.net/hls/live/2011671/SETHD/master.m3u8?hdnea=st=1666483270~exp=1718323270~acl=/*~hmac=0b6d53622b73b15df03a3c3f55d6966442882d9a95c10d6a7f375f1a02801f6e -w 'Time Connect: %{time_connect},Total Time:%{time_total},Download Speed:%{speed_download},Http Code:%{http_code},Download Size:%{size_download}' -o /dev/null")

# # Make a curl request to https://www.google.com/
# print(response)



url1 = "curl https://sony247channels.akamaized.net/hls/live/2011671/SETHD/master.m3u8?hdnea=st=1666483270~exp=1718323270~acl=/*~hmac=0b6d53622b73b15df03a3c3f55d6966442882d9a95c10d6a7f375f1a02801f6e"
url = "curl https://sony247channels.akamaized.net/hls/live/2011671/SETHD/master.m3u8?hdnea=st=1666483270~exp=1718323270~acl=/*~hmac=0b6d53622b73b15df03a3c3f55d6966442882d9a95c10d6a7f375f1a02801f6e -w 'time_connect: %{time_connect},total_time:%{time_total},download_speed:%{speed_download},http_code:%{http_code},download_size:%{size_download}' -o /dev/null"

# os.system(url)

proc = subprocess.Popen([url], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
result = out
print("program output:", out)
print("program error:", err)
print('Result:',type(result))
# res_split = result.split(',')
output = result.decode()
print(output)
res_split = output.split(',')
# res_colon_split = res_split.split()
print(res_split)
collection_list = list()
for val in res_split:
    res_colon_split = val.split(':')
    collection_list.append(res_colon_split)
print(collection_list)
res_dict = dict(collection_list)
print(res_dict['time_connect'])


