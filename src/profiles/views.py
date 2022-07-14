from django.shortcuts import render
from src.profiles import forms
from django.views.generic.edit import FormView


class RegisterUser(FormView):
    form_class = forms.RegisterUserForm
    success_url = '/login/'
    template_name = 'profiles/registration/login.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
