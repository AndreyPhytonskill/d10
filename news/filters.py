import django_filters
from .models import Post, Author
import django.forms

class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name='title', label='Заголовок содержит', lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text', 'class': "form-control", 'placeholder': "Ведите текст..."}))

    date_time__gt = django_filters.DateFilter(
        field_name="time", label="От даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

#    date_time__lt = django_filters.DateFilter(
#        field_name="time", label="До даты", lookup_expr='lt',
#        widget=django.forms.DateInput(
#            attrs={'type': 'date', 'class': "form-control"}))

    class Meta:
        model = Post
        # Порядок в словаре определяет порядок вывода полей в HTML
        fields = {'title','category',}