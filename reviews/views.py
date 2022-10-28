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
from django.contrib import messages

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

@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user.pk == review.user.pk:
        review.delete()
        return redirect('reviews:index')
    else:
        messages.warning(request, '작성자만 삭제 할 수 있습니다.')
        return redirect('reviews:detail', pk)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review':review,
        'comment_form':comment_form,
        'comments':comments,
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('reviews:detail', pk)
        else:
            Review_Form = ReviewForm(instance=review)
        context = {
            'Review_Form':Review_Form
        }
        return render(request, 'reviews/create.html', context)
    else:
        return redirect('reviews:detail', pk)

@login_required
def comments_create(request,pk):
    if request.user.is_authenticated:
        review = Review.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = review
            comment.user = request.user
            comment.save()

            return redirect('reviews:detail', pk)
        


@login_required
def comments_delete(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.pk == comment.user.pk:
        comment.delete()
        return redirect('reviews:detail', review.pk)
    else:
        messages.warning(request, '작성자만 삭제 할 수 있습니다.')
        return redirect('reviews:detail', review.pk)
