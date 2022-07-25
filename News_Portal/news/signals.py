import sys
from django.utils import timezone
from datetime import datetime, timedelta, date

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail, EmailMultiAlternatives
from .models import Category, CategorySubscribers, Post, User, PostCategory
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from News_Portal.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender = PostCategory)
def message_to_sub(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.post_category.all():
            for subscribe in CategorySubscribers.objects.filter(category_sub=cat):

                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[subscribe.subscriber_user.email],
                )
                print(f'{subscribe.subscriber_user.email} почта пописчика {subscribe}')

                port = sys.argv[-2]

                html_content = render_to_string(
                    'alarm.html',
                    {
                        'post': instance.text,
                        'recipient': subscribe.subscriber_user.email,
                        'category_name': subscribe.category_sub,
                        'subscriber_user': subscribe.subscriber_user,
                        'pk_id': instance.pk,
                        'date': instance.time_post,

                        'port': port,
                    }
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                print(f'{instance.title} {instance.text}')
                print('Уведомление отослано подписчику ', subscribe.subscriber_user, 'на почту',
                      subscribe.subscriber_user.email, ' на тему ', subscribe.category_sub)


def get_email_sub(CategorySubscribers):
    email_recipients = []
    for user in subscriber_user:
        email_recipients.append(user.email)
        print(email_recipients)
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    html = render_to_string(
        kwargs['template'],
        {'post_category': kwargs['post_category'], 'post_object': post_object}
        )
    print(kwargs['post_category'])

    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=DEFAULT_FROM_EMAIL,
        to=kwargs['email_recipients']
        )

    print(kwargs)

    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)

def week_post_2():
    week = timedelta(days=1)
    posts = Post.objects.all()
    past_week_posts = []
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for post in posts:
        time_delta = date.today() - post.time_post.date()
        if time_delta < week:
            past_week_posts.append(post)

    past_week_categories = set()
    for post in past_week_posts:
        for category in post.post_category.all():
            past_week_categories.add(category)
    print(f'past_week_categories = {past_week_categories}')

    email_recipients_set = set()
    for category in past_week_categories:
        print(f'category.subscribers.all = {category.subscribers.all()}')
        get_user_emails = set(get_email_sub(category))
        email_recipients_set.update(get_user_emails)
        print(f'get_user_emails = {get_user_emails}')
    email_recipients = list(email_recipients_set)
    print(email_recipients)

    for email in email_recipients:
        post_object = []
        categories = set()

        for post in past_week_posts:
            subscription  = post.post_category.all().values('subscribers').filter(subscribers__email=email)

            if subscription.exists():
                print(f'subscription = {subscription}')
                post_object.append(post)
                categories.update(post.post_category.filter(subscribers__email = email))

            print(f'email = {email}')
            print(f'post_object = {post_object}')

            category_object = list(categories)

            print(f'category_object = {category_object}')
            print(f'set(post.cats.all()) = {set(post.post_category.all())}')

            send_mail(
                #post_object,
                category_object = category_object,
                email_subject = email_subject,
                template = template,
                email_recipients = [email, ]
            )