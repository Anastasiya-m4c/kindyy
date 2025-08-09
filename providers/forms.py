"""
Forms module for the blog application.

Contains forms for creating and updating blog posts.
"""

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post instances.
    """

    class Meta:
        """
        Meta class to specify model and fields to include in the form.
        """
        model = Post
        fields = [
            'title', 'content', 'accepts_30_hours',
            'pickup_dropoff_available', 'address', 'area'
        ]
