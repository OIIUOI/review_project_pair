from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from PIL import Image
from django.core.paginator import Paginator
from pilkit.processors import Thumbnail

# Create your views here.
def index(request):
    reviews = Review.objects.all().order_by('-pk')
    page = int(request.GET.get('p', 1))
    pagenator = Paginator(reviews, 5)
    boards = pagenator.get_page(page)
    context = {
        'reviews': reviews,
        "boards":boards,
    }
    return render(request, 'reviews/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        Review_Form = ReviewForm(request.POST, request.FILES)
        if Review_Form.is_valid():
            post = Review_Form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('reviews:index')
    else: 
        Review_Form = ReviewForm()
    context = {
        'Review_Form': Review_Form
    }
    return render(request, 'reviews/create.html', context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        'review':review,
    }
    return render(request, 'reviews/detail.html', context)