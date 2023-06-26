from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
import random
from .models import OtpCode
from utils import otp_code


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

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
