import os
from conf import *
from time import sleep

paths=[baseDir,inputDir,outputDir,processDir]
for path in paths:
    if os.path.exists(path) is False:
        os.mkdir(path)

baseCmd='cmd.exe /C "C:\\Program Files (x86)\\EZTitlesDevelopmentStudio\\EZConvert6\\EZC6C.exe" -c "C:\\Users\\vvaru\\Desktop\\subs\\config\\pac2ts.cfg" -i PAC -o DVB '

listInput=os.listdir("C:\subs\input")
while True:
    print("Looking for files:")
    for name in listInput:
        print(listInput)
        basefn=name.split('.')[0]
        infn=f"{inputDir}\{name}"
        outfn=f"{outputDir}\{basefn}.ts"
        baseCmd+=f"{infn} {outfn}"
        print(baseCmd)
        os.system(baseCmd)
    sleep(10)