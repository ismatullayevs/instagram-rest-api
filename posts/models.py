from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class DateStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(DateStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to="post_images/")
    caption = models.TextField(max_length=128, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ('-created_at',)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(DateStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1024)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created_at',)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def replies_count(self):
        return self.replies.count()


class Reply(DateStampedModel):
    replied_to = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField(max_length=1024)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created_at',)

    @property
    def likes_count(self):
        return self.likes.count()


class Tag(models.Model):
    name = models.CharField(max_length=40, validators=[RegexValidator(
        "^[a-zA-Z0-9_]+$", message="Invalid name for tag")])

    def __str__(self):
        return self.name
