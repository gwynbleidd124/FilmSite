from Film.utils import menu

def get_film_context(request):
    return {'menu': menu}