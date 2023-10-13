#!/usr/bin/python3
import os, sys, subprocess, shlex, re, json,time
from subprocess import call,Popen,PIPE
from urllib.parse import urlparse
# importing the requests library
# api-endpoint
# import requests module
import requests

speed="fast"
localpath="/opt/drm/"

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("result.stdout",result.stdout)
    return result.stdout
#     return float(result.stdout)

## Making a get request
response = requests.get('https://creator.multitvsolution.com/crons/drm_transcode', verify=False)
url=json.loads(response.text)
err=(response.status_code)
if err == 404:
        print('\x1b[0;37;42m' + ' API list is empty! ' + '\x1b[0m')
        exit ()
else:
        print('\x1b[0;37;44m' + ' API list have data! ' + '\x1b[0m')
for data in url[0]['content_id']:
        access_key=(data['access_key'])
        drm_cid=(data['drm_cid'])
        site_id=(data['site_id'])
        map_id=(data['map_id'])
        content_preview_count=(data['content_preview_count'])
        flavor_id=(data['flavor_id'])
        flavor_name=(data['flavor_name'])
        vb=(data['vb'])
        ab=(data['ab'])
        txt=(data['screen'])
        screen=txt.replace("x",":")
        port_screen=(data['port_screen'])
        squar_screen=(data['squar_screen'])
        frame_rate=(data['frame_rate'])
        content_id=(data['content_id'])
        name=(data['name'])
        content_type=(data['content_type'])
        video_file_name=(data['video_file_name'])
        app_id=(data['app_id'])
        watermark_logo=(data['watermark_logo'])
        watermark_pos=(data['watermark_pos'])
        cloudfront=(data['cloudfront'])
        bucket=(data['bucket'])

## check logo
        if watermark_logo == None:
                print ("NO LOGO")
        else:
                print ("logo")
                a = urlparse(watermark_logo)
                logo_name = (os.path.basename(a.path))
                subprocess.run(shlex.split('curl '+watermark_logo+' --output '+localpath+''+logo_name+''))
                logo_ln = localpath+''+logo_name

                if watermark_pos == "TL":
                              XY_LOGO = "10:10"
                elif watermark_pos == "TR":
                              XY_LOGO = "main_w-overlay_w-10:10"
                elif watermark_pos == "TC":
                              XY_LOGO = "x=(main_w-overlay_w)/2:10"
                elif watermark_pos == "BL":
                              XY_LOGO = "10:main_h-overlay_h-10"
                elif watermark_pos == "BR":
                              XY_LOGO = "main_w-overlay_w-10:main_h-overlay_h-10"
                elif watermark_pos == "BC":
                              XY_LOGO = "(main_w-overlay_w)/2:main_h-overlay_h-10"
                elif watermark_pos == "CR":
                              XY_LOGO = "x=main_w-overlay_w-10:y=(main_h-overlay_h)/2"
                elif watermark_pos == "CL":
                              XY_LOGO = "10:y=(main_h-overlay_h)/2"
                elif watermark_pos == "CC":
                              XY_LOGO = "x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2"
                logo = '[0:v][1:v]overlay='+XY_LOGO
        ## check vod is currpted or not
        vod_check = os.system(f"ffprobe -i '{video_file_name}' ")
        if vod_check == 1:
                print('\x1b[0;37;42m' + ' VOD_CHECK Result is Currpted Video ' + '\x1b[0m')
                p1 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'error'})
                print(p1.status_code, p1.reason)
                exit ()
        else:
                print('\x1b[0;37;44m' + ' VOD_CHECK Result is OK ' + '\x1b[0m')

## check vod already exists on path than dowload subprocess.run(shlex.split('curl -O '+video_file_name+''))
        if not os.path.exists(video_file_name):
                try:
                        print("video_file_name",video_file_name, "DOWNLOAD FILE: ",name)
                        subprocess.run(shlex.split(f"wget '{video_file_name}' -O {name}"))
                except:
                        p3 = requests.post('https://creator.multitvsolution.com/crons/drm_transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'error'})
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
                print ("NO LOGO")
## transcoding without logo
                if not os.path.exists(travod_path):
                        os.system('mkdir '+travod_path+' ')
## for travod.mp4
                subprocess.run(shlex.split('ffmpeg -y -i '+name+' \
-pix_fmt yuv420p -r 25 -vcodec libx264 -vf "scale='+screen+'" -b:v '+vb+' -preset '+speed+' -profile:v baseline -keyint_min 25 -g 50 -x264opts no-scenecut -strict experimental -movflags +faststart -acodec aac -b:a '+ab+' -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" -map_metadata -1 -f mp4 '+travod_path+'/'+tranvod ))
        else:
                print ("logo")
## transcoding with logo
                if not os.path.exists(travod_path):
                        os.system('mkdir '+travod_path+' ')
## for travod.mp4
                subprocess.run(shlex.split('ffmpeg -y -i '+name+' -i '+logo_ln+' -pix_fmt yuv420p -r 25 -vcodec libx264 -filter_complex \"'+ logo+',scale='+screen+'\"  -b:v '+vb+' -preset '+speed+' -profile:v baseline -keyint_min 25 -g 50 -x264opts no-scenecut -strict experimental -movflags +faststart -acodec aac -b:a '+ab+' -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" -map_metadata -1 -f mp4 '+travod_path+'/'+tranvod ))
#        exit ()
        p2 = requests.post('https://creator.multitvsolution.com/crons/transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'inprocess'})
        print(p2.status_code, p2.reason)
        print (p2)

## upload transcoded content
        os.system('aws s3 cp '+travod_path+' s3://'+bucket+'/multitv/video/'+travod_path+' --recursive --acl public-read')

## loop end packaging start
cmd=""
flavor_id=""
for data in url[0]['content_id']:
        cmd+=' '+travod_path+'/'+data['flavor_id']+'_'+data['flavor_name']+'.'+fextensions+''
print('PallyConPackager --site_id '+site_id+' --access_key '+access_key+' --content_id '+drm_cid+' --dash --hls -i '+cmd+' -o '+content_id+' ')
subprocess.run(shlex.split('PallyConPackager --site_id '+site_id+' --access_key '+access_key+' --content_id '+drm_cid+' --dash --hls -i '+cmd+' -o '+content_id+' '))

## check file size
file_size = os.stat(content_id)
print("Size of file :", file_size.st_size, "bytes")

## upload drm content
os.system('aws s3 cp '+content_id+' s3://'+bucket+'/'+app_id+'/'+travod_path+' --recursive --acl public-read')

## remove local vod data
time.sleep(2)
#os.system( 'rm '+name+'' )
#os.system( 'rm -r '+travod_path+'' )
#os.system( 'rm -r '+content_id+'' )
#    print("The file does not exist")
p3 = requests.post('https://creator.multitvsolution.com/crons/drm_transcodeupdate', verify=False, data = {'id': map_id, 'content_id': content_id, 'status': 'completed'})
print(p3.status_code, p3.reason)
print (p3)
dash=cloudfront+'/'+app_id+'/'+travod_path+'/dash/stream.mpd'
hls=cloudfront+'/'+app_id+'/'+travod_path+'/hls/master.m3u8'
print (dash)
print (hls)
print (content_id)
p4 = requests.post('https://creator.multitvsolution.com/crons/drm_tanscoded_url', verify=False, data = {'id': map_id, 'content_id': content_id, 'hls': hls, 'dash': dash, 'duration' : duration, 'hls_size': file_size})
print(p4.status_code, p4.reason) 