from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def allposts(request):
    if request.method == "POST":
        poster = request.user
        content = request.POST["content"]

        post = Post(poster=poster,content=content)
        post.save()
        return HttpResponseRedirect(reverse("allposts"))
    else:
        posts = Post.objects.order_by('-timestamp')
        paginator = Paginator(posts,9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"network/allposts.html",{
            "page_obj":page_obj
        })

def followers(request,user_id):
    user = User.objects.get(pk=user_id)
    return render(request,"network/follower.html",{
        "people": user.follower.all()
    })

def followings(request,user_id):
    user = User.objects.get(pk=user_id)
    return render(request,"network/following.html",{
        "people":user.followers.all()
    })



def user(request,user_id):
    user = User.objects.get(pk=user_id)
    posts = user.posts.order_by("-timestamp")
    paginator = Paginator(posts,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/user.html",{
        "username":user.username,
        "self": user == request.user,
        "user_id":user.id,
        "num_followers":user.follower.count,
        "num_followings":user.followers.all().count,
        "page_obj":page_obj,
        "following":user in request.user.followers.all()
    })

def unfollow(request,user_id):
    user = User.objects.get(pk=user_id)
    request.user.followers.remove(user)
    return HttpResponseRedirect(reverse('user',args=(user_id,)))


def follow(request,user_id):
    user = User.objects.get(pk=user_id)
    request.user.followers.add(user)
    return HttpResponseRedirect(reverse('user',args=(user_id,)))

def following(request,user_id):
    user = User.objects.get(pk=user_id)
    allpost = Post.objects.filter(poster__in = user.followers.all()).order_by("-timestamp")

    paginator = Paginator(allpost,9)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request,"network/followings.html",{
        "page_obj": page_obj
    })

@csrf_exempt
def post(request,post_id):
    try:
        post = Post.objects.get(pk=post_id,poster=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found."},status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
def like(request,post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found."},status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("status") is not None:
            if data["status"] == "Like":
                post.likes = post.likes + 1
            else:
                post.likes = post.likes - 1
        post.save()
        return HttpResponse(status=204)
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)





