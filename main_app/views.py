# import
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Toy
from .forms import FeedingForm

# Create views here
# def home(request):
#   return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cat-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def about(request):
  return render(request, 'about.html')

@login_required
def cat_index(request):
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cat_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  feeding_form = FeedingForm()
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  return render(request, 'cats/detail.html', {
    'cat': cat,
    'feeding_form': feeding_form,
    'toys': toys_cat_doesnt_have
  })

@login_required
def add_feeding(request, cat_id):
  # create a ModelForminstance using date in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save form to the db until it has cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('cat-detail', cat_id=cat_id)

@login_required
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('cat-detail', cat_id=cat_id)

class Home(LoginView):
  template_name = 'home.html'

class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age'] # disallow renaming of cat

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'