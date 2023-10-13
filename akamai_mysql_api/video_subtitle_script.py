
import subprocess
import whisper
from whisper.utils import get_writer
import pandas as pd
model = whisper.load_model("base")

video_in = 'video1.mp4'
audio_out = 'audio.mp3'

ffmpeg_cmd = f"ffmpeg -i {video_in} -vn -c:a libmp3lame -b:a 192k {audio_out}"

subprocess.run(["ffmpeg", "-i", video_in, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", audio_out])

# result = model.transcribe(audio_out)
# print(result["text"])

result = model.transcribe(audio_out, verbose = True)
output_directory = "./"

# speech = pd.DataFrame.from_dict(result['segments'])
# print(speech.head())
# write_txt(result["segments"], file=txt)
# Save as an SRT file
srt_writer = get_writer("srt", output_directory)
srt_writer(result, audio_out)

f = open("vide_srtfile.txt", "a")
f.write(result["text"])
f.close()
print(result["text"])

# for write video subtitle ffmpeg command
# ffmpeg -i video1.mp4 -vf subtitles=audio.srt out.mp4