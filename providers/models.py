from django.db import models
from django.contrib.auth.models import User
from .choices import SWANSEA_AREAS
from django.utils.text import slugify



STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=1)
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

    def save(self, *args, **kwargs):
        # Automatically generate a slug if it is not provided
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title} | written by {self.author}"


