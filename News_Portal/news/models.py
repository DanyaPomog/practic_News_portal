from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from allauth.account.forms import SignupForm


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser}, rating = {self.ratingAuthor}'

    def update_rating(self):
        author_post = self.post_set.all()
        for post in author_post:
            self.ratingAuthor += post.rating * 3
            post_comments = post.comment_set.all()
            for comment in post_comments:
                self.ratingAuthor += comment.rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True, )#verbose_name='Категория'
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', blank=True, ) #verbose_name='Подписчик'
    objects = models.Manager()

    def __str__(self):
        return f'{self.name_category}'

    def subscriber(self):
        pass

    def get_category(self):
        return self.name_category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    #def __str__(self):
     #   return f'{self.subscribers} подписан на категорию {self.name_category}'

    def is_subscribed(self):
        cat = Category.objects.get(id=self.pk)
        return cat.subscribers.filter(id=User.pk).exists()



class CategorySubscribers(models.Model):
    objects = None
    subscriber_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category_sub = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_post = models.DateTimeField(auto_now_add=True)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    category_type = models.CharField(max_length=2,
                                     choices=CATEGORY_CHOICES,
                                     default=ARTICLE, )
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_category = models.ManyToManyField(Category, through='PostCategory')
    rating = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        post_metadata = f"'{self.title}' by {self.author},\n \
                          published on: {self.time_post.strftime('%d/%m/%Y, %H:%M')},\n \
                          the rating of this post is {self.rating}\nPreview: {self.preview()}"
        return post_metadata

    def __str__(self):
        post_category = f'{self.post_category}'
        return post_category

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        if len(self.text) > 124:
            return f'{self.text[:124]}...'
        return f'{self.text}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост в категории')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category}, Пост: {self.post}'

    class Meta:
        verbose_name = 'Связь категории'
        verbose_name_plural = 'Связь категории'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_comm = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        comment_metadata = f"{self.user.username} wrote: '{self.text[:64]}',\n \
                             on: {self.time_comm.strftime('%d-%m-%Y, %H:%M')},\n \
                             the rating of this comment is {self.rating}\n"
        return comment_metadata


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user.save()
        return user
