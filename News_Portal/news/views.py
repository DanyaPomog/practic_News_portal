from django.views.generic import ListView, DetailView
from news.models import Post


class PostList(ListView):
    model = Post
    ordering = '-time_post'
    template_name = 'news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
