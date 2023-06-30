import random
import pytz
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from utils import otp_code
from .forms import UserRegisterForm, UserRegisterVerifyCodeForm, UserLoginForm
from .models import User, OtpCode


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)  # Generate random code
            otp_code(cd['phone_number'], random_code)  # Send random code
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_register_info'] = {
                'full_name': cd['full_name'],
                'email': cd['email'],
                'phone_number': cd['phone_number'],
                'password': cd['password'],
            }
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = UserRegisterVerifyCodeForm
    template_name = 'accounts/verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_register_info']
        code_instance = get_object_or_404(OtpCode, phone_number=user_session['phone_number'])
        if form.is_valid():
            if (datetime.now(tz=pytz.timezone('Asia/Tehran')) - code_instance.created) < timedelta(minutes=2):
                if form.cleaned_data['code'] == code_instance.code:
                    User.objects.create_user(
                        email=user_session['email'],
                        full_name=user_session['full_name'],
                        phone_number=user_session['phone_number'],
                        password=user_session['password']
                    )
                    code_instance.delete()
                    return redirect('home:home')
                else:
                    return redirect('accounts:verify_code')
            else:
                code_instance.delete()
                return redirect('accounts:user_register')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                return redirect('accounts:user_login')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        return render(request, 'accounts/profile.html', {'user': user})
