from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        author_post = self.post_set.all()
        for post in author_post:
            self.ratingAuthor += post.rating *3
            post_comments = post.comment_set.all()
            for comment in post_comments:
                self.ratingAuthor += comment.rating



#    def update_rating(self):
 #       post_rating = self.Post_set.aggregate(postRating=Sum('rating'))
 #       p_rat = 0
 #       p_rat += post_rating.get('postRating')
#
 #       com_rating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
  #      c_rat = 0
   #     c_rat += com_rating.get('commentRating')

#        self.ratingAuthor = p_rat * 3 + c_rat
 #       self.save()

class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)


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
                                     default=ARTICLE,)
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_category = models.ManyToManyField(Category, through='PostCategory')
    rating = models.IntegerField(default=0)

    def prewiew(self):
        return self.text[0:123] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
