from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from reviews.models import Review, Comment
# Create your views here.
def index(request):
    all = get_user_model().objects.all()
    context = {
        'v':all,
    }
    return render(request,"accounts/index.html",context)
def signup(request):
    if request.method == "POST":
        userform = CustomUserCreationForm(request.POST)
        if userform.is_valid():
            userform.save()
            return redirect("reviews:index")
    else:
        userform = CustomUserCreationForm()
    context = {"userform": userform}
    return render(request, "accounts/signup.html", context)


def log_in(request):
    if request.method == "POST":
        loginform = AuthenticationForm(request, request.POST)
        if loginform.is_valid():
            login(request, loginform.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        loginform = AuthenticationForm()
    context = {"loginform": loginform}
    return render(request, "accounts/login.html", context)


def log_out(request):
    logout(request)
    return redirect("reviews:index")


@login_required
def changepassword(request):
    if request.method == "POST":
        changepassword = PasswordChangeForm(request.user, request.POST)
        if changepassword.is_valid():
            changepassword.save()
            return redirect("accounts:login")
    else:
        changepassword = PasswordChangeForm(request.user)
    context = {"changepassword": changepassword}
    return render(request, "accounts/changepassword.html", context)

def detail(request, pk):
    user = get_user_model().objects.get(pk = pk)
    reviews = Review.objects.filter(user_id = pk)
    comments = Comment.objects.filter(user_id = pk)
    person = get_object_or_404(get_user_model(), pk = pk)
    context = {
        "person": person,
        'user': user,
        'reviews': reviews,
        'comments': comments,
    }
    return render(request, 'accounts/detail.html', context)
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk = user_pk)
        if person != request.user:
            if person.followers.filter(pk = request.user.pk).exists():
                person.followers.remove(request.user)
                is_followed = False
            else:
                person.followers.add(request.user)
                is_followed = True
            data = {
                'is_followed': is_followed,
                'followers_count': person.followers.count(),
                'followings_count': person.followings.count(),
            }
            return JsonResponse(data)
        return redirect('accounts:detail', person.pk)
    return redirect('accounts:login')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES ,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(request.FILES, instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

def delete(request):
    request.user.delete()
    logout(request)
    return redirect('reviews:index')