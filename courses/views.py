from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.generic.list import ListView
from .models import Course 
from django.urls import reverse_lazy 
from django.views.generic.edit import CreateView, DeleteView, UpdateView 
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin
)

def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return render(request, 'registration/logged_out.html')


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user) 
    

class OwnerEditMixin:
    def form_valid(self, form):
        form.istance.owner = self.request.user
        return super().form_valid(form)
    


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course 
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_cource_list') 



class ManageCourseListView(OwnerCourseMixin ,ListView):
    model = Course 
    template_name = 'manage/course/list.html' 
    permission_required = 'courses.view_course'


    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)







class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'manage/course/form.html' 


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course' 


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course' 


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'manage/course/delete.html' 
    permission_required = 'courses.delete_course'