from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('registration/', IndexView.as_view(template_name='flatpages/registration.html'), name='registration'),
]