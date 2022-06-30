from django.urls import path
from .views import (PostList, ArticleCreate, PostDetail, NewsCreate, PostUpdate, PostDelete,
                    UserUpdate)


urlpatterns = [
   path('', PostList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),

   path('new/create/', NewsCreate.as_view(), name='new_create'),

   path('post/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('user/<int:pk>', UserUpdate.as_view()),
]
