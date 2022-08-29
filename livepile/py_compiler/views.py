from concurrent.futures import Executor
import os
import re
import sys
from django.shortcuts import render, redirect
from .models import *
from forum.models import Profile

def join(request):
    context = {}
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)

    return render(request, 'py_compiler/join.html', context)

def compiler(request):
    context = {}
    # if user is logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        context['code'] = request.POST['code']
        try:
            original_stdout = sys.stdout
            sys.stdout = open('compiled.txt', 'w')
            exec(context['code'])
            sys.stdout.close()
            sys.stdout = original_stdout
            context['output'] = open('compiled.txt', 'r').read()
            os.remove("compiled.txt")
        except Exception as e:
            sys.stdout = original_stdout
            context['output'] = str(e)
    else:
        context['code'] = 'print("Hello World!")'
        context['output'] = 'Hello World!'
            
    return render(request, 'py_compiler/compiler.html', context)

def room(request):
    context = {}
    # if user is logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # form has been submitted
    if request.method == 'POST':
        try:
            room_type = request.POST['room_type']
            context['room_type'] = room_type
            room_name = request.POST['room_name']
            context['room_name'] = room_name
            # if username input is exmpty, name user to Anon
            if request.POST['username'] == '':
                username = "Anonymous"
            else:
                username = request.POST['username']
            # password required for private room
            if 'password' in request.POST:
                password = request.POST['password']
            else:
                password = ''
            # get/create room
            if (Room.objects.filter(room_name=room_name, type=room_type).exists()):
                room = Room.objects.get(room_name=room_name, type=room_type)
            else:
                room = Room.objects.create(room_name=room_name, password=password, type=room_type)
            # check password against room password
            if (room.password != password):
                context['errormsg'] = 'Incorrect password.'
                return render(request, 'py_compiler/join.html', context)
            else:
                # check if a user with same username already exists
                while (Participant.objects.filter(username=username, room=room).exists()):
                    tmp = Participant.objects.get(username=username, room=room).username
                    match = re.match(r"([a-z]+)([0-9]+)", tmp, re.I)
                    if match:
                        items = match.groups()
                        username = items[0] + str(int(items[1]) + 1)
                    else:
                        username = username + str(1)
                # add user to room
                Participant.objects.create(username=username, room=room)
                context['username'] = username
        except Exception as e:
            print("views.room() POST threw an error:", e)

    return render(request, 'py_compiler/room.html', context)