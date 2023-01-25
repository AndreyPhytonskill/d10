from .models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import notify_subs


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if instance.category.first():
        print(instance.category.first())

        cat = instance.category.first()
        subscribers = cat.subscribers.all()
        subscribers_emails = cat.subscribers.all().values('email')
        subscribers_names = cat.subscribers.all().values('username')

        print(subscribers_emails)
        print(subscribers_names)

        user_emails = []
        user_names = []

        for subscriber in subscribers:
            user_emails.append(subscriber.email)
            user_names.append(subscriber.username)
            sub_name = subscriber.username
            sub_email = subscriber.email
            title = instance.title
            pub_time = instance.date.strftime("%d %m %Y")
            pk = instance.pk
            post = Post.objects.get(id=pk)
            category = Post.objects.get(id=pk).category.get().name_category

            notify_subs.delay(sub_name, sub_email, title, category, pub_time, pk)