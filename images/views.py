from django.shortcuts import render,redirect
from users.models import Image,Profile,Comment,Follow
from users.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    images = Image.get_images()
    comments = Comment.get_comment()
    profile = Profile.get_profile()

    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
        return redirect('index')

    else:
        form = CommentForm()
    return render(request,"index.html",{"images":images, "comments":comments,"form": form,"profile":profile})
