from django.views.generic import (ListView, DetailView,
                                  UpdateView, DeleteView, CreateView)
from .forms import PostForm
from news.models import Post
from .filters import PostFilter, FilterSet, DateFilter
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-time_post'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'new'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    context_object_name = 'article'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post'


class PostDelete(DeleteView):
    model = Post
    template_name = 'Post_delete.html'
    success_url = reverse_lazy('news_list')


#class ArticleUpdate(UpdateView):
 #   form_class = ArticleForm
  #  model = Post
   # template_name = 'article_create.html'
    #context_object_name = 'article'


#class ArticleDelete(DeleteView):
 #   model = Post
  #  template_name = 'post_update.html'
   # success_url = reverse_lazy('news_list')
