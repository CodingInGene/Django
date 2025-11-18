from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def tweets(request):
    tweets = Tweet.objects.all()
    return render(request, "tweetlist.html", {"tweets":tweets})

def createtweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.user = request.user
            new_tweet.save()
            
            return redirect('/tweets/')
    else:
        form = TweetForm()

    return render(request, "createtweet.html", {"form":form})

def edittweet(request, postid):
    tweet = get_object_or_404(Tweet, id=postid, user=request.user)  #Pre fill form with the tweet to edit
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        edited_tweet = form.save(commit=False)
        edited_tweet.user = request.user
        edited_tweet.save()

        return redirect("/tweets/")
    else:
        form = TweetForm(instance=tweet)

    return render(request, "edittweet.html", {"form":form})

def deletetweet(request, postid):
    tweet = Tweet.objects.filter(id=postid).filter(user=request.user)
    tweet.delete()
    return redirect("/tweets/")