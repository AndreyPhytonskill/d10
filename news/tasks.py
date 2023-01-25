from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from .models import Post, Category
import datetime as DT
from datetime import timedelta, date


@shared_task
def subscribe_category_confirmation_message(user_name, email, category_name):
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category_name}',
        message=f'«{user_name}», вы подписались на обновления категории: «{category_name}».',
        from_email='example@yandex.ru',
        recipient_list=[f'{email}', ],
    )


@shared_task
def notify_subs(sub_name, sub_email, title, category, pub_time, pk):
    post = Post.objects.get(id=pk)
    # print(sub_name, sub_email, title, category, pub_time, post)
    subject = f'{sub_name}, новая публикация в разделе {category} - {title},  ... {pub_time}'

    msg = EmailMultiAlternatives(
        subject=subject,
        body=f'Привет {sub_name}, новая публикация - {title}, в разделе {category}',  # это то же, что и message
        from_email='subscribecategory@yandex.ru',
        to=[f'{sub_email}'],  # это то же, что и recipients_list
    )

    html_content = render_to_string(
        'post_created.html',
        {
            'post': post,
            'user': sub_name,
        }
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем

    print(subject)
    print(sub_email)


def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week_ago = today- DT.timedelta(days=7)
    week = timedelta(days=7)

    for category in categories:

        category_subscribers = category.subscribers.all()

        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(category=f'{category.id}')

        for post in posts_in_category:
            time_delta = DT.datetime.now - post.time
            if time_delta < week:
                weekly_posts_in_category.append(post)
                print(f'Дата публикации: {post.time}')
                print(f'Дельта: {time_delta}')
                print('----------------   ---------------')

        print(f'ID: {category.id}')
        print(category)
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email='subscribecategory@yandex.ru',
                to=category_subscribers_emails,
            )

            # получаем наш html
            html_content = render_to_string(
                'weekly_digest.html',
                {
                    'digest': weekly_posts_in_category,
                    'category': category,
                }
            )

            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
        else:
            continue