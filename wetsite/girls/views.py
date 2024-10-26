from typing import Any
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import *
from .models import *
from .utils import *

class GirlsHome(DataMixin, ListView):
    model = Girls
    template_name = 'girls/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Girls.objects.filter(is_published=True).select_related('cat')

# def index(request):
#     posts = Girls.objects.all()

#     contextQ = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }

#     return render(request, 'girls/index.html', context=contextQ)
# @login_required  404 декоратор для функций

def about(request):
    contact_list = Girls.objects.all()
    paginator = Paginator(contact_list, 3)
    # пагинатор для функций
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'girls/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'girls/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home') # перенаправление на хоум если не авторизован
    raise_exception = True # доступ запрещен 403
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'girls/addpage.html', {'form': form, 'title': 'Добавление статьи'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'girls/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'girls/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'girls/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

def LogoutUser(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Girls
    template_name = 'girls/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Girls, slug=post_slug)

#     contextW = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }

#     return render(request, 'girls/post.html', context=contextW)

class GirlsCategory(DataMixin, ListView):
    model = Girls
    template_name = 'girls/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Girls.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), 
                                      cat_selected = c.pk)
        return dict(list(context.items()) + list(c_def.items()))



# def show_category(request, cat_slug):

#     posts = Girls.objects.filter(cat__slug=cat_slug)

#     contextE = {'title': 'Отображение по рубрикам',
#             'posts': posts,
#             'cat_selected': cat_slug
#             }

#     if len(posts) == 0:
#         raise Http404
    
#     return render(request, 'girls/index.html', context=contextE)

