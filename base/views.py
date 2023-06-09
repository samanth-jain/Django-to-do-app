
from typing import Any, Dict, Optional
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task
from .forms import PositionForm

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm                 


class CustomLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('task')

class Register(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')        
        return super(Register, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/list.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['tasks'] = context['tasks'].filter(user=self.request.user)
       context['count'] = context['tasks'].filter(completed=False).count() 
       search_input = self.request.GET.get('search') or ''
       if search_input:
           context['tasks'] = context['tasks'].filter(title__contains=search_input)

       context['search_input'] = search_input

       return context
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'taskdetail'
    template_name  = 'base/details.html'
    # def get_context_data(self, **kwargs) :
    #     context =  super().get_context_data(**kwargs)
    #     context['taskdetail'] = context['taskdetail'].filter(title = self.request.)
    #     return context


    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated is False:
            return redirect('task')        
        return super(TaskDetail, self).get(*args, **kwargs)
    
   
    

    

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'desc', 'completed']
    success_url = reverse_lazy('task')
    # context_object_name = 'create-list'
    template_name = 'base/create-list.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task')
    context_object_name = 'update-list'
    template_name = 'base/create-list.html'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    
    success_url = reverse_lazy('task')
    context_object_name = 'task'
    template_name = 'base/delete-list.html'

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))