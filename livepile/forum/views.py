import re
import difflib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import *
from .forms import *

def register(request):
    context = {}
    context['registered'] = False
    # form has been submitted
    if request.method == 'POST':
        # get form data
        userForm = UserForm(data=request.POST)
        profileForm = ProfileForm(data=request.POST)
        # check if form is valid
        if userForm.is_valid() and profileForm.is_valid():
            # save user data
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            # save profile data
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.email = user.email
            if 'fname' in userForm.cleaned_data:
                profile.fname = request.DATA['fname']
            if 'lname' in userForm.cleaned_data:
                profile.lname = request.DATA['lname']
            profile.save()
            # change registered to true
            context['registered'] = True
    else:
        context['userForm'] = UserForm()
        context['profileForm'] = ProfileForm()

    return render(request, 'forum/register.html', context)

def forum_login(request):
    context = {}
    # form has been submitted
    if request.method == 'POST':
        # get credentials
        username = request.POST['username']
        password = request.POST['password']
        # authenticate credentials
        user = authenticate(username=username, password=password)
        # if authenticated successfully
        if user:
            # if user account not locked
            if user.is_active:
                # log user in
                login(request, user)
                # if a 'next' page has been specified, redirect to it instead of home
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                else:          
                    return redirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            context['errormsg'] = 'Invalid login credentials.'

    return render(request, 'forum/login.html', context)

def forum_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def profile(request, username):
    context = {}
    # if user is logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # get requested user's profile
    try:
        requested_user = User.objects.get(username=username)
        context['requested_profile'] = requested_user.profile
    except Exception as e:
        print("views.profile() threw an error:", e)
    # form has been submitted
    if request.method == 'POST':        
        try:
            if 'delete_post' in request.POST:
                Post.objects.filter(pk=request.POST['delete_post']).delete()
                context['post_deleted'] = 'Post has been deleted.'
            if 'delete_reply' in request.POST:
                Reply.objects.filter(pk=request.POST['delete_reply']).delete()
                context['reply_deleted'] = 'Reply has been deleted.'
        except Exception as e:
            print("views.profile() POST threw an error:", e)

    return render(request, 'forum/profile.html', context)

def edit(request):
    context = {}
    # if user is logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # form has been submitted
    if request.method == 'POST':
        try:
            user_form = UpdateUserForm(request.POST or None, instance=request.user)
            profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=context['my_profile'])
            if user_form.is_valid() and profile_form.is_valid():
                # save and redirect
                user_form.save()
                profile_form.save()
                return redirect('profile', request.user)
            else:
                print("user_form: ", user_form.errors)
                print("profile_form: ", profile_form.errors)
        except Exception as e:
            print('views.edit() threw an error:', e)
    else:
        context['user_form'] = UpdateUserForm(instance=request.user)
        context['profile_form'] = UpdateProfileForm(instance=context['my_profile'])

    return render(request, 'forum/edit.html', context)

def forum(request):
    context = {}
    # if user logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # get last five profiles ordered by most recently created
    new_members = Profile.objects.all().order_by('-created')[:5]
    context['new_members'] = new_members
    # get ten posts
    new_posts = Post.objects.all()[:10]
    context['new_posts'] = new_posts
    # get five tags
    tags = Tag.objects.all()[:5]
    context['tags'] = tags

    return render(request, 'forum/forum.html', context)

def post(request, pk):
    context = {}
    # if user logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # form has been submitted and user is logged in
    if request.method == 'POST':
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            content = request.POST['content']
            code = request.POST['code']
            try:
                if (code == '' or code == post.code):
                    reply = Reply(content=content, post=post, author=context['my_profile'])
                else:
                    reply = Reply(content=content, code=code, post=Post.objects.get(pk=pk), author=context['my_profile'])
                reply.save()
            except Exception as e:
                print("views.post threw an error:", e)
                context['errormsg'] = 'Reply was unsuccessful.'
        else:
            context['errormsg'] = 'You must be logged in to reply to a question.'

    try:
        # get post
        post = Post.objects.get(pk=pk)
        # # cleaning format
        post.content = post.content.replace("<code>", "<pre>")
        post.content = post.content.replace("</code>", "</pre>")
        context['post'] = post
        # get replies
        replies = post.get_replies()
        for reply in replies:
            reply.content = reply.content.replace("<code>", "<pre>")
            reply.content = reply.content.replace("</code>", "</pre>")
            if reply.code != '':
                newCode = compare(post.code, reply.code)
                reply.code = newCode
        context['replies'] = replies
    except Exception as e:
        print("views.post threw an error", e)

    return render(request, 'forum/post.html', context)

def ask(request):
    context = {}
    context['posted'] = False
    # get user (this view can only be accessed when a user is already logged in)
    context['my_profile'] = Profile.objects.get(user=request.user)
    # form has been submitted
    if request.method == 'POST':
        # get form data
        title = request.POST['title']
        content = request.POST['content']
        code = request.POST['code']
        # output = request.POST['output']
        if request.POST['tags'] == '':
            tag_array = []
        else:
            tag_array = request.POST['tags'].split(',')
        try:
            # create post
            post = Post(title=title, content=content, author=context['my_profile'], code=code)
            post.save()
            # add tags
            for tag_name in tag_array:
                if (Tag.objects.filter(tag=tag_name).exists() == False):
                    Tag.objects.create(tag=tag_name)
                post.tags.add(Tag.objects.get(tag=tag_name))
            # change posted to True
            context['posted'] = True
            context['post'] = post
        except Exception as e:
            context['errormsg'] = 'Post was unsuccessful.'
            print("views.ask threw an error:", e)

    return render(request, 'forum/ask.html', context)

def search(request):
    context = {}
    # if user logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # form has been submitted
    if request.method == 'POST':
        try:
            if 'search' in request.POST:
                input = request.POST['search']
                tags = Tag.objects.filter(tag__icontains=input)
                multiple_queries = Q(Q(title__icontains=input) | Q(tags__id__in=tags))
                results = Post.objects.filter(multiple_queries).distinct()
            if 'tag' in request.POST:
                input = request.POST['tag']
                tags = Tag.objects.filter(tag__icontains=input)
                results = Post.objects.filter(tags__id__in=tags).distinct()
            context['input'] = input
            context['results'] = results
        except Exception as e:
            print("views.search threw an error:", e)

    return render(request, 'forum/search.html', context)

def tags(request):
    context = {}
    # if user logged in, get their profile
    if request.user.is_authenticated:
        context['my_profile'] = Profile.objects.get(user=request.user)
    # get tags
    tags = Tag.objects.all()
    context['tags'] = tags
    return render(request, 'forum/tags.html', context)

# helper functions
# https://www.delftstack.com/howto/python/position-of-character-in-string/
def find_indices(s):
    list = []
    for pos, char in enumerate(s):
        if(char == "_"):
            list.append(pos)
    return list

# https://www.geeksforgeeks.org/find-all-ranges-of-consecutive-numbers-from-array/
def consecutiveRanges(a, n):
    length = 1
    list = []
    
    if (n == 0):
        return list
    for i in range (1, n + 1):
        if (i == n or a[i] - a[i - 1] != 1):
            if (length == 1):
                list.append(str(a[i - length]))
            else:
                temp = (str(a[i - length]) + ":" + str(a[i - 1] + 1))
                list.append(temp)
            length = 1
        else:
            length += 1
    return list

# https://towardsdatascience.com/side-by-side-comparison-of-strings-in-python-b9491ac858
def tokenize(s):
    return re.split('\s+', s)

def untokenize(ts):
    return ' '.join(ts)
        
def equalize(original, edited):
    l1 = tokenize(original)
    l2 = tokenize(edited)
    res1 = []
    res2 = []
    prev = difflib.Match(0,0,0)
    for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
        if (prev.a + prev.size != match.a):
            for i in range(prev.a + prev.size, match.a):
                res2 += ['_' * len(l1[i])]
            res1 += l1[prev.a + prev.size:match.a]
        if (prev.b + prev.size != match.b):
            for i in range(prev.b + prev.size, match.b):
                res1 += ['_' * len(l2[i])]
            res2 += l2[prev.b + prev.size:match.b]
        res1 += l1[match.a:match.a+match.size]
        res2 += l2[match.b:match.b+match.size]
        prev = match
    return untokenize(res1), untokenize(res2)

def compare(original, edited):
    s1, s2 = equalize(original, edited)
    arr1 = find_indices(s1)
    color_arr = consecutiveRanges(arr1, len(arr1))

    # my code
    words_to_highlight = []
    for color in color_arr:
        color = color.split(":")
        start = None
        end = None
        try:
            start = int(color[0])
            end = int(color[1])
        except Exception as e:
            pass
        words_to_highlight.append(s2[start:end])

    try:
        for i in range(len(words_to_highlight)):
            edited = edited.replace(words_to_highlight[i], "<span style='background-color: lightgreen; font-weight: bold;'>" + words_to_highlight[i] + "</span>")
    except Exception as e:
        print(e)
        
    edited = "<span>" + edited + "</span>"
    
    return edited