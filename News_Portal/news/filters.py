import django
from django_filters import FilterSet, DateFilter

from .models import Post


class PostFilter(FilterSet):
    time_post = DateFilter(
        lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )


    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'post_category': ['exact'],

        }
