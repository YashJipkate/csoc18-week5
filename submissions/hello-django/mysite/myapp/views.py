from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Armoury
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

def hello(request):
    response = requests.get('http://api.ipstack.com/check?access_key=e982de7daa879f35d6e4bacae8689fa7&format=1&legacy=1')
    location_data = response.json()

    context = {
        'city': location_data['city'],
        'region': location_data['region_name'],
    }

    return render(request, 'myapp/index.html', context)

def inventory(request):
    armoury = Armoury.objects.all()
    armoury_set = Armoury.objects.all().distinct('item_name').iterator()
    response = requests.get('http://api.ipstack.com/check?access_key=e982de7daa879f35d6e4bacae8689fa7&format=1&legacy=1')
    location_data = response.json()

    context = {
        'armoury': armoury,
        'armoury_set': armoury_set,
        'city': location_data['city'],
        'region': location_data['region_name'],
    }
    return render(request, 'myapp/index1.html', context)

def add(request):
    return render(request, 'myapp/forms.html')

class addarms(LoginRequiredMixin ,CreateView):
    login_url = reverse_lazy('login')
    redirect_field_name = reverse_lazy('addarms')
    model = Armoury
    success_url = reverse_lazy('inventory')
    fields = ['item_name', 'quantity', 'price']

class updatearms(UpdateView):
    model = Armoury
    success_url = reverse_lazy('inventory')
    fields = ['item_name', 'quantity', 'price']

@login_required
def selectupdate(request):
    armoury = Armoury.objects.all()
    context = {
        'armoury': armoury,
    }
    return render(request, 'myapp/selectupdate.html', context)

class UserFormView(View):
    form_class = UserForm
    template_name = 'myapp/registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inventory')

        return render(request, self.template_name, {'form': form}) 