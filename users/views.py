import hashlib
import random
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .utils import send_email_for_verify
from .forms import RegisterForm, AuthenticationForm, ProfileForm
from .models import Profile
from campaigns.models import Campaign


def home(request):
    return render(request, 'home.html')


def get_robohash_url(email, size = 100):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    random_id = random.randint(1, 10)
    return f'https://robohash.org/{email_hash}?set=set{random_id}&size={size}x{size}'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.avatar_url = get_robohash_url(user.email)
                user.save()
                send_email_for_verify(request, user)
                messages.success(request, "Registration successful. Please check your email to verify your account.")
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


class EmailVerify(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            messages.error(request, f"Verification link error: {e}")

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified successfully. You can now log in.')
            return redirect('users:login')
        else:
            messages.error(request, 'Verification link is invalid or has expired.')
            return redirect('users:register')


@login_required
def profile_view(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        campaigns = Campaign.objects.filter(owner=request.user)
    except Exception as e:
        messages.error(request, f"An error occurred while fetching profile: {e}")
        return redirect('users:profile')

    return render(request, 'users/profile.html', {'profile': profile, 'campaigns': campaigns})


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('users:profile')
            except Exception as e:
                messages.error(request, f"An error occurred while updating profile: {e}")
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})


