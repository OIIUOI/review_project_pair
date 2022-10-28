from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    RATING = [
    (1, "★"),
    (2, "★★"),
    (3, "★★★"),
    (4, "★★★★"),
    (5, "★★★★★"),
    ]
    grade = models.IntegerField(choices=RATING, default=None)
    image = models.ImageField(upload_to='image/', blank=True)
    thumbnail = ProcessedImageField(upload_to='image/', blank=True,
                                processors=[ResizeToFill(200, 100)],
                                format='JPEG',
                                options={'quality': 80})
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_user = models.ManyToManyField(get_user_model(), related_name='like_Review')

    @property
    def update_counter(self):
        self.hits = self.hits + 1
        self.save()
    


class Comment(models.Model):
    content = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)