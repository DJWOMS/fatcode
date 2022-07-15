from src.profiles import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic.base import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from src.profiles.models import FatUser


class RegisterUser(FormView):
    form_class = forms.RegisterUserForm
    success_url = '/account/login/'
    template_name = 'profiles/registration/registration.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "profiles/registration/login.html"
    success_url = "/account/profile/"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')

        return super().get(self, request)

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/account/login/')


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = FatUser.objects.get(pk=self.request.user.id)

        return context

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().get(self, request)
