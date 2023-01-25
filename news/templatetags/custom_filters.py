from django import template

register = template.Library()

stop_list_words = ['редиска','Дзюдо', 'дурак', 'идиот', 'Редиска', 'редиски', 'Редиски']


@register.filter()
def censor(input_value: str):
    for stop_word in stop_list_words:
        while stop_word in input_value:
            stars_string = '*' * len(stop_word[1:len(stop_word) - 1])
            replace_string = stop_word.replace(stop_word[1:len(stop_word) - 1], stars_string)
            input_value = input_value.replace(stop_word, replace_string)
    return input_value