from django.urls import path
from .views import (PostList, ArticleCreate, PostDetail, NewsCreate, PostUpdate, PostDelete,
                    UserUpdate, IndexView, upgrade_me, CategoryDetail, subscribe_to_category, unsubscribe_from_category)
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView

from .views import AppointmentView


urlpatterns = [
   path('list/', PostList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),

   path('new/create/', NewsCreate.as_view(), name='new_create'),

   path('post/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('user/<int:pk>', UserUpdate.as_view()),
   path('', IndexView.as_view()),
   path('login/',
        LoginView.as_view(template_name='sign/login.html'),
        name='login'),
   path('sign/logout/',
        LogoutView.as_view(template_name='sign/logout.html'),
        name='logout'),
   path('signup/',
        BaseRegisterView.as_view(template_name='sign/signup.html'),
        name='signup'),
   path('upgrade/', upgrade_me, name = 'upgrade'),
   path('unsubscribe/category/<int:pk>', unsubscribe_from_category, name='unsubscribe_from_category'),
   path('cat/subscribe/category/<int:pk>', subscribe_to_category, name='subscribe_to_category'),
   path('cat/', CategoryDetail.as_view(template_name='cat_sub.html'), name='category'),
   #path('cat/unsub/'),
]
