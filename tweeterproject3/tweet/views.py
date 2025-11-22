from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def home(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, "home.html", {"posts":posts})

@login_required
def createpost(request):
    if request.method=="POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()

            return redirect("/")
    else:
        form = TweetForm()

    return render(request, "createpost.html", {"form":form})

@login_required
def editpost(request, postid):
    post_inst = get_object_or_404(Post, id=postid, user=request.user)
    if request.method=="POST":
        form = TweetForm(request.POST, request.FILES, instance=post_inst)
        tweet = form.save(commit=False)
        tweet.user = request.user
        tweet.save()

        return redirect("/")
    else:
        form = TweetForm(instance=post_inst)

    return render(request, "editpost.html", {"form":form})

def delpost(request, postid):
    post = get_object_or_404(Post, id=postid, user=request.user)
    post.delete()

    return redirect("/")


def register(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect("/")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form":form})