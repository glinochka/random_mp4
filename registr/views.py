from django.shortcuts import render
from django.http import HttpResponse
from video_rand.models import List, Video
from random import shuffle
 
def home(request):
	if 'enter' in request.POST:
		stream = List.objects.filter(user = request.user)[0]
		videos = list(Video.objects.filter(user = request.user))
		shuffle(videos)
		videos =[i.file.name for i in videos]
		playlist = '|'.join(videos)
		stream.listt = playlist
		stream.save()
		
	if str(request.user) == 'AnonymousUser':
		user ='Guest'
	else: user = request.user
	context = {
    	'user': user
	}
	
	return render(request, 'registr/home.html', context)
 
