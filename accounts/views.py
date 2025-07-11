from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from .models import Profile
from django.shortcuts import redirect

# Create your views here.
def UserLogin(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user = authenticate(request,
                          username = data['username'],
                          password = data['password']
                          )
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponse('Muvaffaqiyatli login amalga oshirildi!')
        else:
          return HttpResponse('Sizning accountingiz faol holatda emas.')
      else:
        return HttpResponse('Login va Parolda xatolik bor!')
  else:
    form = LoginForm()
    context = {
      'form': form
    }
  return render(request, 'registration/login.html', context)

@login_required
def DashboardView(request):
  user = request.user
  user_info = Profile.objects.get(user=user)
  context = {
    'user': user,
    'profile': user_info,
  }
  return render(request, 'pages/profile.html', context)

def UserRegister(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
      new_user = user_form.save(commit=False)
      new_user.set_password(
        user_form.cleaned_data['password']
      )
      new_user.save()
      Profile.objects.create(user=new_user)
      context = {
        'new_user': new_user
      }
      return render(request, 'account/register_done.html', context)
  else:
    user_form = UserRegistrationForm()
    context = {
      'user_form': user_form
    }
    return render(request, 'account/register.html', context)

@login_required
def edit_user(request):
  if request.method == 'POST':
    user_form = UserEditForm(instance=request.user, data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      return redirect('profile')

  else:
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

  context = {
    'user_form': user_form,
    'profile_form': profile_form
  }
  return render(request, 'account/profile_edit.html', context)

class EditUserView(LoginRequiredMixin, View):
  def get(self, request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
    'user_form': user_form,
    'profile_form': profile_form
    }
    return render(request, 'account/profile_edit.html', context)

  def post(self, request):
    user_form = UserEditForm(instance=request.user, data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      return redirect('profile')


class SignUpView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'account/register.html'
