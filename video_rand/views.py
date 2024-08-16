from django.shortcuts import render
from .models import Video
from .models import List
from random import shuffle
import shutil
import os, cv2



def add(request):
    if len(request.FILES) > 0 :

        for video in request.FILES:
            Video(user = request.user, file = request.FILES[video]).save()
        if len(List.objects.filter(user = request.user))==0:
            List(user = request.user,listt = '').save()

    return render(request, 'video_rand/add.html')
def listof(request):
    videos = Video.objects.filter(user = request.user)[::-1]
    lens = List.objects.get(user=request.user).listt
    info = None
    if 'info' in request.POST:
        c = 'D:/Django/random_mp4/'
        info=0
        for dir in videos:
            fr = cv2.VideoCapture(c+dir.file.url).get(cv2.CAP_PROP_FPS)
            fn = cv2.VideoCapture(c+dir.file.url).get(cv2.CAP_PROP_FRAME_COUNT)
            info += (fn/fr)
        info = f'{int(info//60)}:{int(info%60)}'






    context = {
        'videos' : videos,
        'x' : lens,
        'info':info
    }
    return render(request, 'video_rand/list_of_vid.html', context)
def watch(request):
    stream = List.objects.filter(user = request.user)[0] 
    tvideos = list(Video.objects.filter(user = request.user))
    playlist = str(stream)
    req = request.POST
    if len(playlist)==0:
        shuffle(tvideos)
        videos =[i.file.name for i in tvideos]
        playlist = '|'.join(videos)
        stream.listt = playlist
        stream.save()
        video =playlist.split('|')[0]
    if 'enter' in req:
        video = playlist.split('|')[0]
        playlist = '|'.join(playlist.split('|')[1:])
        stream.listt = playlist
        stream.save()
    for file in tvideos:
        if file.file.name==video:
            video = file
            break
    context = {
        'req':req,
        'video':video
    }
    return render(request, 'video_rand/watch.html',context=context)

def submit(request):
    video=''
    req = request.POST
    if 'del' in request.POST:
        video = Video.objects.get(file = request.POST['del'])
    if 'delis' in request.POST:
        video = Video.objects.get(file = request.POST['delis'])
        if request.POST['delis']:
            
            c = 'D:/Django/random_mp4/'
            shutil.copy2(c+video.file.url,c+'videos/trash')
            
                
            Video.objects.get(file = request.POST['delis']).delete()
            return render(request, 'video_rand/error.html')
    context = {
        'x' : video,
        'req' : req
    }
    return render(request, 'video_rand/submit.html', context)