from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Category, Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    recent_categories = Category.objects.all().order_by('-id')[:3]
    popular_categories = [Category.objects.get(pk=1)], [Category.objects.get(pk=2)], [Category.objects.get(pk=3)],
    return render(request, 'category/home.html', {'recent_categories': recent_categories,
                                                  'popular_categories': popular_categories})


@login_required
def dashboard(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'category/dashboard.html', {'categories': categories})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateCategory(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ['title']
    template_name = 'category/create_category.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateCategory, self).form_valid(form)
        return redirect('dashboard')


class DetailCategory(generic.DetailView):
    model = Category
    template_name = 'category/detail_category.html'


class DetailRecipe(generic.DetailView):
    model = Recipe
    template_name = 'category/detail_recipe.html'


class UpdateCategory(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'category/update_category.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        category = super(UpdateCategory, self).get_object()
        if not category.user == self.request.user:
            raise Http404
        return category



class UpdateRecipe(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    template_name = 'category/update_recipe.html'
    fields = ['title', 'prep_time', 'cook_time', 'servings', 'ingredients', 'directions']
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        recipe = super(UpdateRecipe, self).get_object()
        if not recipe.category.user == self.request.user:
            raise Http404
        return recipe


class DeleteCategory(LoginRequiredMixin, generic.DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        cat = super(DeleteCategory, self).get_object()
        if not cat.user == self.request.user:
            raise Http404
        return cat


class DeleteRecipe(LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    template_name = 'category/delete_recipe.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        recipe = super(DeleteRecipe, self).get_object()
        if not recipe.category.user == self.request.user:
            raise Http404
        return recipe


@login_required
def add_recipe(request, pk):
    form = RecipeForm()
    cat = Category.objects.get(pk=pk)
    if not cat.user == request.user:
        raise Http404
    if request.method == 'POST':
        done_form = RecipeForm(request.POST)
        if done_form.is_valid():
            recipe = Recipe()
            recipe.category = cat
            recipe.title = done_form.cleaned_data['title']
            recipe.picture = done_form.instance
            recipe.prep_time = done_form.cleaned_data['prep_time']
            recipe.cook_time = done_form.cleaned_data['cook_time']
            recipe.servings = done_form.cleaned_data['servings']
            recipe.ingredients = done_form.cleaned_data['ingredients']
            recipe.directions = done_form.cleaned_data['directions']
            recipe.category = Category.objects.get(pk=pk)
            recipe.save()
            return redirect('detail_category', pk)

    return render(request, 'category/add_recipe.html', {'form': form})
