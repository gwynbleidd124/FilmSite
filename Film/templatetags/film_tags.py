from django import template

from Film.models import Category, Film




register = template.Library()

@register.inclusion_tag('Film/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('Film/list_rec_film.html')
def get_random_film():
    random_film = Film.objects.filter(cat=1, rating__gte=8).order_by('?')[:4]
    random_serial = Film.objects.filter(cat=2, rating__gte=8).order_by('?')[:4]
    return {'random_film': random_film, 'random_serial': random_serial}





