import os
import subprocess

def videoconvert(url):
    print("program stated")
    cmd_240=f"ffmpeg -i {url} -vf scale=426:240 output_240p.mp4"
    os.system(cmd_240)

    cmd_360=f"ffmpeg -i {url} -vf scale=640:360 output_360p.mp4"
    os.system(cmd_360)

    cmd_480=f"ffmpeg -i {url} -vf scale=854:480 output_480p.mp4"
    os.system(cmd_480)

    thumbnail = f"ffmpeg -ss 00:00:53 -i {url} -frames:v 1 thumbnail.png"
    os.system(thumbnail)

    gif_command = f"ffmpeg -ss 00:00:10 -i {url} -to 10 -r 10 -vf scale=200:-1 video_gif_file.gif"
    os.system(gif_command)

    # duration = f"ffmpeg -i {url} 2>&1 | grep Duration"
    # os.system(duration)

    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1",url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# def get_length(filename):
#     result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
#                              "format=duration", "-of",
#                              "default=noprint_wrappers=1:nokey=1", filename],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT)
    
#     return float(result.stdout)
if __name__ == "__main__":

    path = "/home/roop/Roopsingh/python_api/video1.mp4"
    result = videoconvert(path)
    print('Duration of video:',result)
    # duration = get_length(path)
    # print(duration)