from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserChangeForm, UserLoginForm
from django.contrib.auth import login, logout, get_user_model
from .models import UserEmailConfirmed

# for email verification
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.contrib import messages

User = get_user_model()
# Create your views here.
def RegisterView(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()

            # Email Sending
            user = UserEmailConfirmed.objects.get(user=instance)
            site = get_current_site(request)
            email = instance.email
            first_name = instance.first_name
            last_name = instance.last_name
            email_body = render_to_string(
                'App_Register/verify_email.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'domain': site.domain,
                    'activation_key': user.activation_key
                }
            )
            send_mail(
                subject='Account Confirmation!!',
                message= email_body,
                from_email='abdullah.al.nahdi2426@gmail.com',
                recipient_list=[email],
                fail_silently=True
            )
            return render(request, 'App_Register/register_start.html',{})
        return render(request, 'App_Register/register_page.html',{'form':form})
    return render(request, 'App_Register/register_page.html',{'form':form})


def LoginView(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            if _next:
                return redirect(_next)
            return render(request, 'App_Register/login_success.html', {})
        return render(request, 'App_Register/login_page.html', {'form':form})
    return render(request, 'App_Register/login_page.html', {'form':form})

def LogoutView(request):
    logout(request)
    return render(request, 'App_Register/logout_page.html', {})

def EmailConfirmation(request, activation_key):
    user = get_object_or_404(UserEmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed = True
        user.save()

        instance = User.objects.get(email=user)
        instance.is_active = True
        instance.save()
        return render(request, 'App_Register/register_end.html', {})