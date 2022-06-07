from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,UploadImageForm,CommentForm
from django.contrib.auth.decorators import login_required
from .models import Image,Profile,Follow
from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):

    current_user = request.user
    images =  Image.objects.filter(profile = current_user.profile)
    try:
        profile = Profile.objects.get(user = current_user)
        
    except: 
        ObjectDoesNotExist
    
    context = {
        
        'profile':profile,
        'images':images,
        'current_user':current_user
    }
    return render(request, 'users/profile.html',context)    

def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/update_profile.html', context)

def user_profile(request,pk):

    profile = Profile.objects.get(Profile, pk=pk)

    current_user = request.user
    images =  Image.objects.filter(profile = current_user.profile)
    try:
        profile = Profile.objects.get(user = current_user)
        
    except: 
        ObjectDoesNotExist
    
    context = {
        
        'profile':profile,
        'images':images,
        'current_user':current_user
    }
    return render(request, 'users/user_profile.html',context)        

@login_required
def upload_image(request):
    current_user  = request.user.profile
    if request.method =='POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('profile')
    else:
        form  = UploadImageForm()
        context  = {
            "form":form
            }
    return render(request, 'users/upload_image.html', context)    

def add_comment(request,pk):
    image = get_object_or_404(Image, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.poster = current_user
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()
        return render(request,'users/comment.html',{"user":current_user,"comment_form":form})    

def like(request,operation,pk):
    image = get_object_or_404(Image,pk=pk)
    
    if operation == 'like':
        image.likes += 1
        image.save()
    elif operation =='unlike':
        image.likes -= 1
        image.save()
    return redirect('index')

def search_users(request):
    current_user = request.user
    profile = Profile.get_profile()
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_name = Profile.find_profile(search_term)
        message = search_term

        return render(request,'users/search.html',{"message":message,
                                             "profiles":profile,
                                             "user":current_user,
                                             "username":searched_name})
    else:
        message = "You haven't searched for any user"
        return render(request,'users/search.html',{"message":message})    

def follow(request,operation,id):
    current_user=User.objects.get(id=id)
    if operation=='follow':
        Follow.follow(request.user,current_user)
        return redirect('index')
    elif operation=='unfollow':
        Follow.unfollow(request.user,current_user)
        return redirect('index')        