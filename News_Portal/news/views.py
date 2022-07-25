from django.views.generic import (ListView, DetailView,
                                  UpdateView, DeleteView, CreateView)
from .forms import PostForm
from .models import Post, User, Category, CategorySubscribers, PostCategory
from .filters import PostFilter
from django.urls import reverse_lazy
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import mail_admins
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from .models import Appointment

from django.http import HttpResponseRedirect

from django.urls import resolve
from django.conf import settings
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import BaseRegisterForm


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if not is_subscribed:
        cat.subscribers.add(user)
        html = render_to_string(  # передаем в шаблон переменные, тут передал категорию для вывода ее в письме
            template_name='alarm.html',
            context={
                'categories': cat,
                'user': user,
            },
        )
        cat_repr = f'{cat}'
        email = user.email
        msg = EmailMultiAlternatives(
            subject=f'Subscription to {cat_repr} category',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, user.email],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)

        return redirect('/')

    return redirect('/')  # (request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if is_subscribed:
        cat.subscribers.remove(user)
    return redirect('/list/')


class PostList(ListView):
    model = Post
    ordering = '-time_post'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5
    cat = Post.post_category

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = Category.objects.all()
        context['time_now'] = datetime.now()
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

    permission_required = 'news.add_new'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    context_object_name = 'article'

    #permission_required = 'news.add_article'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post'

    permission_required = 'news.add_post'


class PostDelete(DeleteView):
    model = Post
    template_name = 'Post_delete.html'
    success_url = reverse_lazy('news_list')


class UserUpdate(UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user'
    template_name = 'user_update.html'
    fields = [
            'username',
            'email',
            'first_name',
        ]
    success_url = reverse_lazy('news_list')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'list/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class CategoryDetail(ListView):
    model = Category
    context_object_name = 'category_detail'
    template_name = 'cat_sub.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['category_post'] = Post.objects.filter(post_category=id)
        context['subscription_object'] = 'category_subscription'
        context['name'] = Category.objects.filter(id=id)
        is_subscribed= CategorySubscribers.objects.filter(
            category_sub=id, subscriber_user=user).exists()
        #is_subscribed = CategorySubscribers.objects.filter(id=id).subscriber_user.filter(id=user.id).exists()
        context['is_subscribed'] = is_subscribed
        return context



#class CategoryViews(TemplateView):
 #   template_name = 'cat_sub.html'
  #  model = Category
#
 #   def get_context_data(self, request, **kwargs):
  #      user = self.request.user
   #     context = super().get_context_data(**kwargs)
    #    context['subscription_object'] = 'category_subscription'
     #   #context['name'] = Category.objects.get(id=self.id)
#
 #       is_subscribed = Category.objects.get(id=id).subscribers.filter(id=user.id).exists()
  #      context['is_subscribed'] = is_subscribed
   #     print(context)
    #    return context




