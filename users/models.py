from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


GENDER_TYPES = (
    ('M', "Male"),
    ('F', "Female"),
    ('O', "Other"),
    ('N', "Prefer Not to Say")
)


class CustomUser(AbstractUser):
    avatar_thumbnail = ProcessedImageField(
        blank=True,
        upload_to='avatars',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 70}
    )
    following = models.ManyToManyField(
        'self',
        related_name="followers",
        symmetrical=False,
        blank=True,
    )
    bio = models.CharField(max_length=120, blank=True)
    website = models.CharField(max_length=40, blank=True)
    gender = models.CharField(choices=GENDER_TYPES, max_length=1, blank=True)
    is_verified = models.BooleanField(default=False)

    @property
    def posts_count(self):
        return self.posts.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()
