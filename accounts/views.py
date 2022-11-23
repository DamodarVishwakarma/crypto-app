from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from accounts.models import user_type, User
from django.views.generic import CreateView, View
from accounts.forms import UserSignUpForm, AdminUserForm, LoginForm
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'User'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('login')



class AdminUserView(CreateView):
    model = User
    form_class = AdminUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        user = form.save()
        return redirect('login')


def home(request):
    if request.user.is_authenticated:
        return redirect('pet_list')
    else:
        return render(request, 'home.html')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")


class LoginView(View):
	model = User
	form_class = LoginForm
	template_name = 'accounts/login.html'
	success_url = reverse_lazy('home')