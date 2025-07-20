from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
from .choices import SWANSEA_AREAS


STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    accepts_30_hours = models.BooleanField(
        default=False,
        help_text="Tick if you accept 30 hours free childcare vouchers"
    )
    pickup_dropoff_available = models.BooleanField(
        default=False,
        help_text="Tick if you offer pick-up and drop-off services"
    )
    address = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    area = models.CharField(max_length=50, choices=SWANSEA_AREAS, default='swansea_city_centre')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


