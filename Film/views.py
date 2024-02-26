import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, CreateView


from django.views.generic.edit import FormMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddPostForm, CommentsForm
from .models import Film, Category
from .serializers import FilmSerializer
from .utils import DataMixin

class FilmHome(DataMixin, ListView):
    model = Film
    template_name = 'Film/index.html'
    title_page = 'Главная страница'
    context_object_name = 'posts'
    cat_selected = 0

    def get_queryset(self):
        return Film.published.all().order_by('-time_create').select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'Film/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    login_url = '/users/login'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        form.save()
        return super().form_valid(form)
def contact(request):
    return HttpResponse('Контакты')

class ShowPost(FormMixin, DataMixin, DetailView):
    model = Film
    template_name = 'Film/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = CommentsForm

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'post_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.films = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object.author
        likes_connected = get_object_or_404(Film, slug=self.kwargs['post_slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_of_likes'] = likes_connected.number_of_likes()
        context['post_is_liked'] = liked
        return self.get_mixin_context(context, title=context['post'].title)
        return context

class FilmCategory(DataMixin, ListView):
    template_name = 'Film/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)
        return context

    def get_queryset(self):
        return Film.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat').order_by('-time_create')


class FilmRec(DataMixin, ListView):
    model = Film
    template_name = 'Film/recommendations.html'
    title_page = 'Рекомендации'
    context_object_name = 'posts'

    def get_queryset(self):
        return Film.published.filter(rating__gte=7.5).order_by('?')[:9]

def BlogPostLike(request, blog_slug):
    post = get_object_or_404(Film, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post', args=[str(blog_slug)]))


# ------------------------API-----------------------------------------

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.published.all()
    serializer_class = FilmSerializer


class RandomFilm(APIView):
    def get(self, *args, **kwargs):
        all_film = Film.published.all()
        random_film = random.choice(all_film)
        serialized_random_film = FilmSerializer(random_film, many=False)
        return Response(serialized_random_film.data)