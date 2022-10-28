from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'content', 'grade', 'image', 'thumbnail']
        labels = {
            "title": "제목",
            "content": "내용",
            "grade":"평점",
            "image":"이미지",
            "thumbnail":"썸네일",
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]
        labels = {
            "content": "",
        }
        error_messages = {
            'content': {
                'required':"",
            },
        }