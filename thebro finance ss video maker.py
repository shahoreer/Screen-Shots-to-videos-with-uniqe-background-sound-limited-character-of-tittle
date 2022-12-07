#modules
import os
from moviepy.editor import *
import json

#path (_ at the end -> folder)
backgrounds_path_="/Users/shahoreertalha/Desktop/Work/TheBro Finance/background"
audios_path_="/Users/shahoreertalha/Desktop/Work/TheBro Finance/audio"
saved_vids_path_="/Users/shahoreertalha/Desktop/Work/TheBro Finance/vids" # folder to save finished vids
saveddata_path="/Users/shahoreertalha/Desktop/Work/TheBro Finance/data.json"
screen_shots_path_="/Users/shahoreertalha/Desktop/Work/TheBro Finance/ss"

#customizable variables
video_length=5
video_fps=1

#def 1...
def __json__func__(loc_path,read:bool,target="",data=0): 
     #loc_path = path of json file, read = true/false, target = targeted variable
          if read:
               with open(loc_path) as f:
                    data = json.load(f)
                    ret_data=data[target]
                    f.close()
                    return ret_data
          else:
               f= open(loc_path, 'w+')
               json.dump(data,f)
               f.close()

def loadfolder(path):
     arr=os.listdir(path)
     if arr.__contains__('.DS_Store'):
         arr.remove('.DS_Store')
     return arr

#program variables
sss= [screen_shots_path_+"/"+s for s in loadfolder(screen_shots_path_)] 
backgrounds=[backgrounds_path_+"/"+s for s in loadfolder(backgrounds_path_)] 
audios=[audios_path_+"/"+s for s in loadfolder(audios_path_)] 

backgroundnumlimit=len(backgrounds)-1
audionumlimit=len(audios)-1

audionum= __json__func__(saveddata_path,True,"audio")
backgroundnum= __json__func__(saveddata_path,True,"background")

#def 2...
def max_clamp_0(val:int,max:int):
     if val>max:
          return 0
     return val

def makevid(ss_path,background_path,audio_path,tittle):

    background=VideoFileClip(background_path).set_duration(5)
    background.audio=VideoFileClip(audio_path).audio.set_duration(video_length)

    ss = (ImageClip(ss_path).set_duration(video_length)
          .resize(width=background.size[0])
          .set_pos(("center","center")))

    finalvid = CompositeVideoClip([background, ss]).set_fps(video_fps)
    finalvid.write_videofile(saved_vids_path_+"/"+tittle,codec='libx264',audio_codec='aac')
    vidfinished()

def vidfinished():
     global backgroundnum,audionum
     backgroundnum=max_clamp_0(backgroundnum+1,backgroundnumlimit)
     audionum=max_clamp_0(audionum+1,audionumlimit)

def programfinished():
     newdata={ "audio": max_clamp_0(audionum,audionumlimit), "background": max_clamp_0(backgroundnum,backgroundnumlimit) }
     __json__func__(saveddata_path,False,data=newdata)


def findfilename(path):
     file_name = os.path.basename(path)
     return os.path.splitext(file_name)[0]

def writetittle(name):
     add= "#pop #music #lyrics #fyp #song #newsong #trending"
     return cut_bywords_cahr_limit(name+" "+add,150)+".mp4"

def cut_bywords_cahr_limit(string,limit):
    if len(string)>limit:
        string=string.split(" ")
        ret_str=""
        for i in string:
            if len(ret_str+i)>limit:
                return ret_str[1:]
            else:
                ret_str=ret_str+" "+i
    return string

#starter
for i in sss:
     makevid(i,backgrounds[backgroundnum],audios[audionum],writetittle(findfilename(i)))

programfinished()