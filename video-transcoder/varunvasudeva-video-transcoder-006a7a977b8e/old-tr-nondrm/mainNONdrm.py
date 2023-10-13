#!/usr/bin/python3
import os, subprocess, shlex, json,time,requests, urllib3
from subprocess import call,Popen,PIPE
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
speed="fast"
localpath="/opt/drm/"

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("result.stdout",result.stdout)
    return result.stdout
#     return float(result.stdout)

## Making a get request
response = requests.get('https://creator.multitvsolution.com/crons/transcode', verify=False)
url=json.loads(response.text)
err=(response.status_code)
if err == 404:
        print('\x1b[0;37;42m' + ' API list is empty! ' + '\x1b[0m')
        exit ()
else:
        print('\x1b[0;37;44m' + ' API list have data! ' + '\x1b[0m')
mp4_fn = []

for data in url[0]['content_id']:
        # access_key=(data['access_key'])  # drm_cid=(data['drm_cid']) # site_id=(data['site_id'])
        map_id = data['map_id']
        # content_preview_count = data['content_preview_count']
        flavor_id = data['flavor_id']
        flavor_name = data['flavor_name']
        vb = data['vb']
        ab = data['ab']
        txt = data['screen']
        screen = txt.replace("x",":")
        # port_screen = data['port_screen']
        # squar_screen = data['squar_screen']
        # frame_rate = data['frame_rate']
        content_id = data['content_id']
        name = data['name']
        # content_type = data['content_type']
        video_file_name = data['video_file_name']
        app_id = data['app_id']
        watermark_logo = data['watermark_logo']
        watermark_pos = data['watermark_pos']
        cloudfront = data['cloudfront']
        bucket = data['bucket']

        p2 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'inprocess'})
        print(p2.status_code, p2.reason)
        print (p2)

## check logo
        if watermark_logo == None:
                print ("NO LOGO")
        else:
                print ("logo")
                a = urlparse(watermark_logo)
                logo_name = (os.path.basename(a.path))
                subprocess.run(shlex.split('curl '+watermark_logo+' --output '+localpath+''+logo_name+''))
                logo_ln = localpath+''+logo_name

                if watermark_pos == "TL": XY_LOGO = "10:10"
                elif watermark_pos == "TR": XY_LOGO = "main_w-overlay_w-10:10"
                elif watermark_pos == "TC": XY_LOGO = "x=(main_w-overlay_w)/2:10"
                elif watermark_pos == "BL":  XY_LOGO = "10:main_h-overlay_h-10"
                elif watermark_pos == "BR": XY_LOGO = "main_w-overlay_w-10:main_h-overlay_h-10"
                elif watermark_pos == "BC": XY_LOGO = "(main_w-overlay_w)/2:main_h-overlay_h-10"
                elif watermark_pos == "CR": XY_LOGO = "x=main_w-overlay_w-10:y=(main_h-overlay_h)/2"
                elif watermark_pos == "CL": XY_LOGO = "10:y=(main_h-overlay_h)/2"
                elif watermark_pos == "CC": XY_LOGO = "x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2"
                logo = '[0:v][1:v]overlay='+XY_LOGO

        ## check vod is currpted or not
        vod_check = os.system(f"ffprobe  -v quiet -i '{video_file_name}' ")
        if vod_check == 1:
                print('\x1b[0;37;42m' + ' VOD_CHECK Result is Currpted Video ' + '\x1b[0m')
                p1 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'error'})
                print(p1.status_code, p1.reason)
                exit ()
        else:
                print('\x1b[0;37;44m' + ' VOD_CHECK Result is OK ' + '\x1b[0m')

        ## check if vod not already exists on path then download
        if not os.path.exists(name):
                try:
                        print("video_file_name",video_file_name, "DOWNLOAD FILE: ",name)
                        subprocess.run(shlex.split(f"wget '{video_file_name}' -O {name}"))
                except:
                        p3 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'error'})
                        print(p3.status_code, p3.reason)
                        print (p3)
                        exit()


## check vod extensions
        time.sleep(1)
        x = name.split(".")
        extensions = (x[1])
        print (extensions) #Same as INPUT use travod
        travod = flavor_id+'_'+flavor_name+'.'+extensions
        fextensions = 'mp4' #Force change in MP4 fextensions
        tranvod = flavor_id+'_'+flavor_name+'.'+fextensions
        travod_path = (x[0])
        print (travod_path)

## call duration function
        duration = get_length(video_file_name)
#        print (duration)

## check logo
        if watermark_logo == None:
                print("NO LOGO")
## transcoding without logo
                if not os.path.exists(travod_path):
                        os.system('mkdir '+travod_path+' ')
## for travod.mp4
                subprocess.run(shlex.split('ffmpeg -y -i '+name+' \
-pix_fmt yuv420p -r 25 -vcodec libx264 -vf "scale='+screen+'" -b:v '+vb+' -preset '+speed+' -profile:v baseline -keyint_min 25 -g 50 -x264opts no-scenecut -strict experimental -movflags +faststart -acodec aac -b:a '+ab+'  -map_metadata -1 -f mp4 '+travod_path+'/'+tranvod ))
                mp4_fn.append(travod_path+'/'+tranvod)
        else:
                print("logo")
## transcoding with logo
                if not os.path.exists(travod_path):
                        os.system('mkdir '+travod_path+' ')
## for travod.mp4
                CMD = 'ffmpeg -y -i '+name+' -i '+logo_ln+' -pix_fmt yuv420p -r 25 -vcodec libx264 -filter_complex \"'+ logo+',scale='+screen+'\"  -b:v '+vb+' -preset '+speed+' -profile:v baseline -keyint_min 25 -g 50 -x264opts no-scenecut -strict experimental -movflags +faststart -acodec aac -b:a '+ab+'  -map_metadata -1 -f mp4 '+travod_path+'/'+tranvod
                subprocess.run(shlex.split( CMD))
                mp4_fn.append(travod_path+'/'+tranvod)
#        exit ()
                print(CMD,' CMD')
        # p3 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'completed'}) # print(p3.status_code, p3.reason) # print(p3)
        # p2 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'inprocess'}) # print(p2.status_code, p2.reason) # print (p2)

## upload transcoded mp4
upload_cmd = f"aws s3 cp {travod_path} s3://{bucket}/multitv/video/{travod_path} --recursive --acl public-read"
print(upload_cmd)
p = Popen(upload_cmd,stdout=PIPE,stderr=PIPE,shell=True)
out,err = p.communicate()
err = err.decode('utf-8')
print("ERR: ",err)
# if(err != ''): return(False)
# else:
# 	return(True)
#? os.system('aws s3 cp '+travod_path+' s3://'+bucket+'/multitv/video/'+travod_path+' --recursive --acl public-read')

## loop end packaging start
#todo /usr/bin/packager  'in=/storage/data/mp4/1061_63a2aa060f3de_200000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/200000_$Number$.ts,playlist_name=200000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_350000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/350000_$Number$.ts,playlist_name=350000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_500000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/500000_$Number$.ts,playlist_name=500000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_700000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/700000_$Number$.ts,playlist_name=700000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_950000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/950000_$Number$.ts,playlist_name=950000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_2000000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/2000000_$Number$.ts,playlist_name=2000000.m3u8'  'in=/storage/data/mp4/1061_63a2aa060f3de_4500000.mp4,stream=video,segment_template=/storage/data/hls/1061_63a2aa060f3de/4500000_$Number$.ts,playlist_name=4500000.m3u8'   --segment_duration 4 --hls_master_playlist_output /storage/data/hls/1061_63a2aa060f3de/master.m3u8
# cmd="" # flavor_id="" # for data in url[0]['content_id']: #         cmd+=' '+travod_path+'/'+data['flavor_id']+'_'+data['flavor_name']+'.'+fextensions+'' # subprocess.run(shlex.split('PallyConPackager --site_id '+site_id+' --access_key '+access_key+' --content_id '+drm_cid+' --dash --hls -i '+cmd+' -o '+content_id+' '))
try: os.makedirs(f"./{content_id}")
except: pass
print(mp4_fn)
packager_cmd = "/usr/bin/packager "
# packager_cmd += " 'in=%s,stream=video,segment_template=%s/hls/%s/%s_$Number$.ts,playlist_name=%s.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
for mp4fn in mp4_fn:
        vbitrate = mp4fn.split('.')[0].split('_')[-1]
        packager_cmd += f" 'in={mp4fn},stream=video,segment_template={content_id}/{vbitrate}_$Number$.ts,playlist_name={vbitrate}.m3u8' "
packager_cmd += " --segment_duration 4 --hls_master_playlist_output %s/master.m3u8 " % (content_id)
print(packager_cmd)
print(f"Starting Packaging")
# subprocess.run(shlex.split(packager_cmd))
p = Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
out,err = p.communicate()
if(p.returncode != 0): status = "error"
else: status = "completed"
#todo ########################
## check file size
file_size = os.stat(name)
print("Size of file :", file_size.st_size, "bytes")

## upload transcoded content
upload_content = f"aws s3 cp {content_id} s3://{bucket}/{app_id}/{travod_path} --recursive --acl public-read"
print(upload_content)
p = Popen(upload_content,stdout=PIPE,stderr=PIPE,shell=True)
out,err = p.communicate()
err = err.decode('utf-8')
print("ERR: ",err)
# os.system('aws s3 cp '+content_id+' s3://'+bucket+'/'+app_id+'/'+travod_path+' --recursive --acl public-read')

## remove local vod data
time.sleep(2)
#os.system( 'rm '+name+'' ) #os.system( 'rm -r '+travod_path+'' ) #os.system( 'rm -r '+content_id+'' ) #    print("The file does not exist")
p3 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': status})
print(p3.status_code, p3.reason)
print(p3)
dash=cloudfront+'/'+app_id+'/'+travod_path+'/dash/stream.mpd'
hls=cloudfront+'/'+app_id+'/'+travod_path+'/master.m3u8'
print (dash)
print (hls)
print (content_id)
p4 = requests.post('https://creator.multitvsolution.com/crons/tanscoded_url', verify=False, data = {'id': map_id, 'content_id': content_id, 'hls': hls, 'dash': dash, 'duration' : duration, 'hls_size': file_size})
print(p4.status_code, p4.reason) 
