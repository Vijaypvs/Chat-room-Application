from django.shortcuts import render,get_object_or_404, redirect
from django.utils.safestring import mark_safe
from .models import User,Chatroom
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request,'chat/index.html',{})
	else:
		return redirect('login')

def room(request, room_name):
	if request.user.is_authenticated:
		try:
			room=Chatroom.objects.get(name=json.dumps(room_name))
		except Chatroom.DoesNotExist:
			room=Chatroom(name=json.dumps(room_name),no_of_users=1)
			room.save()
		else:
			room.no_of_users=len(User.objects.filter(current_chat_room=Chatroom.objects.get(name=json.dumps(room_name))))
			room.save()
		request.user.current_chat_room=room
		return render(request, 'chat/room.html', {
			'room_name_json': mark_safe(json.dumps(room_name)),
			'no_of_users':room.no_of_users},
			)
	return redirect('logout')

def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('pass')
		user=authenticate(username=username,password=password)
		print(username,password)
		print(user)
		if user:
			auth_login(request,user)
			return redirect('index')
		else :
			return redirect('login')
	else:
		return render(request,'chat/login.html',{})


def register(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('pass')
		user_set = User.objects.filter(username=username)
		if user_set:
			return HttpResponse('User already exists')
		user = User.objects.create_user(username=username, password=password)
		auth_login(request,user)
		return redirect('index')
	else:
		return render(request, 'chat/register.html', {})


def logout(request):
	auth_logout(request)
	return redirect('login')
